"""Canonical project paths."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system-prompt.md"
BOT_DIR = PROJECT_ROOT / "bot"
EVAL_DIR = PROJECT_ROOT / "eval"
