#!/usr/bin/env python3
"""
指月 — 善知識 Telegram Bot

Usage:
    cp .env.example .env  # 填入 BOT_TOKEN
    pip3 install -r requirements.txt
    python3 bot.py
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

# Allow running as ``python3 bot/bot.py`` from repo root.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram import Update

from bot.app import app
from bot.handlers import (
    handle_message,
    help_command,
    log_command,
    model_callback,
    model_command,
    new_command,
    post_init,
    reset_command,
    start_command,
)


async def on_error(update: Any, context: Any) -> None:
    """任何 handler exception 都唔可以令用戶收唔到回覆。

    2026-10-08 加：err log 有 773 條「No error handlers are registered」，
    即係之前任何 NetworkError/TelegramBadRequest 都會令 handler 死咗，
    用戶（包括危機用戶）收到完全沉默 —— 呢個係最壞嘅失敗模式。
    """
    logging.getLogger(__name__).error("Unhandled exception", exc_info=context.error)
    if update is None:
        return
    try:
        message = getattr(update, "effective_message", None) or getattr(
            update, "message", None
        )
        if message is not None:
            await message.reply_text(
                "唔好意思，我出咗啲問題，暫時回應唔到你。\n\n"
                "如果你而家好辛苦，請打撒瑪利亞防止自殺會 2389 2222（24小時），"
                "或生命熱線 2382 0000（24小時）。"
            )
    except Exception:
        logging.getLogger(__name__).exception("Fallback reply failed")


def main() -> None:
    if not app.config.bot_token:
        print("❌ 請先設定 BOT_TOKEN（參考 .env.example）")
        print("   1. 打開 Telegram，搵 @BotFather")
        print("   2. 發 /newbot")
        print("   3. 攞到 token，填入 .env")
        # 2026-10-08：launchd plist 係 KeepAlive.SuccessfulExit=false，
        # exit 0 = 「成功退出」= launchd 唔會重啟。改做 exit 1 先等得到拉返起。
        raise SystemExit(1)

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.INFO)

    print("🌙 指月 bot 啟動中…")
    print(f"   Model: {app.config.llm_model}")
    print(f"   API:   {app.config.llm_base_url}")

    application = (
        Application.builder()
        .token(app.config.bot_token)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("new", new_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("model", model_command))
    application.add_handler(CallbackQueryHandler(model_callback, pattern=r"^model:"))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("log", log_command))
    application.add_error_handler(on_error)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Bot 已啟動，按 Ctrl+C 停止")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
