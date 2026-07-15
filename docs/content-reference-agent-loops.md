# 指月 Content Reference — Claude Code Agent Loop 設計框架

**來源：** AI 郵報《Claude Code 官方把 AI Agent 拆成 4 種循環：比 Prompt 更重要的，是停止條件》
**原文：** https://www.aiposthub.com/claude-code-agent-loops-guide/
**來源日期：** 2026-07-07
**分析日期：** 2026-07-16

---

## 一、4 種 Loop 框架

Anthropic 將 Agent Loop 定義為：**Agent 重複執行一連串工作，直到符合停止條件。**

| Loop 類型 | 觸發方式 | 停止條件 | 適合情境 | Hermes 對應 |
|:---|:---|:---|:---|:---|
| **Turn-based** | 用戶下 Prompt | AI 判斷完成或需要更多資訊 | 一次性、較短、需人類判斷 | 平時對話 |
| **Goal-based** | 用戶設定目標 | 達成目標或到回合上限 | 有明確驗收條件嘅複雜任務 | Eval system |
| **Time-based** | 固定時間或間隔 | 用戶取消或外部工作完成 | 定期整理、監控 | Cron jobs |
| **Proactive** | 排程或外部事件 | 單次任務達標；Routine 持續運作 | 穩定、重複、可驗證嘅長期工作流 | Dual-star system |

---

## 二、核心觀點：停止條件比 Prompt 更重要

> 「你唔係要 AI 做得更耐，而係要佢知道幾時停。」

### 指月應用
- 每次對話回應：唔好一次過講晒，用戶冇回應就停
- Eval system：safety_trigger < 3 → 停，唔好再跑
- Cron jobs：冇新內容就靜默，唔好強行出 message

### 指月嘅停止條件設計
```
用戶講完 → 接住 → 留白 → 等用戶回應
                     ↓
              冇回應 = 停（唔好追问）
              有回應 → 繼續
```

---

## 三、Token 黑洞警告

> 「Loop 一旦自動重試，成本容易從『多跑幾次』變成『同時跑很多條工作流』。」

### 控制方式
1. 設定明確成功條件
2. 設定上限（回合數、時間）
3. 可預測嘅步驟改成 script（唔用 LLM）

### 指月嘅控制策略
- Eye-drop reminder → 已用 `no_agent=True` + Python script（✅）
- TechOrange digest → 已用 script 抓取 RSS（✅）
- 其他 cron jobs → 考慮將可預測嘅部分改 script，減少 LLM 調用

---

## 四、Proactive Loop 同 Dual-Star 對照

### Claude Code 嘅 Proactive 範例
> 「每小時檢查回饋頻道 → 自動分流 Bug → 平行探索 3 種解法 → 另一個 Agent 做 Review」

### 指月嘅 Dual-Star 實現
> 「Hermes 收到訊息 → 分析 → 執行 cron/文件/投資 → 雙星 review」

### 差別
- Claude Code：用原生工具（/goal、/loop、/schedule）
- Hermes：用 cron jobs + subagent + OpenClaw 協作
- **底層邏輯完全一樣**

---

## 五、獨立 Reviewer 原則

> 「高風險變更要有獨立 Reviewer。讓第二個 Agent 在新脈絡中檢查結果，降低主 Agent 對自己解法過度有信心的問題。」

### 指月應用
- 指月 bot 嘅回應唔應該自動發送，需要有 review 層
- Eval system 就係呢個角色——用 judge model 檢查善知識 model 嘅輸出
- 建議：crisis case 一定要人手 review（已經有嘅 policy）

---

## 六、可直接應用嘅規則

### 1. 設計 Loop 先問三個問題
- 邊個觸發工作？（用戶 / 排程 / 外部事件）
- 乜嘢算完成？（可驗證嘅條件）
- 邊個負責驗證？（用戶 / AI / 獨立 Reviewer）

### 2. 停止條件必須具體
- ❌「做到最好」
- ✅「測試全部通過」
- ✅「用戶冇回應 → 停」
- ✅「跑到第 N 個回合 → 停」

### 3. 可預測嘅步驟改 script
- 每次都做一樣嘅嘢（抓 RSS、check 狀態、格式化輸出）→ 用 script
- 需要判斷嘅嘢（分析、共情、決策）→ 用 LLM

### 4. Proactive Loop 要有安全閥
- 設定 Token 上限
- 設定時間上限
- 設定回合上限
- 冇上限嘅自動化 = Token 黑洞

---

## 七、同 Project-Decathlon 嘅連結

| Decathlon Phase | Loop 類型 | 指月對應 |
|:---|:---|:---|
| Grill（拷問需求） | Turn-based | 對話式問答 |
| Slice（垂直切片） | Goal-based | 每個切片有驗證標準 |
| Feedback Loop | Time-based | Cron 定期檢查 |
| 全自動化 | Proactive | Dual-star + cron + eval |

---

*此文件為指月 content reference，唔係 guidelines。指月嘅核心規則以 system-prompt.md 同 CONTENT-PILLARS.md 為準。*
