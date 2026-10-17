# 指月（Finger Pointing at Moon）

> 佛學智慧 × 心理學方法嘅心靈陪伴 AI。  
> 唔係治療、唔係算命、唔係取代人——係「指月之指」，指向你內心本來就有嘅智慧。

公開倉庫：https://github.com/lt1634/buddha-ai

## 而家係咩

呢個 repo 收嘅係**人設、安全護欄、同評測框架**——方便公開審視同迭代。早期 Telegram bot、IG carousel、推廣／階段路線圖已搬去 [`archive/`](archive/)，唔再維護。

## 核心目錄

| 路徑 | 內容 |
| :--- | :--- |
| `prompts/` | 指月 system prompt（人設同對話原則） |
| `shared/` | 共用程式：`safety.py`（危機偵測）、`hotlines.py`（熱線卡）、paths／env |
| `eval/` | 評測題庫、rubrics、trap cases、`run.py` |
| `RULES.md` / `RUBRICS.md` / `EVAL-*.md` / `EXTENSION-RULES.md` | 規則同評測說明 |
| `docs/` | 品牌、家長腳本、測試倫理、練習引擎、內容參考（唔係硬廣） |
| `tests/` | `test_safety.py`、`test_eval_parse.py` |
| `archive/` | 2026-10-18 歸檔嘅過期實驗（見 `archive/README.md`） |

## 安全護欄（最高優先）

- ❌ 唔做醫療／精神診斷，唔取代治療
- ❌ 唔算命、唔預測吉凶、唔做法事
- ❌ 唔以因果報應恐嚇人
- ✅ 始終表明自己係 AI 工具
- ✅ 偵測到自殺／自殘跡象 → 即刻引導真人熱線
  - 撒瑪利亞防止自殺會：2389 2222
  - 生命熱線：2382 0000

危機偵測喺 **code 層**（`shared/safety.py`），唔單靠 prompt。

## 點跑測試

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```

而家 CI 只跑保留嘅 safety 同 eval parse 測試。

## 點跑 eval（需要 API key）

```bash
cd eval
cp .env.example .env   # 填入 OPENAI_API_KEY 等
python run.py
```

詳見 `EVAL-PROTOCOL.md`、`eval/CASE-INDEX.md`。

## 定位

- **唔係**：佛陀、開悟者、出家僧人、心理治療師
- **係**：指月之指、善知識、同行者
- **功能**：用佛學智慧 + 心理學方法，陪伴面對煩惱、轉化痛苦

佛經：「如人以手指月示人，彼人因指，應當看月。」  
AI 唔係月亮本身——佢係指向月亮嗰隻手指。
