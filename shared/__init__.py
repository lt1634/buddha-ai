"""Shared utilities for buddha-ai bot and eval."""

from shared.hotlines import (
    HOTLINES,
    YOUTH_HOTLINES,
    build_hotline_card,
    build_safety_fallback,
    hotlines_for_eval_check,
)
from shared.env import load_env_file
from shared.paths import PROJECT_ROOT, PROMPTS_DIR, SYSTEM_PROMPT_PATH

__all__ = [
    "HOTLINES",
    "YOUTH_HOTLINES",
    "build_hotline_card",
    "build_safety_fallback",
    "hotlines_for_eval_check",
    "load_env_file",
    "PROJECT_ROOT",
    "PROMPTS_DIR",
    "SYSTEM_PROMPT_PATH",
]
