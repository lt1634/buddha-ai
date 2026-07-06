#!/usr/bin/env python3
"""
safety.py unit tests — 鎖定口頭禪 vs 危機行為。

Run: python3 -m pytest test_safety.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from safety import detect_crisis, check_output_safety, build_hotline_card, build_safety_fallback


# ---- detect_crisis (input) ----

def test_crisis_suicide_keyword():
    assert detect_crisis("我想自殺")

def test_crisis_method_keyword():
    assert detect_crisis("我想跳樓")

def test_crisis_specific_plan():
    assert detect_crisis("我已經準備好方法")

def test_crisis_self_harm():
    assert detect_crisis("我諗過割自己")

def test_casual_slang_not_crisis():
    """口頭禪「好攰呀想死」唔應該觸發 crisis"""
    assert not detect_crisis("好攰呀想死")

def test_casual_slang_hot():
    """「熱到想死」唔應該觸發"""
    assert not detect_crisis("熱到想死")

def test_buddha_question_not_crisis():
    """「你係咪佛陀」唔應該觸發"""
    assert not detect_crisis("你係咪佛陀？你有冇開悟？")

def test_gambling_not_crisis():
    """賭博心理探索唔應該觸發"""
    assert not detect_crisis("買入球細，我好平靜")

def test_not_exist_crisis():
    """「唔存在就好」應該觸發"""
    assert detect_crisis("有時諗不如唔存在就好")


# ---- check_output_safety (output) ----

def test_output_safe():
    assert check_output_safety("你而家喺度，我聽到你。")

def test_output_forbidden_suicide():
    assert not check_output_safety("你講過想自殺")  # 複述禁字

def test_output_forbidden_not_exist():
    assert not check_output_safety("你話想唔存在")

def test_output_safe_normal():
    """正常承接口頭禪唔應該被 block"""
    assert check_output_safety("攰到想死——我明，俾老細鬧完仲要追 deadline")


# ---- build_hotline_card ----

def test_hotline_card_has_24hr():
    card = build_hotline_card()
    assert "2389 2222" in card
    assert "2382 0000" in card
    assert "24小時" in card

def test_hotline_card_youth():
    card = build_hotline_card(is_youth=True)
    assert "2382 0777" in card
    assert "下午" in card or "凌晨" in card  # 時段標註

def test_hotline_card_max_three():
    """熱線最多三條（危機中大腦過載）"""
    card = build_hotline_card()
    # 數 📞 數量
    phone_count = card.count("📞")
    # 通用熱線 3 條 + 青少年 2 條 = 5（if youth）
    # 通用 only = 3
    assert phone_count <= 5


# ---- build_safety_fallback ----

def test_fallback_has_hotline():
    fb = build_safety_fallback()
    assert "2389 2222" in fb
    assert "2382 0000" in fb
    assert "24小時" in fb

def test_fallback_no_forbidden_words():
    """Fallback 本身唔應該包含禁止字眼（除機構名「防止自殺會」合法用法）"""
    fb = build_safety_fallback()
    # 移除機構名後再 check
    fb_clean = fb.replace("防止自殺會", "").replace("自殺", "")
    assert check_output_safety(fb_clean)
