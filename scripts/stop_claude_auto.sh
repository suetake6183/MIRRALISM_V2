#!/bin/bash
# ClaudeCode自動化 - 停止スクリプト

LOG_FILE="$HOME/.mirralism/claude_auto_launcher.log"

echo "[$(date)] 🛑 ClaudeCode自動化停止要求" >> "$LOG_FILE"

# AppleScriptプロセスを停止
pkill -f "claude_final_auto.applescript"

if [ $? -eq 0 ]; then
    echo "✅ ClaudeCode自動化を停止しました"
    echo "[$(date)] ✅ 自動化停止完了" >> "$LOG_FILE"
else
    echo "⚠️ 停止するプロセスが見つかりませんでした"
    echo "[$(date)] ⚠️ 停止対象プロセスなし" >> "$LOG_FILE"
fi