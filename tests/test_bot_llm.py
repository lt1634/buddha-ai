"""Tests for bot/llm.py helpers."""

from bot.llm import trim_history


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
