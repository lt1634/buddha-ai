"""Shared utilities for buddha-ai (safety, hotlines, paths)."""

from shared.hotlines import (
    HOTLINES,
    YOUTH_HOTLINES,
    build_hotline_card,
    build_safety_fallback,
    hotlines_for_eval_check,
)
from shared.env import load_env_file
from shared.paths import PROJECT_ROOT, PROMPTS_DIR, SYSTEM_PROMPT_PATH, EVAL_DIR
from shared.safety import (
    DECLARATION,
    check_output_safety,
    detect_crisis,
    log_crisis,
)

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
    "EVAL_DIR",
    "DECLARATION",
    "check_output_safety",
    "detect_crisis",
    "log_crisis",
]
