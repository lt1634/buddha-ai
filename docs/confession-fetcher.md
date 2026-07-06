# Confession Link Fetcher

> 每日自動搜集 IG / Threads 帖 link，供 intake 篩選。

---

## 運行方式

Hermes cron job — 每日 20:00 跑 web_search，輸出 link list。

## 關鍵字（按效果分組）

### 高命中

| 關鍵字 | 預期結果 |
|:---|:---|
| DSE 完 孤單 | 過渡期空虛 |
| AI 陪伴 投入 | AI 依賴 |
| 放唔低 前任 | 失戀 / 自責 |
| 好辛苦 點算 | 壓力宣洩 |
| AI 男友 AI 女友 | AI RP 依賴 |
| 失戀 好難過 | 分手痛 |
| 過渡期 孤單 | 節奏斷裂 |

### Borderline 練習

| 關鍵字 | 預期結果 |
|:---|:---|
| 想死 頂唔順 | borderline 口頭禪 |
| 返工 好累 | 工作壓力 |
| 讀書 壓力大 | 學業焦慮 |

## 評分（篩選用）

| 條件 | 分數 |
|:---|:---:|
| OP 有具體故事 | +2 |
| 有求助意圖（點算、好辛苦） | +2 |
| 留言有共鳴 | +1 |
| Crisis / 未成年人可識別 | -10（跳過） |

## 輸出格式

```markdown
# Confession Links — YYYY-MM-DD

## Link 1
- URL: [link]
- 標題/摘要: ...
- 類型: AI依賴 / 失戀 / 壓力 / ...
- 評分: +4
- 點解值得回: ...

## Link 2
...
```

## 去重

存過嘅 link 唔再出現。每次搜完對比 `docs/confession-links/` 已有檔案。

## 紅線

- ❌ 唔搜未成年人帖子
- ❌ 唔搜明確危機帖（遺書 / 計劃）
- ❌ 唔自動爬 IG 內容（Meta 封了）
