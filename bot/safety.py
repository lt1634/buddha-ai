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
    # 2026-10-08 修正：原本係 r"學生.*(?:自殺|死)" / r"學校.*(?:自殺|死)"，
    # 但 .* 會吞埋第一人稱危機句（「我係學生，我想死」被放過）。
    # 改成要求 topic 名詞緊接自殺，學生自殺新聞/案例/率仍然放過。
    r"學生自殺(?:率|傾向|新聞|案例|個案|問題)",
    r"學校自殺(?:率|傾向|新聞|案例|個案|問題)",
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
    r"(?:寫好|寫咗|寫了)遺書",
    r"(?:已經|我已|我都)?準備(?:好)?(?:自殺|輕生|跳樓|割腕|燒炭|上吊|遺書)",
    r"諗好(?:自殺|輕生|死)",
    r"準備好(?:自殺|輕生|死)",
    # 明確意圖詞 + 自殺：需要動作詞先行
    # 注意：口頭禪式「好攰想死」「熱到想死」靠 negation 或 LLM 判斷，
    # 呢度只攔截明確意圖，唔好 overscope
    r"(?:打算自殺|準備自殺|要自殺|不如死咗|想自殺)",
    # ---- 2026-10-08 補漏（audit 發現）----
    # C1：第一人稱意圖。原本成個 CRISIS_KEYWORDS 冇「我想死」——
    # 係廣東話最常用嘅講法，一直冇觸發過危機層。
    # 加「我」做錨，「熱到想死」「好攰呀想死」冇「我」喺前面，仍然唔會誤觸。
    r"我想死", r"我.{0,4}想死", r"想死就算", r"不如死",
    # C3：方法／意圖詞彙。原本只得 跳樓/跳落街/割手腕，
    # 割腕（冇手）、跳落去/跳落海、吞藥、自盡、輕生念頭全部冇。
    # 沿用既有設計：方法詞單獨攔（燒炭/上吊/割脈本身都係單獨攔）。
    r"割腕", r"跳落(?:去|海|河)", r"墮樓", r"跳天台",
    r"吞藥", r"食安眠藥", r"自盡", r"輕生念頭", r"尋死", r"揾死",
    # 香港學生會中英夾雜，英文零覆蓋
    r"kill myself", r"want to die", r"wanna die", r"end my life",
    r"suicid", r"cut myself", r"harm myself", r"hang myself",
]

OUTPUT_FORBIDDEN = [
    r"唔存在", r"唔喺度", r"消失", r"了結", r"離開呢個世界",
    r"走咗", r"自殺",
]

_crisis_pattern = re.compile("|".join(CRISIS_KEYWORDS), re.IGNORECASE)
_output_forbidden_pattern = re.compile("|".join(OUTPUT_FORBIDDEN), re.IGNORECASE)

# 已知熱線號碼。回應入面有呢啲號碼 = 提供資源，唔係重複傷害。
_HOTLINE_NUMBER = re.compile(r"2389\s*2222|2382\s*0000|2382\s*0777|2777\s*8899|18111")

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
    """檢查 LLM 回應是否包含禁止字眼。返回 True = 安全。

    2026-10-08 修正：OUTPUT_FORBIDDEN 包含「自殺」，但 system prompt
    明確要求 LLM 喺危機時提供熱線號碼 —— 嗰句一定會講到「自殺」。
    原本會將正確嘅熱線回應打掉換做 fallback，用戶反而拎唔到資源。
    修正：回應入面有已知熱線號碼 → 當佢係提供資源，放行。
    """
    if _HOTLINE_NUMBER.search(text):
        return True
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
