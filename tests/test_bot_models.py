"""Tests for bot/models.py."""

from bot.models import (
    MODEL_CATALOG,
    compatible_models,
    current_api,
    model_short_name,
    set_user_model,
)


def test_current_api_opencode():
    assert current_api("https://opencode.ai/zen/go/v1") == "opencode"


def test_current_api_nvidia():
    assert current_api("https://integrate.api.nvidia.com/v1") == "nvidia"


def test_compatible_models_opencode():
    models = compatible_models("https://opencode.ai/zen/go/v1")
    assert "mimo" in models
    assert "glm" in models
    assert "maverick" not in models


def test_compatible_models_nvidia():
    models = compatible_models("https://integrate.api.nvidia.com/v1")
    assert "maverick" in models
    assert "mimo" not in models


def test_model_short_name():
    assert model_short_name("mimo-v2.5") == "mimo"


def test_set_user_model_success():
    user_models: dict[int, str] = {}
    ok, msg = set_user_model(user_models, 1, "mimo", "https://opencode.ai/zen/go/v1")
    assert ok
    assert user_models[1] == MODEL_CATALOG["mimo"]["id"]
    assert "Mimo" in msg


def test_set_user_model_unknown():
    user_models: dict[int, str] = {}
    ok, msg = set_user_model(user_models, 1, "unknown", "https://opencode.ai/zen/go/v1")
    assert not ok
    assert "唔認識" in msg
