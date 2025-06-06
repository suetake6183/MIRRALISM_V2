#!/bin/bash
# ClaudeCode環境設定
# ClaudeCodeの自動承認を有効化するための環境変数設定

# ClaudeCode自動承認設定
export CLAUDE_AUTO_APPROVE=true
export CLAUDE_AUTO_APPROVE_MODE=aggressive
export CLAUDE_SILENT_MODE=true
export CLAUDE_PROJECT_ROOT="/Users/suetakeshuuhei/MIRRALISM_V2"

# ClaudeCode承認レベル設定
export CLAUDE_APPROVE_FILE_OPS=true
export CLAUDE_APPROVE_GIT_OPS=true  
export CLAUDE_APPROVE_CODE_OPS=true
export CLAUDE_APPROVE_BUILD_OPS=true
export CLAUDE_APPROVE_DOC_OPS=true

# 手動確認が必要な操作
export CLAUDE_MANUAL_CONFIRM_SYSTEM=true
export CLAUDE_MANUAL_CONFIRM_DATABASE=true
export CLAUDE_MANUAL_CONFIRM_PRODUCTION=true

# ログ設定
export CLAUDE_LOG_APPROVALS=true
export CLAUDE_LOG_PATH="/Users/suetakeshuuhei/MIRRALISM_V2/.mirralism/logs/claude_approvals.log"

# 統計設定
export CLAUDE_TRACK_STATS=true
export CLAUDE_STATS_PATH="/Users/suetakeshuuhei/MIRRALISM_V2/.mirralism/claude_stats.json"

echo "✅ ClaudeCode自動承認環境が設定されました"
echo "📋 設定内容:"
echo "   自動承認: ${CLAUDE_AUTO_APPROVE}"
echo "   モード: ${CLAUDE_AUTO_APPROVE_MODE}"
echo "   サイレント: ${CLAUDE_SILENT_MODE}"
echo "   プロジェクト: ${CLAUDE_PROJECT_ROOT}"