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
prompts/
  system-prompt.md  # 善知識 system prompt（從主項目複製）
logs/
  crisis.log        # 危機對話記錄（每日 review）
```

## 安全設計

1. **獨立 regex 層**：唔靠 LLM 判斷危機，code level 攔截
2. **Crisis log**：每個危機回應記低，第二朝人手 review
3. **三輪上限**：bot 唔准安撫 crisis case 超過三輪
4. **無 login、無 database**：對話歷史淨存 memory（dict），重啟即清

## Token 獲取

1. 打開 Telegram，搵 @BotFather
2. 發 `/newbot`
3. 名叫 `指月`，username 例如 `point_to_moon_bot`
4. 攞到 token，貼入 `.env`
