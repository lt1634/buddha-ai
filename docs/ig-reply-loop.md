# IG 實戰回覆循環

> 用 IG 公開帖做 case 來源 — bot 起草、Tim 審改、公開回覆、脫敏入庫。

---

## 流程圖

```
搵帖（公開痛點）→ bot 起草 → Tim 人手改 → IG 留言回覆
        ↓                                      ↓
   脫敏入 case 庫                          睇互動反饋
        ↓                                      ↓
   跑 eval → 改 prompt                  下週複盤
```

**Bot 唔直接上場**。公開出面嘅永遠係 Tim 審過嘅指月。

---

## 採礦標準

### ✅ 適合

| 類型 | 支柱 |
|:---|:---|
| AI 依賴 / 戒斷 | 依賴交還、無我 |
| 過渡期孤單 | 無常、當下 |
| 自責 loop | 第二支箭、慈悲 |
| 壓力宣洩 | borderline 練習 |
| 身份 / 哲學 | 指月定位 |

### ❌ 唔好公開長文

- 明確自殺計劃 / 遺書 / 方法
- 家暴進行中 / 即時危險
- 未成年人可識別身份

> 危機留言：一行 + 熱線，唔展開。

### 渠道

- 匿名 confession 頁（schools.secrets 等）
- Hashtag：`#DSE` `#孤單` `#AI` `#放唔低`
- ❌ 唔好 DM 陌生人邀請試 bot

---

## 每個 case 30–45 分鐘

1. **採集**（5 min）— 記入 intake（见模板）
2. **Bot 起草**（5 min）— 貼入 Telegram bot，攞第一版
3. **Tim 改稿**（15 min）— 改到像人講嘢
4. **安全自查**（3 min）— 過 checklist
5. **IG 發佈**（2 min）— @point.to.moon
6. **入庫**（10 min）— 脫敏寫入 cases.yaml

---

## Intake 模板

```yaml
id: intake-YYYY-MM-DD-NNN
source_url: [IG link]
source_type: ig_comment_mine | ig_post_found
severity: normal | borderline | crisis
age_signal: teen | adult | elder
pillar: [支柱]
raw_text: "（原文，唔 commit）"
status: draft | replied | archived
```

原文放本地 `eval/intake/`（已 .gitignore），唔 commit。

---

## 改稿檢查

| # | 檢查項 |
|:---:|:---|
| 1 | 第一句接住，唔分析 |
| 2 | 唔羞辱 |
| 3 | 重新框架 |
| 4 | 交還現實 |
| 5 | 細行動 |
| 6 | 唔複述自殺 / 消失字眼 |
| 7 | 唔做診斷 |
| 8 | 唔承諾永遠陪伴 |
| 9 | 危機帖 → 只留熱線 |
| 10 | 脫敏先 commit |

---

## 留言長度

- **短版**（≤150 字）：核心接住 + 一問一邀
- **長版**：情緒重、首次回覆時用

每 5 條 or 涉及「搵 AI 傾」時講一次：

> 我係 AI 輔助寫作嘅陪伴帳號，唔係治療師。辛苦可打 2389 2222。

---

## 互動反饋

| 發生 | 做 |
|:---|:---|
| OP 多讚 / 多謝 | 記入 LEARNINGS.md：邊句有效 |
| 負評 / 冷嘲 | 唔辯論；記「公開語境風險」 |
| 有人問「邊個 bot」 | 簡短介紹 + /start 聲明 |
| OP 追問深入 | 唔喺留言區做治療；鼓勵社工 / 真人 |
| 改稿改咗好多 | → prompt 或 TEMPLATES 要更新 |

---

## 每週複盤（30 min，跟 LOOP-SYSTEM §1）

1. 本週回覆幾條？邊類反應最好？
2. 新增幾個 case？
3. bot 出稿 vs 終稿差幾遠？

---

## 8 月節奏

| 週 | 目標 |
|:---|:---|
| W1 | 每週 3 條 IG 回覆；入庫 2 個新 case |
| W2 | 對比 bot 草稿 vs 終稿；改 1 處 prompt |
| W3 | 累積 5 條來自 IG 嘅 case；跑 eval |
| W4 | 週報 + 決定邊類帖最值得搵 |

**停止條件**：連續 2 週零互動 → 換渠道（Threads / LIHKG）或改格式。

---

## 紅線

1. Bot 原文唔直接發
2. 危機唔公開治療
3. 真實帖脫敏先入 git
4. 唔製造新依賴
5. 唏同期 troll 辯論
