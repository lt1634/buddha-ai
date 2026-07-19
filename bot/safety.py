"""
安全護欄：獨立於 LLM 嘅 regex 危機偵測層。

呢層係 code-level 防線，唔靠 prompt 信任 LLM 自己判斷。
觸發即攔截，唔交俾 LLM。
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from shared.hotlines import build_hotline_card, build_safety_fallback
from shared.paths import BOT_DIR

# Re-export for callers that import from safety.
__all__ = [
    "DECLARATION",
    "build_hotline_card",
    "build_safety_fallback",
    "check_output_safety",
    "detect_crisis",
    "log_crisis",
]

# ---- Negation context：呢類用法唔係危機意圖，唔攔截 ----
_NEGATION_CONTEXTS = [
    r"避免.*(?:自殺|死)", r"防止.*(?:自殺|死)", r"預防.*(?:自殺|死)",
    r"減少.*(?:自殺|死)", r"降低.*(?:自殺|死)",
    r"監控.*(?:心理|情緒|自殺)", r"監察.*(?:心理|情緒|自殺)",
    r"自殺傾向", r"自殺率", r"自殺新聞", r"自殺案例",
    r"關於.*自殺", r"探討.*自殺", r"討論.*自殺",
    r"教育.*(?:自殺|死)", r"認識.*(?:自殺|死)",
    r"學生.*(?:自殺|死)", r"學校.*(?:自殺|死)",
]
_NEGATION_PATTERN = re.compile("|".join(_NEGATION_CONTEXTS), re.IGNORECASE)

# ---- Crisis keywords（user input 攔截）----
CRISIS_KEYWORDS = [
    r"唔想生存", r"唔想活",
    r"了結自己", r"結束生命", r"唔存在就好",
    r"想消失咗就好", r"走咗就好",
    r"唔存在咗", r"死咗就好", r"死咗就算", r"死咗無人知",
    r"死咗唔使煩", r"死咗唔使憂", r"不如死咗",
    r"消失咗就好", r"唔喺度就好",
    r"跳樓", r"跳落街", r"割手腕", r"燒炭", r"㓤自己",
    r"食藥自殺", r"上吊", r"跳橋自盡", r"割脈",
    r"自殘", r"割自己", r"𠝹手", r"傷害自己",
    r"已經準備", r"寫好遺書", r"諗好方法", r"準備好方法",
    # 明確意圖詞 + 自殺：需要動作詞先行
    # 注意：口頭禪式「好攰想死」「熱到想死」靠 negation 或 LLM 判斷，
    # 呢度只攔截明確意圖，唔好 overscope
    r"(?:打算自殺|準備自殺|要自殺|不如死咗|想自殺)",
]

OUTPUT_FORBIDDEN = [
    r"唔存在", r"唔喺度", r"消失", r"了結", r"離開呢個世界",
    r"走咗", r"自殺",
]

_crisis_pattern = re.compile("|".join(CRISIS_KEYWORDS), re.IGNORECASE)
_output_forbidden_pattern = re.compile("|".join(OUTPUT_FORBIDDEN), re.IGNORECASE)

DEFAULT_LOG_DIR = BOT_DIR / "logs"


def detect_crisis(text: str) -> bool:
    """檢測 user message 是否包含危機關鍵字。

    優先檢查 negation context（避免/防止/監察/討論等），
    如果匹配到 negation 就放過，交俾 LLM 語境判斷。
    """
    # Negation check first — if text is about discussing/preventing suicide,
    # it's not a crisis intent.
    if _NEGATION_PATTERN.search(text):
        return False
    return bool(_crisis_pattern.search(text))


def check_output_safety(text: str) -> bool:
    """檢查 LLM 回應是否包含禁止字眼。返回 True = 安全。"""
    return not bool(_output_forbidden_pattern.search(text))


def log_crisis(
    user_id: int,
    message: str,
    response: str,
    log_dir: str | Path | None = None,
) -> None:
    """記低危機對話，供人手 review。"""
    base = Path(log_dir) if log_dir else DEFAULT_LOG_DIR
    log_path = base / "crisis.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    entry = (
        f"[{datetime.now().isoformat()}] "
        f"User {user_id}\n"
        f"  Input: {message[:200]}\n"
        f"  Response: {response[:200]}\n"
        f"  ---\n"
    )
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


DECLARATION = (
    "🌙 *指月*\n\n"
    "我係一個 AI 工具，用佛學智慧同心理學方法陪伴你面對煩惱。\n\n"
    "*我唔係佛陀，唔係開悟者，唔係出家人。*\n"
    "我只係一根「指月之指」——引導你睇自己嘅心。\n\n"
    "🆘 如果你正經歷好深嘅痛苦：\n"
    "撒瑪利亞防止自殺會 2389 2222（24小時）\n"
    "生命熱線 2382 0000（24小時）\n\n"
    "你值得被好好接住。\n\n"
    "———\n\n"
    "直接打字同我傾就得，唔使客氣。"
)
