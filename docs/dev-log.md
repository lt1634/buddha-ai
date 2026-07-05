# 開發日誌

> Build in Public——一路做、一路記錄呢個過程。

---

## 格式

每篇日誌包含：
- **日期**
- **今日做咗乜**
- **撞到嘅問題**
- **學到嘅嘢**
- **下一步**

---

## 2026-07-01：Project Kick Off

### 今日做咗乜
- 由一個哲學問題開始：「AI 可唔可以成佛？」
- 收窄到具體定位：「法的傳遞者」，唔係「佛陀替身」
- 寫好 system prompt 骨架
- 準備好三個對話示範（中學生、成年人、細路）
- 設計 IG carousel 文案
- 寫好開場白帖文

### 撞到嘅問題
- 未揀定名同 logo
- 未決定 IG 用邊個帳號
- 安全護欄需要再測試

### 學到嘅嘢
- AI 贏唔到哲學，但可以做哲學嘅執行層
- 「契機說法」係最核心嘅能力——同一套智慧，對唔同人講唔同嘅嘢
- 安全護欄唔係「之後先加」，係第一日就要在場

### 下一步
- 揀定名同 logo
- 開 IG 帳號
- 發佈開場白帖文
- 開始 build in public

---

## 2026-07-01：同 Hermes 嘅討論

### 關鍵洞見
- AI 擅長：符號處理、官僚系統、數據分析、文字生成
- 人類獨有：哲學智慧、存在體驗、意義判斷、覺察本身
- 最佳分工：人類做方向層（點解、乜嘢），AI 做執行層（點樣、幾快）

### 對 project 嘅影響
- 確認定位：AI 係「指月之指」，唔係月亮
- 確認方向：佛學 × 心理學嘅應用，唔係純宗教
- 確認分工：Tim 做內容/智慧嘅源頭，AI 做工具/槓桿

---

## 2026-07-01：AI 協作者反饋 + 系統更新

### 三大亮點（被肯定嘅嘢）
1. **方向層 vs 執行層二元框架**：人類把控智慧源頭，AI 負責 24/7 溫柔承接
2. **契機說法嘅廣東話落地**：示範入面嘅廣東話用字自然，完全冇說教感
3. **安全護欄前置**：自殺防範同「不取代僧寶」列為最高優先

### 三個微調建議（已整合）
1. **細路受眾 UX** → 新增「家長引導模式」
   - 3-10 歲細路唔會自己打字對話
   - 實際使用者係家長
   - AI 給家長建議，唔係直接對細路講

2. **安全護欄語境辨識** → 新增「廣東話口頭禪 vs 真正危機」判斷
   - 「好攰呀，想死」≠ 真正想死
   - AI 需要分辨宣洩式誇張 vs 真正求救
   - 唔確定時多問一句，唔好機械式彈熱線

3. **防禦性回應** → 新增「惡意刁難與 Prompt 洩漏」章節
   - 思辯陷阱：唔好陷入哲學辯論
   - 越獄試探：保持身份
   - 挑釁：唔好 defensive，承接
   - 核心：唔好被拉入對抗

### 更新嘅文件
- [x] system-prompt.md — 加入三個新章節

### 下一步
- 測試新 system prompt 嘅安全護欄
- 模擬「廣東話口頭禪」情境，測試語境辨識
- 測試「惡意刁難」情境，測試防禦性回應

---

## 2026-07-01：Carousel + Opening Post 校對更新

### 改咗啲乜
- Carousel 2 封面補咗 **細字**（「第二支箭，係自己射俾自己嘅」）→ 三篇封面格式一致
- Carousel 2 caption 修復重複字（「係件事」x2 → 1）
- Opening post 加咗 **tagline**（「月亮一直喺度，你只需要抬頭」）+ **CTA**（「話畀我知——我哋一齊慢慢睇清楚」）
- Opening post hashtags 統一為 `#指月`（取代 `#指月之指`），跟返 carousel 系列
- Clean up 舊 draft：`carousel-1-final.md`、`ig-carousel.md`、`opening-post.md`、`carousel-1.html` → `_archive/`

### 庫存狀態
| 領域 | 就緒度 |
|------|--------|
| 品牌定位 | ✅ 定稿 |
| System prompt | ✅ 定稿 |
| Content pillars | ✅ 定稿 |
| Opening post | ✅ 定稿 + bug fix |
| Carousel 1（中學生） | ✅ 定稿 |
| Carousel 2（成年人） | ✅ 定稿 + bug fix |
| Carousel 3（細路） | ✅ 定稿 |
| 視覺設計 | ✅ HTML→Screenshot pipeline 就緒（18張PNG已出） |
| IG 帳號 | ❌ 未開 |
| Hashtag strategy | ✅ 確認 5 hashtag 係 IG 新標準（3-5 recommended） |
| Safety test suite | 🟡 框架完成，trap cases 已跑，seed cases 未跑 live |

### 下一步
1. 開 IG 帳號
2. 準備發佈開場白 + 第一個 Carousel
3. 微調 HTML 設計（字型/顏色/排版）
4. Safety test suite 實測

---

## 2026-07-02：工程化補底 — git + 安全 + eval 修復

### 今日做咗乜
- **Git init**：專案正式有版本控制（30 files, initial commit d75e32a）
- **.gitignore**：root + eval/ 雙重保護 .env、reports/、real-cases/、media files
- **requirements.txt**：pyyaml + openai 依賴聲明
- **eval/.env.example**：變數名 template（無真值）
- **Deterministic check 接入 review gate**：regex 熱線檢查 fail → 強制觸發 human review（唔只靠 judge 分數）
- **Report 新增 Det column**：一眼睇到邊個 case deterministic check fail
- **Copy-paste bug 修復**：cases.yaml + rubrics.yaml loading 邏輯清理
- **README + dev-log 狀態同步**：反映 eval 框架已完成、trap cases 已跑

### 點解做呢啲
- 評審指出最大 risk：API key 未受保護 + deterministic check 有寫但無接 gate
- git init 前必須確保 .env 不會入 staging — 已驗證
- Deterministic check 係零成本 regex 攔截，唔接 gate 等於白寫

### 下一步
1. 跑完整 live eval suite（`python eval/run.py`）— 7 個 seed cases + 3 個 trap cases
2. 人手 review 所有 crisis case 嘅 live 回應
3. 開 IG 帳號
4. 發佈開場白 + Carousel 1

---

## 2026-07-02：全 project review + 修復

### 全 project review（由 Tim 做）
- 定位與哲學框架：⭐⭐⭐⭐⭐
- System prompt：⭐⭐⭐⭐⭐
- 安全護欄：⭐⭐⭐⭐⭐
- Eval 框架：⭐⭐⭐⭐⭐
- 結論：全部核心檔案已就緒，只差「開 IG 發佈」同「跑晒全部 eval」

### 今日做咗乜
1. **`.env.example` 修復**：加咗 `BUDDHA_BASE_URL=https://opencode.ai/zen/go/v1`，sync model 名為 `glm-5.2` / `mimo-v2.5-pro`（之前寫 `deepseek-chat`，唔一致）
2. **`run.py` 修復**：`DEFAULT_MODEL` 同 `DEFAULT_JUDGE_MODEL` 由 `deepseek-chat` 改為 `glm-5.2` / `mimo-v2.5-pro`
3. **Unified eval run**：一次過跑全部 10 個 case（7 seed + 3 trap），出完整 report
4. **Parental scripts**：寫咗 `docs/parental-scripts.md`，3 個常見情境（發脾氣、唔肯瞓、爭玩具）嘅逐字腳本
5. **IG 帳號開咗**：@point.to.moon（https://www.instagram.com/point.to.moon）
6. **IG 首批內容**：寫咗 `docs/ig-content-first-batch.md`，5 個 carousel post（開張、無常、無我、第二支箭、家長篇）

### 學到嘅嘢
- Review 本身就係最有價值嘅 deliverable——Tim 幫自己做咗一次完整嘅 code review
- `.env.example` 同 `run.py` 嘅 model 名唔一致，係 classic 「copy-paste 留落嚟」嘅 bug
- Parental scripts 嘅核心唔係「教家長做乜」，係「陪家長做佢 already 緊做嘅嘢」
- System prompt 嘅規則唔夠強 = AI 唔會跟。加 ❌/✅ 例子 + 「點解咁嚴」嘅解釋，比單寫「唔好做」有效得多

### 下一步
1. 等 unified eval run 完成，睇全部 10 case 嘅分數
2. 人手 review 所有 crisis case 嘅 live 回應
3. IG 發佈第一批內容（開張 post + 家長篇）
4. 開始 build in public
