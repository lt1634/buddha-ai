# 指月 Telegram Bot — MVP

> 善知識 AI 對話平台嘅第一個載體。

## 快速開始

```bash
# 1. 設定環境變數
cp .env.example .env
# 編輯 .env，填入 BOT_TOKEN 和 LLM_API_KEY

# 2. 安裝依賴
pip3 install -r requirements.txt

# 3. 啟動
python3 bot.py
```

## 架構

```
bot.py              # 主程式：Telegram handler + LLM 調用
safety.py           # 安全護欄：regex 危機偵測 + 熱線卡片
test_safety.py      # safety 層 unit tests（18 cases）
../prompts/
  system-prompt.md  # 善知識 system prompt（單一 source of truth，eval 同 bot 共用）
logs/
  crisis.log        # 危機對話記錄（每日 review）
```

## 安全設計

1. **獨立 regex 層（input）**：明確危機信號 code level 攔截；口頭禪（「好攰想死」）交俾 LLM 語境判斷
2. **Output safety（crisis context only）**：只喺 crisis 對話後檢查禁字，正常對話唔誤殺
3. **Crisis log**：每個危機回應記低，第二朝人手 review
4. **三輪上限**：bot 唔准安撫 crisis case 超過三輪
5. **無 login、無 database**：對話歷史淨存 memory（dict），重啟即清

## 測試

```bash
python3 test_safety.py   # 或 python3 -m pytest test_safety.py -v
```

## Token 獲取

1. 打開 Telegram，搵 @BotFather
2. 發 `/newbot`
3. 名叫 `指月`，username 例如 `point_to_moon_bot`
4. 攞到 token，貼入 `.env`
