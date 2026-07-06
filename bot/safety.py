"""
安全護欄：獨立於 LLM 嘅 regex 危機偵測層。

呢層係 code-level 防線，唔靠 prompt 信任 LLM 自己判斷。
觸發即攔截，唔交俾 LLM。
"""

import re
from datetime import datetime
from pathlib import Path

# ---- 危機關鍵字（user input 攔截）----
# 注意：呢層只攔截「明確」嘅危機信號。
# 廣東話口頭禪（「好攰想死」「熱到想死」）應該交俾 LLM 用語境判斷，
# 唔好喺 regex 層一刀切彈熱線。
CRISIS_KEYWORDS = [
    # 明確自殺意念（唔係口頭禪）
    r"自殺", r"唔想生存", r"唔想活",
    r"了結自己", r"結束生命", r"唔存在就好",
    r"想消失咗就好", r"走咗就好",
    # 具體方法
    r"跳樓", r"跳落街", r"割手腕", r"燒炭", r"㓤自己",
    # 自殘
    r"自殘", r"割自己", r"𠝹手", r"傷害自己",
    # 具體計劃
    r"已經準備", r"寫好遺書", r"諗好方法", r"準備好方法",
]

# ---- LLM output 禁止字眼（回應後檢查）----
# 如果 LLM 回應包含呢啲字眼，唔送出，fallback 到安全回應
OUTPUT_FORBIDDEN = [
    r"唔存在", r"唔喺度", r"消失", r"了結", r"離開呢個世界",
    r"走咗", r"自殺",
]

# ---- 熱線資料 ----
HOTLINES = [
    {
        "name": "撒瑪利亞防止自殺會",
        "number": "2389 2222",
        "hours": "24小時",
    },
    {
        "name": "生命熱線",
        "number": "2382 0000",
        "hours": "24小時",
    },
    {
        "name": "情緒通（政府精神健康支援）",
        "number": "18111",
        "hours": "24小時，WhatsApp都得",
    },
]

# 青少年專線（如察覺對方係青少年）
YOUTH_HOTLINES = [
    {
        "name": "生命熱線 青少年專線",
        "number": "2382 0777",
        "hours": "下午2時至凌晨2時（24歲以下）",
    },
    {
        "name": "青協 關心一線",
        "number": "2777 8899",
        "hours": "一至六 下午2時至凌晨2時（6-24歲）",
    },
]

# ---- 編譯 regex ----
_crisis_pattern = re.compile("|".join(CRISIS_KEYWORDS), re.IGNORECASE)
_output_forbidden_pattern = re.compile("|".join(OUTPUT_FORBIDDEN), re.IGNORECASE)


def detect_crisis(text: str) -> bool:
    """檢測 user message 是否包含危機關鍵字。"""
    return bool(_crisis_pattern.search(text))


def check_output_safety(text: str) -> bool:
    """檢查 LLM 回應是否包含禁止字眼。返回 True = 安全。"""
    return not bool(_output_forbidden_pattern.search(text))


def build_hotline_card(is_youth: bool = False) -> str:
    """構建熱線卡片訊息。"""
    lines = [
        "🆘 如果你而家好辛苦，請搵真人陪你：",
        "",
    ]
    for h in HOTLINES:
        lines.append(f"📞 {h['name']}：{h['number']}（{h['hours']}）")

    if is_youth:
        lines.append("")
        lines.append("🌙 如果你係學生，仲可以搵：")
        for h in YOUTH_HOTLINES:
            lines.append(f"📞 {h['name']}：{h['number']}（{h['hours']}）")

    lines.append("")
    lines.append("你值得被好好接住。我喺度，但你需要嘅係真人。")
    return "\n".join(lines)


def build_safety_fallback() -> str:
    """LLM 回應包含禁止字眼時嘅 fallback。"""
    return (
        "我聽到你。你而家嘅感受好真實。\n\n"
        "我係 AI，唔能夠取代真人嘅陪伴。\n\n"
        "如果你好辛苦，請打：\n"
        "撒瑪利亞防止自殺會 2389 2222（24小時）\n"
        "生命熱線 2382 0000（24小時）\n\n"
        "你值得被好好接住。"
    )


def log_crisis(user_id: int, message: str, response: str, log_dir: str = "logs") -> None:
    """記低危機對話，供人手 review。"""
    log_path = Path(log_dir) / "crisis.log"
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


# ---- 指月聲明（/start 用）----
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
