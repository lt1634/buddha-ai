"""LLM model catalog and selection helpers."""

from __future__ import annotations

from typing import TypedDict


class ModelMeta(TypedDict):
    id: str
    api: str
    label: str


MODEL_CATALOG: dict[str, ModelMeta] = {
    "mimo": {"id": "mimo-v2.5", "api": "opencode", "label": "Mimo 2.5（預設）"},
    "glm": {"id": "glm-5.2", "api": "opencode", "label": "GLM 5.2"},
    "maverick": {
        "id": "meta/llama-4-maverick-17b-128e-instruct",
        "api": "nvidia",
        "label": "Llama Maverick",
    },
    "qwen": {"id": "qwen/qwen3.5-397b-a17b", "api": "nvidia", "label": "Qwen 3.5"},
}

DEFAULT_MODEL_KEY = "mimo"


def current_api(base_url: str) -> str:
    """Return ``opencode`` or ``nvidia`` based on the API base URL."""
    if "nvidia" in base_url.lower():
        return "nvidia"
    return "opencode"


def compatible_models(base_url: str) -> dict[str, str]:
    """Short name → full model id for models available on *base_url*."""
    api = current_api(base_url)
    return {
        short: meta["id"]
        for short, meta in MODEL_CATALOG.items()
        if meta["api"] == api
    }


def model_short_name(full_name: str) -> str:
    """Map a full model id back to its catalog short name."""
    for short, meta in MODEL_CATALOG.items():
        if meta["id"] == full_name:
            return short
    return full_name.split("/")[-1]


def set_user_model(
    user_models: dict[int, str],
    user_id: int,
    short: str,
    base_url: str,
) -> tuple[bool, str]:
    """Set a user's model choice. Returns ``(success, message)``."""
    models = compatible_models(base_url)
    if short not in models:
        available = ", ".join(models.keys())
        return False, f"❌ 唔認識 `{short}`。可用：{available}"
    user_models[user_id] = models[short]
    label = MODEL_CATALOG[short]["label"]
    return True, f"✅ 已切換到 *{label}*（`{short}`）"
