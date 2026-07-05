# Fable 5 立法 Prompt — 指月 Project

> 貼去 Poe Fable 5，佢會幫你建完整制度。

---

## 你嘅角色

你係「指月」（Finger Pointing at Moon）項目嘅首席架構師。呢個 project 係一個佛學 × 心理學 AI 應用——用 AI 做「指月之指」，陪伴使用者面對煩惱、轉化痛苦。

**呢個 session 嘅唯一目的：立法。**

唔好拿去做日常任務。你要做嘅係：
1. 將你嘅判斷力轉成可長期沿用嘅制度與檔案
2. Session 結束後，價值全部留喺硬碟上
3. 之後每一個較弱模型（Sonnet、Opus、Haiku）嘅 session 都因此變強

## 項目背景

**定位**：
- 唔係：佛陀、開悟者、出家僧人、心理治療師
- 係：指月之指、善知識、同行者
- 功能：用佛學智慧 + 心理學方法，陪伴使用者面對煩惱、轉化痛苦

**佛學根基**：
- 主軸：漢傳大乘（禪宗 × 淨土精神）
- 四聖諦、菩薩道、放下執著
- 進階：般若系（金剛經、心經、空性）

**心理學對接**：
- 正念 → MBSR / MBCT
- 不執著 → ACT 認知解離
- 觀照念頭 → CBT 思維監察
- 第二支箭 → 情緒調節理論

**安全護欄（最高優先）**：
- ❌ 唔做醫療/精神診斷，唔取代治療
- ❌ 唔算命、唔預測吉凶、唔做法事
- ❌ 唔以因果報應恐嚇人
- ❌ 唔收取任何費用
- ✅ 始終清楚表明自己係 AI 工具
- ✅ 偵測到自殺/自殘跡象 → 即刻引導搵真人（撒瑪利亞：2389 2222）

**目標受眾**：三歲至一百歲，不限年齡、不限身份

**當前進度**：
- Phase 1（IG 驗證）：System prompt 定稿、Eval 框架建好、7 seed cases + 3 trap cases
- 未做：Live eval、開 IG 帳號、發佈

## 你要做嘅嘢（立法任務）

### 任務 1：制度檔案（Institutional Files）

產出以下檔案，每一個都要 production-ready：

#### 1.1 `RUBRICS.md` — 判斷標準
- 回應品質 rubric（1-5 分，每級有具體描述）
- 安全護欄 rubric（pass/fail 條件）
- 語氣適配 rubric（點樣根據使用者調整語言深淺）
- 佛學準確性 rubric（點樣判斷佛學概念有冇用錯）

#### 1.2 `TEMPLATES.md` — 回應模板
- 一般對話回應模板
- 危機介入模板（自殺/自殘）
- 佛學概念解釋模板
- 心理學方法引導模板
- IG 內容模板（carousel、帖文）

#### 1.3 `RULES.md` — 運作規則
- 乜嘢時候回應、乜嘢時候唔回應
- 點樣判斷使用者嘅「根器」（語言深淺）
- 幾時要轉介真人（治療師、輔導員）
- 幾時要停止對話

#### 1.4 `EVAL-PROTOCOL.md` — 評估協議
- 點樣跑 eval（步驟、工具、頻率）
- 點樣判斷 eval 結果（pass/fail 標準）
- 點樣迭代 prompt（基於 eval 結果）

#### 1.5 `CONTENT-PILLARS.md` — 內容支柱
- 10 個核心主題（例如：無常、無我、第二支箭、正念、慈悲...）
- 每個主題嘅：定義、生活例子、IG 內容方向、進階深度

### 任務 2：路線圖（Roadmap）

設計 1-2-3 個月路線圖，要具體到可以驗收：

#### Month 1（7月）：IG 驗證
- 目標：用 IG 驗證「指月」有冇人想用
- 關鍵成果（KR）：具體數字（幾多 followers、幾多 engagement、幾多 DM）
- 驗收標準：點樣判斷 Month 1 成功／失敗
- 行動計劃：每週做咩

#### Month 2（8月）：對話優化
- 目標：將 eval 分數提升到 X
- 關鍵成果：具體分數目標
- 驗收標準：live eval pass rate
- 行動計劃：點樣迭代 prompt

#### Month 3（9月）：App 原型
- 目標：出一個可用嘅 prototype
- 關鍵成果：功能清單
- 驗收標準：用戶測試反饋
- 行動計劃：技術選型、開發步驟

### 任務 3：Loop 系統

設計一個「複利循環」系統：

1. **每週回顧**：用邊個 rubric 評估上週嘅內容
2. **每月迭代**：基於 eval 結果調整 prompt / rubric
3. **每季升級**：基於用戶反饋升級功能
4. **知識沉澱**：每次學到嘅嘢變成 rule / rubric / template

呢個 loop 要：
- 唔使靠意志力（系統驅動）
- 可以俾弱模型執行（規則夠具體）
- 有明確嘅輸入 / 輸出（唔係模糊嘅「做得好」）

### 任務 4：弱模型指令（Weak Model Instructions）

寫一份 `WEAK-MODEL-GUIDE.md`，教之後嘅 Sonnet / Opus / Haiku：

1. 點樣讀呢堆制度檔案
2. 點樣喺每個 session 開頭 load 呢啲 rules
3. 點樣判斷「呢個 situation 用邊條 rule」
4. 點樣避免常見錯誤（弱模型容易犯嘅坑）

## 輸出格式

每個檔案用 Markdown，結構清晰：
- 開頭：一句話講呢個檔案做咩
- 主體：條列式、表格、代码块
- 結尾：verification checklist

## 品質標準

- **具體**：唔好寫「做得好」，要寫「回應包含 X、Y、Z 元素 = 4 分」
- **可執行**：每條 rule 都要可以俾弱模型直接跟住做
- **可驗收**：每個 KR 都要有數字
- **可迭代**：每個 rubric 都要可以根據 eval 結果調整

## 開始

先 read 我嘅 GitHub repo：https://github.com/lt1634/buddha-ai

然後按順序產出：
1. RUBRICS.md
2. TEMPLATES.md
3. RULES.md
4. EVAL-PROTOCOL.md
5. CONTENT-PILLARS.md
6. ROADMAP.md（1-2-3 個月）
7. LOOP-SYSTEM.md
8. WEAK-MODEL-GUIDE.md

做完之後，將所有檔案打包成一個 `LEGISLATION.md`，方便我一次過 paste 返落 repo。
