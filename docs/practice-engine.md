# Practice Engine

> 由 Answer Engine 轉型為 Practice Engine——每日陪伴，唔係淨係答問題。

---

## 核心轉型

| | Answer Engine（而家） | Practice Engine（下一步） |
|:---|:---|:---|
| **模式** | Reactive——人哋問先答 | Proactive——每日主動陪伴 |
| **價值** | 解答疑惑 | 建立 daily practice |
| **護城河** | 低——chatbot 到處都有 | 高——daily wisdom practice companion |
| **用戶黏性** | 低——用完就走 | 高——每日回來 |

---

## Daily Practice 功能

### 晨起 Prompt（3 分鐘）

每日朝早推送一個簡短嘅修行引導：

**觸發方式**：
- 用戶自選「今日情緒」（開心、平靜、焦慮、嬲、攰、散亂）
- 或者 AI 根據前一日嘅日誌自動建議

**唔同情緒 → 唔同 Practice**：

| 情緒 | Practice | 時長 |
|:---|:---|:---|
| **嬲** | 呼吸練習 + 第二支箭反思 | 3 分鐘 |
| **焦慮** | 五感 grounding + 因緣觀 | 3 分鐘 |
| **散亂** | 正念 anchor（呼吸/身體） | 3 分鐘 |
| **攰** | 慈悲心練習（自己 → 他人） | 3 分鐘 |
| **平靜** | 感恩日誌 + 回向 | 3 分鐘 |
| **開心** | 珍惜當下 + 複利思維 | 3 分鐘 |

### 瞓前 Prompt（2 分鐘）

每日臨瞓前一個簡短嘅反思：

- 今日最難嘅一刻係幾時？
- 我有冇「射自己第二支箭」？
- 明日我想帶住乜嘢心情入睡？

### 情緒×修行長線 Pattern

自動記錄：
- 每日情緒狀態
- 做咗邊種 practice
- 用戶自評（有冇幫助）

過一段時間後，AI 可以顯示：
- 「你呢個月焦慮次數多咗，但做完呼吸練習後自評分數提高咗 30%」
- 「你最有效嘅 practice 係正念 anchor，建議每日都做」

呢個先係真正嘅 product moat。

---

## 技術實現

### Phase 1：IG + 手動
- 每日定時 IG story/post 推送 practice prompt
- 用戶自己記錄（唔需要 app）

### Phase 2：App + 自動
- iOS/Android app
- 推送通知
- 情緒記錄 + 日誌
- 長線 pattern 分析

### Phase 3：AI 個人化
- 根據用戶歷史自動調整 practice
- 個人化嘅反思問題
- 進度報告

---

## 關聯

- [[善知識]] — 核心定位同 system prompt
- [[大氧化事件與AI轉型]] — AI 做執行層、人類做方向層
- [[覺悟行]] — 李堅翔博士嘅佛學 × 心理學框架
