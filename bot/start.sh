#!/bin/bash
# 指月 bot wrapper — launchd / cron 用
# 從本 script 位置推算 repo root，唔 hardcode 本機路徑
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT" || exit 1
exec /usr/bin/python3 bot/bot.py
