"""Application state wired for handlers and tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from openai import AsyncOpenAI

from bot.config import BotConfig, CRISIS_ROUNDS_LIMIT, MAX_HISTORY, load_config
from bot.llm import create_llm_client
from bot.session import SessionStore
from shared.paths import BOT_DIR


@dataclass
class BotApp:
    """Shared runtime state for Telegram command handlers."""

    config: BotConfig
    session: SessionStore
    llm_client: AsyncOpenAI
    crisis_log_dir: Path = field(default_factory=lambda: BOT_DIR / "logs")
    max_history: int = MAX_HISTORY
    crisis_rounds_limit: int = CRISIS_ROUNDS_LIMIT

    @classmethod
    def from_env(cls) -> "BotApp":
        """Build app from environment variables."""
        config = load_config()
        return cls(
            config=config,
            session=SessionStore(default_model=config.llm_model),
            llm_client=create_llm_client(config),
        )


# Lazy singleton — only initializes when first accessed (safe for CI import).
_app: BotApp | None = None


def get_app() -> BotApp:
    global _app
    if _app is None:
        _app = BotApp.from_env()
    return _app


# For backward compat: ``from bot.app import app`` still works but
# only triggers init when ``app`` is actually *used*, not on import.
class _AppProxy:
    """Proxy that delays BotApp.from_env() until first attribute access."""

    def __getattr__(self, name: str):
        return getattr(get_app(), name)


app = _AppProxy()
