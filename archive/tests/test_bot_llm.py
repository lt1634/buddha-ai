"""Tests for bot/llm.py helpers."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from bot.llm import call_llm, trim_history, truncate_response


def test_trim_history_keeps_system_and_recent():
    history = [{"role": "system", "content": "sys"}]
    for i in range(30):
        history.append({"role": "user", "content": f"u{i}"})
        history.append({"role": "assistant", "content": f"a{i}"})

    trimmed = trim_history(history, max_history=5)
    assert trimmed[0]["role"] == "system"
    assert len(trimmed) == 1 + 5 * 2
    assert trimmed[-1]["content"] == "a29"


def test_trim_history_noop_when_short():
    history = [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "hi"},
    ]
    assert trim_history(history, max_history=20) == history


def test_truncate_response_preserves_configured_limit():
    assert truncate_response("abcdef", 5) == "abcd…"
    assert truncate_response("abcdef", 1) == "…"
    assert truncate_response("abcdef", 0) == ""


@pytest.mark.asyncio
async def test_call_llm_enforces_limit_after_retries_are_exhausted():
    long_response = "字" * 501
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content=long_response),
                finish_reason="stop",
            )
        ]
    )
    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=response)

    content = await call_llm(
        client,
        [{"role": "system", "content": "sys"}, {"role": "user", "content": "hi"}],
        model="test-model",
        max_tokens=100,
        max_chars=500,
        max_retries=2,
    )

    assert len(content) == 500
    assert content.endswith("…")
    assert client.chat.completions.create.await_count == 3
