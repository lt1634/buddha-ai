"""Tests for Telegram handlers (mocked Update/Context)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from bot.app import BotApp
from bot.config import BotConfig
from bot.handlers import (
    help_command,
    log_command,
    new_command,
    reset_command,
    start_command,
)
from bot.session import SessionStore


def _make_update(user_id: int = 100, text: str = "") -> MagicMock:
    update = MagicMock()
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()
    update.message.text = text
    return update


def _make_context(args: list[str] | None = None) -> MagicMock:
    context = MagicMock()
    context.args = args or []
    return context


@pytest.fixture
def bot_app(tmp_path: Path) -> BotApp:
    config = BotConfig(
        bot_token="test-token",
        llm_api_key="test-key",
        llm_base_url="https://opencode.ai/zen/go/v1",
        llm_model="mimo-v2.5",
        llm_max_tokens=1000,
        admin_telegram_ids=(100,),
    )
    return BotApp(
        config=config,
        session=SessionStore(default_model="mimo-v2.5"),
        llm_client=MagicMock(),
        crisis_log_dir=tmp_path / "logs",
    )


@pytest.mark.asyncio
async def test_start_clears_session(bot_app: BotApp):
    bot_app.session.conversations[42] = [{"role": "user", "content": "old"}]
    bot_app.session.crisis_rounds[42] = 2

    update = _make_update(42)
    await start_command(update, _make_context(), bot_app=bot_app)

    assert bot_app.session.conversations[42] == []
    assert bot_app.session.crisis_rounds[42] == 0
    update.message.reply_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_reset_and_new_clear_history(bot_app: BotApp):
    bot_app.session.conversations[7] = [{"role": "user", "content": "x"}]

    await reset_command(_make_update(7), _make_context(), bot_app=bot_app)
    assert bot_app.session.conversations[7] == []

    bot_app.session.conversations[7] = [{"role": "user", "content": "y"}]
    await new_command(_make_update(7), _make_context(), bot_app=bot_app)
    assert bot_app.session.conversations[7] == []


@pytest.mark.asyncio
async def test_help_replies(bot_app: BotApp):
    update = _make_update(1)
    await help_command(update, _make_context())
    update.message.reply_text.assert_awaited_once()
    body = update.message.reply_text.await_args.args[0]
    assert "/model" in body


@pytest.mark.asyncio
async def test_log_admin_only(bot_app: BotApp):
    update = _make_update(999)
    await log_command(update, _make_context(), bot_app=bot_app)
    update.message.reply_text.assert_awaited_once()
    assert "管理員" in update.message.reply_text.await_args.args[0]


@pytest.mark.asyncio
async def test_log_admin_reads_file(bot_app: BotApp, tmp_path: Path):
    log_dir = bot_app.crisis_log_dir
    log_dir.mkdir(parents=True)
    (log_dir / "crisis.log").write_text("line1\nline2\n", encoding="utf-8")

    update = _make_update(100)
    await log_command(update, _make_context(), bot_app=bot_app)
    body = update.message.reply_text.await_args.args[0]
    assert "line2" in body
