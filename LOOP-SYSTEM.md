═══════════════════════════════════════════

# LOOP-SYSTEM.md — 複利循環系統
> 一句話：三個嵌套 loop（週/月/季）+ 一條知識沉澱管道；每個 loop 有固定輸入輸出，弱模型攞住輸入就做到，唔使判斷「做唔做」。

## §1 每週回顧（週日，30分鐘）
**輸入**：本週 IG 帖數據（reach/saves/shares/留言）、DM 記錄、dev-log
**執行**（弱模型可代跑）：


逐帖填數據表（date/pillar/format/reach/saves/shares/comments）
用 RUBRICS §1 快評本週每個帖嘅文案（五維度，各 1-5）
答三條固定問題： a. 邊個支柱/格式表現最好？（數字） b. 有冇 DM/留言暴露咗 prompt 或內容嘅弱點？（有 → 記入 LEARNINGS.md） c. 下週 3 個帖：2 個延續最好嘅，1 個試新嘢

**輸出**：`reviews/weekly/YYYY-WW.md`（固定格式）+ 下週內容清單

## §2 每月迭代（月尾，半日）
**輸入**：4 份週報 + 當月 eval report + LEARNINGS.md 未處理項
**執行**：


跑全 suite eval（EVAL-PROTOCOL §1）
對照上月 report（--compare）
LEARNINGS.md 逐項處理：每項必須變成以下其一—— → 一條新 rule（入 RULES.md） → 一個 rubric 調整（入 RUBRICS.md，之後重新校準 judge） → 一個 template 修訂（入 TEMPLATES.md） → 一個新 eval case（入 cases.yaml） → 明確標「棄用」+ 一句原因 ⚠️ 唔准留喺 LEARNINGS.md 過月——呢條係複利嘅核心
Prompt 迭代（如需要，跟 EVAL-PROTOCOL §3）
檢查 ROADMAP 當月 KR：達成？未達成邊個？下月修訂？

**輸出**：`reviews/monthly/YYYY-MM.md` + 更新咗嘅制度檔案 + CHANGELOG

## §3 每季升級（季尾，一日）
**輸入**：3 份月報 + 用戶 feedback 彙總 + 制度檔案現況
**執行**：


制度檔案覆核：邊條 rule 三個月冇用過？（考慮刪——制度會肥大）
熱線核實（hotlines.md：每6個月，季檢時睇夠唔夠期）
Roadmap 下一季：用同一格式（目標/KR/驗收/週行動）寫
大版本決策（新功能/新平台/prompt 大改）——呢層需要 Tim 本人，唔外判俾模型

**輸出**：季報 + 下季 ROADMAP + 修訂版制度檔案

## §4 知識沉澱管道（隨時發生）


觸發：任何時候發現「呢樣嘢原來要咁做」 ↓ 即時記入 LEARNINGS.md（一行都得：日期 + 事件 + 教訓） ↓ 每月迭代時強制處理（§2.3） ↓ 變成 rule / rubric / template / case / 棄用

**LEARNINGS.md 格式**：


2026-07-12 | IG DM 有人問塔羅，回應太長 | 候選：RULES §2.1 加塔羅入拒絕清單
asciidoc
## §5 點解唔使意志力
- 每個 loop 有固定時間、固定輸入、固定輸出格式 → 唔存在「今日有冇心情做」
- 弱模型執行：週回顧同月迭代嘅 1-3 步全部係「攞數據填格仔 + 對照 rubric」，Haiku 都做到
- 唯一需要 Tim 判斷嘅位：季度大版本決策 + 佛學內容嘅體證把關（方向層唔外判）

---

## ✅ Verification Checklist
- [ ] 三個 loop 各有明確輸入/輸出檔案路徑
- [ ] LEARNINGS.md 有「唔准過月」強制處理規則
- [ ] 標明咗邊啲步驟弱模型做、邊啲必須 Tim 做
- [ ] 熱線核實已排入季檢
- [ ] 有制度瘦身機制（冇用嘅 rule 會被刪）


═══════════════════════════════════════════
