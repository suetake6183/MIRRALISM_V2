#!/bin/bash
# ClaudeCode通知システム統合スクリプト
# ==================================
#
# ClaudeCodeでの作業完了を自動検出して通知するシェル統合
#
# 使用方法:
#     source scripts/claude_notify_integration.sh
#     claude_notify "echo '作業完了しました'"
#     done "カスタムメッセージ"

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# ClaudeCode通知関数
claude_notify() {
    local command="$@"
    echo "🚀 ClaudeCode監視実行: $command"
    python3 "$SCRIPT_DIR/claude_auto_notify_wrapper.py" --wrap -- $command
}

# 手動完了通知関数
notify_done() {
    local message="${1:-作業が完了しました}"
    echo "🔊 完了通知: $message"
    python3 "$SCRIPT_DIR/claude_completion_notifier.py" --custom "$message"
}

# 成功通知
notify_success() {
    local message="${1:-作業が正常に完了しました}"
    python3 "$SCRIPT_DIR/claude_completion_notifier.py" --play success --custom "$message"
}

# エラー通知
notify_error() {
    local message="${1:-エラーが発生しました}"
    python3 "$SCRIPT_DIR/claude_completion_notifier.py" --play error --custom "$message"
}

# 警告通知
notify_warning() {
    local message="${1:-警告: 注意が必要です}"
    python3 "$SCRIPT_DIR/claude_completion_notifier.py" --play warning --custom "$message"
}

# 通知システムの状態確認
notify_status() {
    python3 "$SCRIPT_DIR/claude_completion_notifier.py" --status
}

# 通知テスト
notify_test() {
    python3 "$SCRIPT_DIR/claude_completion_notifier.py" --test
}

# エイリアス設定
alias cn='claude_notify'
alias done='notify_done'
alias success='notify_success'
alias error='notify_error'
alias warning='notify_warning'
alias notify='notify_done'

# MIRRALISM専用エイリアス
alias mirralism_done='notify_success "MIRRALISM作業が完了しました"'
alias personality_done='notify_success "PersonalityLearning処理が完了しました"'
alias integration_done='notify_success "統合処理が完了しました"'

# 使用方法表示
show_claude_notify_help() {
    echo "🔊 ClaudeCode通知システム - 使用方法"
    echo "================================="
    echo ""
    echo "📋 基本コマンド:"
    echo "  claude_notify <command>     - コマンドを監視付きで実行"
    echo "  cn <command>                - claude_notifyの短縮形"
    echo "  done [message]              - 手動完了通知"
    echo "  success [message]           - 成功通知"
    echo "  error [message]             - エラー通知"
    echo "  warning [message]           - 警告通知"
    echo ""
    echo "🎯 MIRRALISM専用:"
    echo "  mirralism_done              - MIRRALISM作業完了通知"
    echo "  personality_done            - PersonalityLearning完了通知"
    echo "  integration_done            - 統合処理完了通知"
    echo ""
    echo "🔧 システム:"
    echo "  notify_status               - 通知システム状態確認"
    echo "  notify_test                 - 通知テスト実行"
    echo ""
    echo "💡 使用例:"
    echo "  cn git status               - git statusを監視付きで実行"
    echo "  done '48時間実装完了'        - カスタム完了メッセージ"
    echo "  success                     - デフォルト成功通知"
    echo "  mirralism_done              - MIRRALISM完了通知"
}

# ヘルプエイリアス
alias claude_help='show_claude_notify_help'
alias notify_help='show_claude_notify_help'

# 初期化メッセージ
echo "✅ ClaudeCode通知システム統合完了"
echo "💡 'claude_help' で使用方法を確認できます"

# 自動通知を有効化
python3 "$SCRIPT_DIR/claude_completion_notifier.py" --enable-auto > /dev/null 2>&1