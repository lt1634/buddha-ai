"""Single source of truth for crisis hotline data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Hotline:
    """A support hotline entry."""

    name: str
    number: str
    hours: str
    is_24hr: bool
    youth_only: bool = False


HOTLINES: tuple[Hotline, ...] = (
    Hotline("撒瑪利亞防止自殺會", "2389 2222", "24小時", True),
    Hotline("生命熱線", "2382 0000", "24小時", True),
    Hotline("情緒通（政府精神健康支援）", "18111", "24小時，WhatsApp都得", True),
)

YOUTH_HOTLINES: tuple[Hotline, ...] = (
    Hotline(
        "生命熱線 青少年專線",
        "2382 0777",
        "下午2時至凌晨2時（24歲以下）",
        False,
        youth_only=True,
    ),
    Hotline(
        "青協 關心一線",
        "2777 8899",
        "一至六 下午2時至凌晨2時（6-24歲）",
        False,
        youth_only=True,
    ),
)

# Extra entries used only by eval deterministic checks.
EVAL_EXTRA_HOTLINES: tuple[Hotline, ...] = (
    Hotline("Open噏", "openup.hk", "24小時", True),
)


def _format_lines(hotlines: Iterable[Hotline]) -> list[str]:
    return [f"📞 {h.name}：{h.number}（{h.hours}）" for h in hotlines]


def build_hotline_card(*, is_youth: bool = False) -> str:
    """Build the crisis hotline card shown to users."""
    lines = ["🆘 如果你而家好辛苦，請搵真人陪你：", ""]
    lines.extend(_format_lines(HOTLINES))
    if is_youth:
        lines.extend(["", "🌙 如果你係學生，仲可以搵："])
        lines.extend(_format_lines(YOUTH_HOTLINES))
    lines.extend(["", "你值得被好好接住。我喺度，但你需要嘅係真人。"])
    return "\n".join(lines)


def build_safety_fallback() -> str:
    """Fallback message when LLM output is blocked."""
    return (
        "我聽到你。你而家嘅感受好真實。\n\n"
        "我係 AI，唔能夠取代真人嘅陪伴。\n\n"
        "如果你好辛苦，請打：\n"
        "撒瑪利亞防止自殺會 2389 2222（24小時）\n"
        "生命熱線 2382 0000（24小時）\n\n"
        "你值得被好好接住。"
    )


def hotlines_for_eval_check() -> list[dict[str, object]]:
    """Dict rows compatible with ``eval.run.deterministic_hotline_check``."""
    all_lines = (*HOTLINES, *YOUTH_HOTLINES, *EVAL_EXTRA_HOTLINES)
    return [
        {
            "name": h.name,
            "number": h.number,
            "is_24hr": h.is_24hr,
        }
        for h in all_lines
    ]
