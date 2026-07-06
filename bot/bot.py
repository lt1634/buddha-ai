#!/usr/bin/env python3
"""
指月 — 善知識 Telegram Bot

一個用佛學智慧同心理學方法陪伴人嘅 AI 對話 bot。
Project: buddha-ai/bot/（repo 根目錄下）

Usage:
    cp .env.example .env  # 填入 BOT_TOKEN
    pip3 install -r requirements.txt
    python3 bot.py
"""

from __future__ import annotations

import os
import asyncio
from typing import Optional
from pathlib import Path
from collections import defaultdict

from dotenv import load_dotenv
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from safety import (
    detect_crisis,
    check_output_safety,
    build_hotline_card,
    build_safety_fallback,
    log_crisis,
    DECLARATION,
)

# ---- Config ----
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://opencode.ai/zen/go/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "mimo-v2.5")
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4000"))

SYSTEM_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system-prompt.md"
MAX_HISTORY = 20  # 每個用戶保留最近 20 輪對話
CRISIS_ROUNDS_LIMIT = 3  # 危機對話最多 3 輪，之後彈熱線 + 結束

# 可用 models
AVAILABLE_MODELS = {
    "mimo": "mimo-v2.5",
    "glm": "glm-5.2",
    "maverick": "meta/llama-4-maverick-17b-128e-instruct",
    "qwen": "qwen/qwen3.5-397b-a17b",
}
DEFAULT_MODEL_KEY = "mimo"

# ---- LLM Client ----
llm_client = AsyncOpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
)

# ---- 對話歷史（in-memory，重啟即清）----
# {user_id: [{"role": "system"|"user"|"assistant", "content": "..."}]}
conversations: dict[int, list[dict]] = defaultdict(list)

# 危機輪數計數 {user_id: int}
crisis_rounds: dict[int, int] = defaultdict(int)

# 每用戶 model 選擇 {user_id: model_name}
user_models: dict[int, str] = defaultdict(lambda: LLM_MODEL)


def load_system_prompt() -> str:
    """讀取 system prompt。"""
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    return "你是一位善知識，用佛學智慧同心理學方法陪伴使用者。"


async def call_llm(messages: list[dict], model: Optional[str] = None) -> str:
    """調用 LLM API，返回回應文字。"""
    try:
        response = await llm_client.chat.completions.create(
            model=model or LLM_MODEL,
            messages=messages,
            max_tokens=LLM_MAX_TOKENS,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason

        # reasoning model 可能因 max_tokens 不足而空回應
        if not content and finish_reason == "length":
            return "（系統提示：回應被截斷，請再試一次。）"

        return content or "……"
    except Exception as e:
        print(f"LLM Error: {e}")
        return "我而家聽唔到你，可以再講多一次嗎？"


def model_short_name(full_name: str) -> str:
    """將 full model name 轉做短名。"""
    for short, full in AVAILABLE_MODELS.items():
        if full == full_name:
            return short
    return full_name.split("/")[-1]


# ---- Telegram Handlers ----


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /start — 出指月聲明 """
    user_id = update.effective_user.id
    conversations[user_id] = []  # 重置對話
    crisis_rounds[user_id] = 0
    await update.message.reply_text(DECLARATION, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """主訊息 handler — 安全檢查 → LLM → 安全檢查 → 回覆"""
    user = update.effective_user
    user_id = user.id
    user_text = update.message.text

    if not user_text:
        return

    # ---- 1. 安全 regex 層（input）----
    if detect_crisis(user_text):
        crisis_rounds[user_id] += 1
        round_num = crisis_rounds[user_id]

        # 判斷是否青少年（簡單 keyword heuristic）
        youth_keywords = ["學校", "DSE", "考試", "阿爸阿媽", "中學", "功課", "老師"]
        is_youth = any(kw in user_text for kw in youth_keywords)

        hotline_card = build_hotline_card(is_youth=is_youth)

        # log 危機
        log_crisis(user_id, user_text, hotline_card)

        await update.message.reply_text(
            "我聽到你。你而家嘅感受好真實。\n\n"
            "我係 AI，唔能夠取代真人嘅陪伴。\n\n"
            + hotline_card
        )

        # 三輪上限：第三輪彈熱線 + 結束對話
        if round_num >= CRISIS_ROUNDS_LIMIT:
            await update.message.reply_text(
                "我陪你到呢度。你而家最需要嘅唔係我，係真人。\n\n"
                "請打 2389 2222，佢哋 24 小時喺度。"
            )
            conversations[user_id] = []  # 清空對話
            crisis_rounds[user_id] = 0
        return

    # ---- 2. 準備對話歷史 ----
    history = conversations[user_id]

    # 如果係新對話，加入 system prompt
    if not history:
        system_prompt = load_system_prompt()
        history.append({"role": "system", "content": system_prompt})

    # 加入用戶訊息
    history.append({"role": "user", "content": user_text})

    # 限制歷史長度（保留 system prompt + 最近 N 輪）
    if len(history) > MAX_HISTORY * 2 + 1:
        history = [history[0]] + history[-(MAX_HISTORY * 2):]
        conversations[user_id] = history

    # ---- 3. 調用 LLM ----
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    llm_response = await call_llm(history, model=user_models[user_id])

    # ---- 4. 安全 regex 層（output）— 只在 crisis context 啟用 ----
    # 正常對話（含口頭禪）唔檢查 output，避免誤殺 LLM 引用用戶字眼
    # 只有當對話正處於 crisis 輪數時先啟用嚴格禁字
    if crisis_rounds[user_id] > 0 and not check_output_safety(llm_response):
        # LLM 回應包含禁止字眼 → fallback
        fallback = build_safety_fallback()
        log_crisis(user_id, user_text, f"[OUTPUT BLOCKED] {llm_response[:100]}")
        await update.message.reply_text(fallback)
        return

    # ---- 5. 回覆 + 存歷史 ----
    history.append({"role": "assistant", "content": llm_response})
    await update.message.reply_text(llm_response)


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /reset — 清空對話歷史 """
    user_id = update.effective_user.id
    conversations[user_id] = []
    crisis_rounds[user_id] = 0
    await update.message.reply_text("對話已清空。可以由頭傾過。")


async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /model — 切換 LLM 模型 """
    user_id = update.effective_user.id
    args = context.args

    if not args:
        # 顯示當前 model + 可選 list
        current = model_short_name(user_models[user_id])
        lines = [f"🌙 目前模型：`{current}`", "", "可用模型："]
        for short, full in AVAILABLE_MODELS.items():
            marker = " ←" if full == user_models[user_id] else ""
            lines.append(f"  /model {short}{marker}")
        lines.append("\n切換後下一句對話生效。")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    choice = args[0].lower()
    if choice not in AVAILABLE_MODELS:
        await update.message.reply_text(
            f"❌ 唔認識 `{choice}`。可用：{', '.join(AVAILABLE_MODELS.keys())}",
            parse_mode="Markdown",
        )
        return

    user_models[user_id] = AVAILABLE_MODELS[choice]
    await update.message.reply_text(f"✅ 已切換到 `{choice}`", parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /help — 使用說明 """
    await update.message.reply_text(
        "🌙 *指月* — 善知識 AI 陪伴\n\n"
        "直接打字同我傾偈就得。\n\n"
        "*指令：*\n"
        " /start — 重新開始\n"
        " /reset — 清空對話\n"
        " /help — 顯示呢個說明\n"
        " /model — 切換 AI 模型\n\n"
        "*你可以同我傾：*\n"
        " 壓力、煩惱、人際關係、自我懷疑、情緒低落……\n"
        " 任何困住你嘅嘢，唔使客氣。",
        parse_mode="Markdown",
    )


async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /log — 查看最近危機 log（僅限 admin）"""
    user_id = update.effective_user.id
    # 只限 Tim 查看
    admin_ids = [8527502358]  # Tim 嘅 Telegram user ID
    if user_id not in admin_ids:
        await update.message.reply_text("⛔ 呢個命令只有管理員可以用。")
        return

    log_path = Path(__file__).parent / "logs" / "crisis.log"
    if not log_path.exists():
        await update.message.reply_text("📋 冇危機 log — 一切正常。")
        return

    lines = log_path.read_text(encoding="utf-8").strip().split("\n")
    # 顯示最近 10 條
    recent = lines[-30:] if len(lines) > 30 else lines
    await update.message.reply_text(
        f"📋 *危機 log*（最近 {len(recent)} 行，共 {len(lines)} 行）：\n\n"
        f"```\n{''.join(recent)}\n```",
        parse_mode="Markdown",
    )


# ---- Main ----


def main() -> None:
    if not BOT_TOKEN:
        print("❌ 請先設定 BOT_TOKEN（參考 .env.example）")
        print("   1. 打開 Telegram，搵 @BotFather")
        print("   2. 發 /newbot")
        print("   3. 攞到 token，填入 .env")
        return

    import logging
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO,
    )
    # telegram 同 httpcore 嘅 DEBUG 太嘈，淨係睇 INFO+
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.INFO)

    print(f"🌙 指月 bot 啟動中…")
    print(f"   Model: {LLM_MODEL}")
    print(f"   API:   {LLM_BASE_URL}")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("model", model_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("log", log_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Bot 已啟動，按 Ctrl+C 停止")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
