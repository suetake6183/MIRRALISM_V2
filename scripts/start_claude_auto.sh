#!/bin/bash
# ClaudeCode自動化 - バックグラウンド起動スクリプト

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPLESCRIPT_FILE="$SCRIPT_DIR/claude_final_auto.applescript"
LOG_FILE="$HOME/.mirralism/claude_auto_launcher.log"

# ログディレクトリ作成
mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date)] 🚀 ClaudeCode自動化開始" >> "$LOG_FILE"

# 既存のプロセスを停止
pkill -f "claude_final_auto.applescript" 2>/dev/null

# AppleScriptをバックグラウンドで実行
osascript "$APPLESCRIPT_FILE" &

APPLESCRIPT_PID=$!
echo "[$(date)] ✅ AppleScript起動成功 (PID: $APPLESCRIPT_PID)" >> "$LOG_FILE"

echo "🤖 ClaudeCode自動化が開始されました"
echo "   PID: $APPLESCRIPT_PID"
echo "   ログ: $LOG_FILE"
echo "   停止: scripts/stop_claude_auto.sh"