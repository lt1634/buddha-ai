"""Tests for bot/safety.py crisis detection and hotline helpers."""

from safety import (
    build_hotline_card,
    build_safety_fallback,
    check_output_safety,
    detect_crisis,
)


def test_crisis_suicide_keyword():
    assert detect_crisis("我想自殺")


def test_crisis_method_keyword():
    assert detect_crisis("我想跳樓")


def test_crisis_specific_plan():
    assert detect_crisis("我已經準備好方法")


def test_crisis_self_harm():
    assert detect_crisis("我諗過割自己")


def test_casual_slang_not_crisis():
    assert not detect_crisis("好攰呀想死")


def test_casual_slang_hot():
    assert not detect_crisis("熱到想死")


def test_buddha_question_not_crisis():
    assert not detect_crisis("你係咪佛陀？你有冇開悟？")


def test_gambling_not_crisis():
    assert not detect_crisis("買入球細，我好平靜")


def test_not_exist_crisis():
    assert detect_crisis("有時諗不如唔存在就好")


def test_crisis_cantonese_variants():
    assert detect_crisis("死咗就好")
    assert detect_crisis("不如死咗")
    assert detect_crisis("消失咗就好")


def test_output_safe():
    assert check_output_safety("你而家喺度，我聽到你。")


def test_output_forbidden_suicide():
    assert not check_output_safety("你講過想自殺")


def test_output_forbidden_not_exist():
    assert not check_output_safety("你話想唔存在")


def test_output_safe_normal():
    assert check_output_safety("攰到想死——我明，俾老細鬧完仲要追 deadline")


def test_hotline_card_has_24hr():
    card = build_hotline_card()
    assert "2389 2222" in card
    assert "2382 0000" in card


def test_hotline_card_youth():
    card = build_hotline_card(is_youth=True)
    assert "2382 0777" in card


def test_fallback_has_hotline():
    fb = build_safety_fallback()
    assert "2389 2222" in fb
    assert "2382 0000" in fb
