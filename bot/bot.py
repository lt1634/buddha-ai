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


def main() -> None:
    if not app.config.bot_token:
        print("❌ 請先設定 BOT_TOKEN（參考 .env.example）")
        print("   1. 打開 Telegram，搵 @BotFather")
        print("   2. 發 /newbot")
        print("   3. 攞到 token，填入 .env")
        return

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
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Bot 已啟動，按 Ctrl+C 停止")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
