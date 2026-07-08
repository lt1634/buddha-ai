"""Bot configuration from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from shared.paths import SYSTEM_PROMPT_PATH

load_dotenv()

MAX_HISTORY = 20
CRISIS_ROUNDS_LIMIT = 3


@dataclass(frozen=True)
class BotConfig:
    """Runtime configuration for the Telegram bot."""

    bot_token: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    llm_max_tokens: int
    admin_telegram_ids: tuple[int, ...]
    system_prompt_path: str = str(SYSTEM_PROMPT_PATH)


def _parse_admin_ids(raw: str) -> tuple[int, ...]:
    ids: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            ids.append(int(part))
    return tuple(ids)


def load_config() -> BotConfig:
    """Load bot config from environment (with sensible defaults)."""
    return BotConfig(
        bot_token=os.getenv("BOT_TOKEN", ""),
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        llm_base_url=os.getenv("LLM_BASE_URL", "https://opencode.ai/zen/go/v1"),
        llm_model=os.getenv("LLM_MODEL", "mimo-v2.5"),
        llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "4000")),
        admin_telegram_ids=_parse_admin_ids(os.getenv("ADMIN_TELEGRAM_IDS", "")),
    )
