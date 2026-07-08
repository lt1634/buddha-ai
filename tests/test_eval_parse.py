"""Tests for eval/run.py pure functions."""

import json

import run as eval_run


SAMPLE_RUBRICS = [
    {"id": "tone", "type": "scalar", "weight": 1},
    {
        "id": "safety_trigger",
        "type": "composite",
        "weight": 2,
        "sub_dimensions": [
            {"id": "triage"},
            {"id": "no_new_harm"},
        ],
    },
]


def test_is_multi_turn():
    assert eval_run.is_multi_turn({"turns": [{"user": "hi"}]})
    assert not eval_run.is_multi_turn({"input": "hi"})


def test_last_user_turn():
    case = {
        "turns": [
            {"user": "first"},
            {"assistant": "ok"},
            {"user": "second"},
        ]
    }
    assert eval_run.last_user_turn(case) == "second"


def test_parse_full_judge_output_plain_json():
    raw = json.dumps(
        {
            "tone": {"score": 4, "reason": "ok"},
            "safety_trigger": {
                "sub_scores": {"triage": 5, "no_new_harm": 4},
                "reasons": {"triage": "good"},
            },
        }
    )
    result = eval_run.parse_full_judge_output(raw, SAMPLE_RUBRICS)
    assert result["tone"]["score"] == 4
    assert result["safety_trigger"]["score"] == 4


def test_parse_full_judge_output_fenced_json():
    raw = 'Here is JSON:\n```json\n{"tone": {"score": 3, "reason": "fine"}}\n```'
    result = eval_run.parse_full_judge_output(raw, [{"id": "tone", "type": "scalar"}])
    assert result["tone"]["score"] == 3


def test_parse_full_judge_output_missing_rubric():
    raw = json.dumps({"tone": {"score": 4, "reason": "ok"}})
    result = eval_run.parse_full_judge_output(raw, SAMPLE_RUBRICS)
    assert result["tone"]["score"] == 4
    assert result["safety_trigger"]["score"] == 0
    assert "missing" in result["safety_trigger"]["reason"]


def test_deterministic_hotline_crisis_pass():
    case = {"metadata": {"severity": "crisis"}}
    response = "請打撒瑪利亞防止自殺會 2389 2222，24小時"
    out = eval_run.deterministic_hotline_check(response, case)
    assert out["pass"] is True
    assert out["found_24hr"] is True


def test_deterministic_hotline_crisis_fail():
    case = {"metadata": {"severity": "crisis"}}
    out = eval_run.deterministic_hotline_check("我聽到你。", case)
    assert out["pass"] is False
    assert any("24hr" in issue for issue in out["issues"])


def test_deterministic_hotline_youth_needs_hours():
    case = {"metadata": {"severity": "moderate"}}
    response = "可以打 2382 0777"
    out = eval_run.deterministic_hotline_check(response, case)
    assert out["pass"] is False


def test_build_rubric_spec_includes_ids():
    spec = eval_run.build_rubric_spec(SAMPLE_RUBRICS)
    assert "tone" in spec
    assert "safety_trigger" in spec
    assert "composite" in spec


def test_format_rubric_detail_skips_zero():
    lines = eval_run.format_rubric_detail(
        {"tone": {"score": 0}, "warmth": {"score": 4, "reason": "good"}}
    )
    text = "\n".join(lines)
    assert "tone" not in text
    assert "warmth" in text
