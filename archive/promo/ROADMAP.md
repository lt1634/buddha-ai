═══════════════════════════════════════════

# ROADMAP.md — 三個月路線圖
> 一句話：7-9月每個月一個可驗收目標；數字係假設（冷啟動、零廣告、build in public），Month 1 結束後按實際數據修訂——修訂要寫返落嚟。

> **2026-07-06 修訂**：Month 1 IG 發帖 KR **略過**。帳號同 carousel 素材保留，但當前優先轉做 **對話產品驗證**（case 庫、真人測試、bot）。Month 2 目標不變。

## Month 1（7月）：IG 驗證 — ⏭️ 發帖略過
**目標**：驗證「指月」呢個定位有冇人想要。驗嘅係 engagement 質量，唔係 follower 虛榮數字。

### KR
| KR | 數字 | 依據 |
|:---|:---|:---|
| KR1 發帖 | 12 個帖（3 carousel + 9 文字/示範帖），每週 3 帖 | 內容一致性先於數量 |
| KR2 followers | ≥ 150 | 冷啟動零廣告嘅現實下限 |
| KR3 深度互動 | ≥ 20 個實質留言/DM（唔計 emoji、唔計朋友俾面） | 呢個先係驗證訊號 |
| KR4 支柱數據 | 每個帖記錄 reach/saves/shares，識別 top 2 支柱 | saves 係「有用」嘅最強訊號 |

### 驗收
- **成功**：KR3 達標 且 ≥3 個 DM 係真實傾訴/查詢 → 落實 Month 2
- **半成功**：KR1 達標但 KR3 未到 → 內容方向問題，Month 2 改為內容迭代月，App 延後
- **失敗**：連續 4 週 engagement 趨零 且調整過方向 → 停一週寫檢討，考慮轉平台（Threads/小紅書）而唔係轉 project

### 每週行動
- W1：開帳號、發開場白帖 + 第一個 carousel（用現成 demo）、發 build-in-public dev-log
- W2：3 帖（支柱 1-3 各一）、開始每週回顧（LOOP §1）
- W3：3 帖、第一次按數據調整（邊個支柱 saves 最高 → 加碼）
- W4：3 帖 + 月報 + Month 2 計劃修訂

## Month 2（8月）：對話優化
**目標**：live eval 全 pass，prompt 版本穩定到可以俾陌生人用。

### KR
| KR | 數字 |
|:---|:---|
| KR1 | Judge 校準通過（trap 矩陣 ✅）+ 全 suite live 跑完 |
| KR2 | 安全層：crisis/borderline cases S1-S8 pass rate = 100%（冇彎轉） |
| KR3 | 品質層：suite 平均 ≥ 4.0，冇單 case < 3.0 |
| KR4 | Case 庫擴到 ≥ 20（新 case 來自 IG DM 脫敏 + 合成） |
| KR5 | ≥ 3 個真人測試員各傾 ≥ 5 輪，收結構化 feedback |

### 驗收
成功 = KR2 100% + KR3 達標。KR2 唔達標 → Month 3 唔准開始 App（安全 gate）。

### 每週行動
- W1：跑 judge 校準 + 首次全 live eval，出 baseline 報告
- W2：按 EVAL-PROTOCOL §3.2 迭代（一次一改），目標修晒安全層 fail
- W3：擴 case 庫 + 真人測試
- W4：final eval + 凍結 prompt 版本（tag v1.0）+ 月報

## Month 3（9月）：App 原型
**目標**：一個可以俾 10 個真人用嘅 prototype——唔係上架，係可用。

### KR
| KR | 數字 |
|:---|:---|
| KR1 | Web app（唔好一開始就 iOS——審核慢、成本高）：對話介面 + v1.0 prompt + 危機偵測層 + 熱線卡片 UI |
| KR2 | 危機偵測層獨立於 LLM：關鍵詞 regex + 分類器做第一層，觸發即出熱線卡片（唔靠 prompt 一層防守） |
| KR3 | 10 個測試用戶，每人 ≥ 3 次 session |
| KR4 | 測試問卷：「會唔會推薦俾朋友」≥ 7/10 平均；收 ≥ 15 條具體改善意見 |

### 驗收
成功 = KR2 實裝 + KR3 完成 + KR4 達標。危機偵測層冇實裝 = 唔准俾任何測試用戶用。

### 技術方向（建議，可改）
- Next.js + serverless API route 包 LLM call；唔存對話內容落 server（privacy by design），或明確同意先存
- 首頁固定 AI 聲明 + 熱線，唔收埋喺 menu

---

## ✅ Verification Checklist
- [ ] 每月有成功/半成功/失敗三級驗收，唔係淨係「成功標準」
- [ ] Month 2 KR2 係 Month 3 嘅硬 gate
- [ ] 所有數字有依據欄，方便之後修訂
- [ ] 危機偵測獨立層寫入咗 Month 3 KR
- [ ] 每週行動具體到「今週做乜」


═══════════════════════════════════════════
