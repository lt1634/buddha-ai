"""LLM client and prompt loading."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from openai import AsyncOpenAI

from bot.config import BotConfig


def load_system_prompt(path: Path) -> str:
    """Read the system prompt markdown file."""
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "你是一位善知識，用佛學智慧同心理學方法陪伴使用者。"


def create_llm_client(config: BotConfig) -> AsyncOpenAI:
    """Build an async OpenAI-compatible client from *config*."""
    return AsyncOpenAI(
        api_key=config.llm_api_key,
        base_url=config.llm_base_url,
    )


async def call_llm(
    client: AsyncOpenAI,
    messages: list[dict[str, str]],
    *,
    model: str,
    max_tokens: int,
) -> str:
    """Call the LLM API and return response text."""
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason

        if not content and finish_reason == "length":
            return "（系統提示：回應被截斷，請再試一次。）"

        return content or "……"
    except Exception as exc:
        print(f"LLM Error: {exc}")
        return "我而家聽唔到你，可以再講多一次嗎？"


def trim_history(
    history: list[dict[str, str]],
    *,
    max_history: int,
) -> list[dict[str, str]]:
    """Keep system prompt plus the most recent *max_history* user/assistant turns."""
    if len(history) <= max_history * 2 + 1:
        return history
    return [history[0]] + history[-(max_history * 2) :]
