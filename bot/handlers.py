"""Telegram command and message handlers."""

from __future__ import annotations

from pathlib import Path

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.app import BotApp, app
from bot.llm import call_llm, load_system_prompt, trim_history
from bot.models import (
    MODEL_CATALOG,
    compatible_models,
    current_api,
    model_short_name,
    set_user_model,
)
from safety import (
    DECLARATION,
    build_hotline_card,
    build_safety_fallback,
    check_output_safety,
    detect_crisis,
    log_crisis,
)

YOUTH_KEYWORDS = ("學校", "DSE", "考試", "阿爸阿媽", "中學", "功課", "老師")


def _is_youth_message(text: str) -> bool:
    return any(kw in text for kw in YOUTH_KEYWORDS)


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    bot_app: BotApp = app,
) -> None:
    """``/start`` — show the 指月 declaration."""
    user_id = update.effective_user.id
    bot_app.session.clear(user_id)
    await update.message.reply_text(DECLARATION, parse_mode="Markdown")


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    bot_app: BotApp = app,
) -> None:
    """Main message handler: safety → LLM → safety → reply."""
    user_id = update.effective_user.id
    user_text = update.message.text

    if not user_text:
        return

    if detect_crisis(user_text):
        bot_app.session.crisis_rounds[user_id] += 1
        round_num = bot_app.session.crisis_rounds[user_id]
        hotline_card = build_hotline_card(is_youth=_is_youth_message(user_text))
        log_crisis(
            user_id,
            user_text,
            hotline_card,
            log_dir=str(bot_app.crisis_log_dir),
        )

        await update.message.reply_text(
            "我聽到你。你而家嘅感受好真實。\n\n"
            "我係 AI，唔能夠取代真人嘅陪伴。\n\n"
            + hotline_card
        )

        if round_num >= bot_app.crisis_rounds_limit:
            await update.message.reply_text(
                "我陪你到呢度。你而家最需要嘅唔係我，係真人。\n\n"
                "請打 2389 2222，佢哋 24 小時喺度。"
            )
            bot_app.session.conversations[user_id] = []
            bot_app.session.crisis_rounds[user_id] = 0
        return

    history = bot_app.session.conversations[user_id]
    if not history:
        prompt_path = Path(bot_app.config.system_prompt_path)
        history.append(
            {"role": "system", "content": load_system_prompt(prompt_path)}
        )

    history.append({"role": "user", "content": user_text})
    history = trim_history(history, max_history=bot_app.max_history)
    bot_app.session.conversations[user_id] = history

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    llm_response = await call_llm(
        bot_app.llm_client,
        history,
        model=bot_app.session.user_models[user_id],
        max_tokens=bot_app.config.llm_max_tokens,
    )

    if bot_app.session.crisis_rounds[user_id] > 0 and not check_output_safety(
        llm_response
    ):
        fallback = build_safety_fallback()
        log_crisis(
            user_id,
            user_text,
            f"[OUTPUT BLOCKED] {llm_response[:100]}",
            log_dir=str(bot_app.crisis_log_dir),
        )
        await update.message.reply_text(fallback)
        return

    history.append({"role": "assistant", "content": llm_response})
    await update.message.reply_text(llm_response)


async def reset_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    bot_app: BotApp = app,
) -> None:
    """``/reset`` — clear conversation history."""
    user_id = update.effective_user.id
    bot_app.session.clear(user_id)
    await update.message.reply_text("對話已清空。可以由頭傾過。")


async def new_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    bot_app: BotApp = app,
) -> None:
    """``/new`` — start a fresh session."""
    user_id = update.effective_user.id
    bot_app.session.clear(user_id)
    await update.message.reply_text(
        "新 session 已開始。\n"
        "上一個話題唔會再帶入去——你可以講新嘢。"
    )


async def model_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    bot_app: BotApp = app,
) -> None:
    """``/model`` — switch LLM model via arg or inline buttons."""
    user_id = update.effective_user.id
    args = context.args
    base_url = bot_app.config.llm_base_url
    models = compatible_models(base_url)

    if args:
        ok, msg = set_user_model(
            bot_app.session.user_models, user_id, args[0].lower(), base_url
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
        return

    current = model_short_name(bot_app.session.user_models[user_id])
    rows = []
    for short in models:
        meta = MODEL_CATALOG[short]
        label = meta["label"]
        if short == current:
            label = f"✓ {label}"
        rows.append([InlineKeyboardButton(label, callback_data=f"model:{short}")])

    api_note = "opencode.ai" if current_api(base_url) == "opencode" else "NVIDIA NIM"
    await update.message.reply_text(
        f"🌙 目前模型：`{current}`\n"
        f"API：{api_note}\n\n"
        "撳下面揀模型（下一句對話生效）：",
        reply_markup=InlineKeyboardMarkup(rows),
        parse_mode="Markdown",
    )


async def model_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    bot_app: BotApp = app,
) -> None:
    """Inline button handler for model selection."""
    query = update.callback_query
    await query.answer()

    if not query.data or not query.data.startswith("model:"):
        return

    user_id = query.from_user.id
    short = query.data.split(":", 1)[1]
    ok, msg = set_user_model(
        bot_app.session.user_models,
        user_id,
        short,
        bot_app.config.llm_base_url,
    )
    await query.edit_message_text(msg, parse_mode="Markdown")


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """``/help`` — usage instructions."""
    await update.message.reply_text(
        "🌙 *指月* — 善知識 AI 陪伴\n\n"
        "直接打字同我傾偈就得。\n\n"
        "*指令：*\n"
        " /start — 重新開始（顯示聲明）\n"
        " /new — 開新 session\n"
        " /reset — 清空對話\n"
        " /help — 顯示呢個說明\n"
        " /model — 揀 AI 模型（按鈕）\n\n"
        "*你可以同我傾：*\n"
        " 壓力、煩惱、人際關係、自我懷疑、情緒低落……\n"
        " 任何困住你嘅嘢，唔使客氣。",
        parse_mode="Markdown",
    )


async def log_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    bot_app: BotApp = app,
) -> None:
    """``/log`` — show recent crisis logs (admin only)."""
    user_id = update.effective_user.id
    if user_id not in bot_app.config.admin_telegram_ids:
        await update.message.reply_text("⛔ 呢個命令只有管理員可以用。")
        return

    log_path = bot_app.crisis_log_dir / "crisis.log"
    if not log_path.exists():
        await update.message.reply_text("📋 冇危機 log — 一切正常。")
        return

    lines = log_path.read_text(encoding="utf-8").strip().split("\n")
    recent = lines[-30:] if len(lines) > 30 else lines
    await update.message.reply_text(
        f"📋 *危機 log*（最近 {len(recent)} 行，共 {len(lines)} 行）：\n\n"
        f"```\n{''.join(recent)}\n```",
        parse_mode="Markdown",
    )


async def post_init(application) -> None:
    """Register Telegram command menu."""
    await application.bot.set_my_commands(
        [
            BotCommand("start", "重新開始"),
            BotCommand("new", "開新 session"),
            BotCommand("reset", "清空對話"),
            BotCommand("model", "揀 AI 模型"),
            BotCommand("help", "說明"),
        ]
    )
