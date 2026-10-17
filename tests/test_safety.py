"""Tests for shared/safety.py crisis detection and hotline helpers."""

from shared.safety import (
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
    assert detect_crisis("我已經準備好自殺方法")


def test_generic_preparation_is_not_crisis():
    assert not detect_crisis("我已經準備好明日嘅考試")
    assert not detect_crisis("我諗好方法同父母溝通")


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


# ---------------------------------------------------------------------------
# 2026-10-08 regression — audit 拆出嚟嘅三個 critical 漏洞
# ---------------------------------------------------------------------------


def test_c1_first_person_cantonese_intent():
    """C1：「我想死」係廣東話最常用講法，原本完全冇觸發。"""
    assert detect_crisis("我想死")
    assert detect_crisis("我好想死")
    assert detect_crisis("我真係想死")
    assert detect_crisis("想死就算")
    assert detect_crisis("不如死")


def test_c2_student_in_crisis_is_not_suppressed():
    """C2：原本 學生.*死 會吞埋第一人稱危機句，令學生拎唔到熱線。"""
    assert detect_crisis("我係學生，我想死")
    assert detect_crisis("學校啲人鬧我，我想死")
    assert detect_crisis("我係學校學生，我諗過自盡")


def test_c2_negation_still_passes_discussion():
    """收窄後，自殺率/新聞/案例等討論語境仍然放過。"""
    assert not detect_crisis("學生自殺率上升")
    assert not detect_crisis("學校自殺新聞")
    assert not detect_crisis("討論學生自殺案例")
    assert not detect_crisis("避免學生自殺")


def test_c3_method_vocabulary():
    """C3：原本只得 跳樓/跳落街/割手腕，漏晒最常用講法。"""
    assert detect_crisis("我想割腕")
    assert detect_crisis("我想跳落去")
    assert detect_crisis("我想跳落海")
    assert detect_crisis("我想吞藥")
    assert detect_crisis("我想自盡")
    assert detect_crisis("有輕生念頭")


def test_c3_english_coverage():
    """香港學生會中英夾雜，原本英文零覆蓋。"""
    assert detect_crisis("I want to kill myself")
    assert detect_crisis("I want to die")
    assert detect_crisis("I'm gonna end my life")
    assert detect_crisis("I've been having suicidal thoughts")


def test_colloquial_still_not_crisis():
    """C1 修正唔可以破壞已鎖死嘅口頭禪行為。"""
    assert not detect_crisis("好攰呀想死")
    assert not detect_crisis("熱到想死")
    assert not detect_crisis("忙到想死")
    assert not detect_crisis("我今日好攰，想死")


def test_h2_hotline_reply_is_not_blocked():
    """H2：LLM 正確覆熱線會講到「自殺」，原本被自己嘅 gate 打掉。"""
    assert check_output_safety(
        "如果你需要，可以打撒瑪利亞防止自殺會 2389 2222（24小時）。"
    )
    assert check_output_safety(
        "生命熱線 2382 0000，同青協關心一線 2777 8899 都幫到你。"
    )


def test_h2_non_hotline_forbidden_still_blocked():
    """熱線放行唔可以放走真正嘅禁止字眼。"""
    assert not check_output_safety("你講過想自殺")
    assert not check_output_safety("你想唔存在")
