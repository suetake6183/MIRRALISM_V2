#!/bin/bash
# ClaudeCode 完全自動化マネージャー
# ================================
# 
# 目的: 全ての自動化ツールを統合管理
# 方針: シンプル・確実・即座実行
# 作成日: 2025年6月6日

# 設定
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_ROOT/.mirralism"
PYTHON_CLICKER="$SCRIPT_DIR/claude_auto_clicker.py"
SWIFT_CLICKER="$SCRIPT_DIR/claude_auto_clicker_app.swift"
APPLESCRIPT_CLICKER="$SCRIPT_DIR/claude_auto_clicker.applescript"

# ログファイル
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/claude_auto_manager.log"

# ログ関数
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ヘルプ表示
show_help() {
    cat << EOF
🤖 ClaudeCode 完全自動化マネージャー
===============================

MIRRALISM V2プロジェクト専用の確認ダイアログ自動化ツール

使用方法:
  $0 [COMMAND] [OPTIONS]

コマンド:
  start [METHOD]     自動化開始 (METHOD: python|swift|applescript)
  stop               全ての自動化停止
  status             現在の状態確認
  install            依存関係インストール
  test              各ツールのテスト実行
  config            設定変更・確認
  logs              ログ表示

メソッド:
  python            Python版 (推奨) - 高機能・設定可能
  swift             Swift版 - ネイティブ・高速
  applescript       AppleScript版 - シンプル・軽量

例:
  $0 start python    # Python版で自動化開始
  $0 start           # デフォルト(Python)で開始
  $0 stop            # 停止
  $0 status          # 状態確認

設定ファイル: $LOG_DIR/claude_auto_clicker_config.json
ログファイル: $LOG_FILE

EOF
}

# 依存関係インストール
install_dependencies() {
    log_message "📦 依存関係インストール開始"
    
    # Python依存関係
    log_message "Python依存関係インストール中..."
    pip3 install pyautogui opencv-python >/dev/null 2>&1
    
    # Swift実行可能ファイル作成
    if [ -f "$SWIFT_CLICKER" ]; then
        log_message "Swift版コンパイル中..."
        swift -o "$SCRIPT_DIR/claude_auto_clicker_app" "$SWIFT_CLICKER" 2>/dev/null
        if [ $? -eq 0 ]; then
            log_message "✅ Swift版コンパイル完了"
        else
            log_message "⚠️ Swift版コンパイル失敗（オプション機能）"
        fi
    fi
    
    log_message "✅ 依存関係インストール完了"
}

# Python版開始
start_python() {
    log_message "🐍 Python版自動クリック開始"
    
    if [ ! -f "$PYTHON_CLICKER" ]; then
        log_message "❌ Python版スクリプトが見つかりません: $PYTHON_CLICKER"
        return 1
    fi
    
    # バックグラウンドで実行
    python3 "$PYTHON_CLICKER" --start &
    PYTHON_PID=$!
    echo $PYTHON_PID > "$LOG_DIR/claude_auto_clicker_python.pid"
    
    log_message "✅ Python版開始 (PID: $PYTHON_PID)"
    echo "Python版自動クリックが開始されました"
    echo "停止: $0 stop"
}

# Swift版開始
start_swift() {
    log_message "🔥 Swift版自動クリック開始"
    
    local swift_executable="$SCRIPT_DIR/claude_auto_clicker_app"
    
    if [ ! -f "$swift_executable" ]; then
        log_message "Swift実行ファイルが見つかりません。コンパイル中..."
        swift -o "$swift_executable" "$SWIFT_CLICKER" 2>/dev/null
        if [ $? -ne 0 ]; then
            log_message "❌ Swift版コンパイル失敗"
            return 1
        fi
    fi
    
    # バックグラウンドで実行
    "$swift_executable" &
    SWIFT_PID=$!
    echo $SWIFT_PID > "$LOG_DIR/claude_auto_clicker_swift.pid"
    
    log_message "✅ Swift版開始 (PID: $SWIFT_PID)"
    echo "Swift版自動クリックが開始されました"
    echo "停止: $0 stop"
}

# AppleScript版開始
start_applescript() {
    log_message "🍎 AppleScript版自動クリック開始"
    
    if [ ! -f "$APPLESCRIPT_CLICKER" ]; then
        log_message "❌ AppleScript版スクリプトが見つかりません: $APPLESCRIPT_CLICKER"
        return 1
    fi
    
    # AppleScript実行
    osascript "$APPLESCRIPT_CLICKER" &
    APPLESCRIPT_PID=$!
    echo $APPLESCRIPT_PID > "$LOG_DIR/claude_auto_clicker_applescript.pid"
    
    log_message "✅ AppleScript版開始 (PID: $APPLESCRIPT_PID)"
    echo "AppleScript版自動クリックが開始されました"
    echo "停止: $0 stop または AppleScript Editor"
}

# 自動化開始
start_automation() {
    local method="${1:-python}"  # デフォルトはPython
    
    log_message "🚀 自動化開始: $method"
    
    # 既存プロセスチェック
    if is_running; then
        echo "既に自動化が実行中です"
        show_status
        return 1
    fi
    
    case "$method" in
        python|py)
            start_python
            ;;
        swift)
            start_swift
            ;;
        applescript|applescript)
            start_applescript
            ;;
        *)
            echo "❌ 未知のメソッド: $method"
            echo "利用可能: python, swift, applescript"
            return 1
            ;;
    esac
}

# 全停止
stop_automation() {
    log_message "🛑 自動化停止開始"
    
    local stopped=false
    
    # Python版停止
    if [ -f "$LOG_DIR/claude_auto_clicker_python.pid" ]; then
        local pid=$(cat "$LOG_DIR/claude_auto_clicker_python.pid")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            rm -f "$LOG_DIR/claude_auto_clicker_python.pid"
            log_message "✅ Python版停止 (PID: $pid)"
            stopped=true
        fi
    fi
    
    # Swift版停止
    if [ -f "$LOG_DIR/claude_auto_clicker_swift.pid" ]; then
        local pid=$(cat "$LOG_DIR/claude_auto_clicker_swift.pid")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            rm -f "$LOG_DIR/claude_auto_clicker_swift.pid"
            log_message "✅ Swift版停止 (PID: $pid)"
            stopped=true
        fi
    fi
    
    # AppleScript版停止
    if [ -f "$LOG_DIR/claude_auto_clicker_applescript.pid" ]; then
        local pid=$(cat "$LOG_DIR/claude_auto_clicker_applescript.pid")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            rm -f "$LOG_DIR/claude_auto_clicker_applescript.pid"
            log_message "✅ AppleScript版停止 (PID: $pid)"
            stopped=true
        fi
    fi
    
    # 強制停止（念のため）
    pkill -f "claude_auto_clicker" 2>/dev/null
    
    if [ "$stopped" = true ]; then
        echo "✅ 自動化停止完了"
    else
        echo "ℹ️ 実行中の自動化はありませんでした"
    fi
    
    log_message "🛑 自動化停止完了"
}

# 実行中チェック
is_running() {
    # PIDファイルチェック
    for pidfile in "$LOG_DIR/claude_auto_clicker_"*.pid; do
        if [ -f "$pidfile" ]; then
            local pid=$(cat "$pidfile")
            if kill -0 "$pid" 2>/dev/null; then
                return 0  # 実行中
            else
                rm -f "$pidfile"  # 無効なPIDファイル削除
            fi
        fi
    done
    
    # プロセス名でもチェック
    if pgrep -f "claude_auto_clicker" >/dev/null 2>&1; then
        return 0  # 実行中
    fi
    
    return 1  # 停止中
}

# 状態表示
show_status() {
    echo "📊 ClaudeCode自動化マネージャー状態"
    echo "=================================="
    
    local running_status="⏹️ 停止中"
    local active_methods=()
    
    # 各バージョンの状態チェック
    if [ -f "$LOG_DIR/claude_auto_clicker_python.pid" ]; then
        local pid=$(cat "$LOG_DIR/claude_auto_clicker_python.pid")
        if kill -0 "$pid" 2>/dev/null; then
            active_methods+=("Python(PID:$pid)")
            running_status="✅ 実行中"
        fi
    fi
    
    if [ -f "$LOG_DIR/claude_auto_clicker_swift.pid" ]; then
        local pid=$(cat "$LOG_DIR/claude_auto_clicker_swift.pid")
        if kill -0 "$pid" 2>/dev/null; then
            active_methods+=("Swift(PID:$pid)")
            running_status="✅ 実行中"
        fi
    fi
    
    if [ -f "$LOG_DIR/claude_auto_clicker_applescript.pid" ]; then
        local pid=$(cat "$LOG_DIR/claude_auto_clicker_applescript.pid")
        if kill -0 "$pid" 2>/dev/null; then
            active_methods+=("AppleScript(PID:$pid)")
            running_status="✅ 実行中"
        fi
    fi
    
    echo "状態: $running_status"
    if [ ${#active_methods[@]} -gt 0 ]; then
        echo "実行中: ${active_methods[*]}"
    fi
    
    # 設定確認
    if [ -f "$LOG_DIR/claude_auto_clicker_config.json" ]; then
        echo "設定ファイル: 存在"
        if command -v python3 >/dev/null && [ -f "$PYTHON_CLICKER" ]; then
            python3 "$PYTHON_CLICKER" --status 2>/dev/null | grep -E "(状態|モード|総クリック数)" || true
        fi
    else
        echo "設定ファイル: 未作成"
    fi
    
    echo "ログファイル: $LOG_FILE"
    echo ""
    echo "コマンド:"
    echo "  開始: $0 start [python|swift|applescript]"
    echo "  停止: $0 stop"
    echo "  設定: $0 config"
}

# 設定変更
configure() {
    if [ ! -f "$PYTHON_CLICKER" ]; then
        echo "❌ Python版が必要です"
        return 1
    fi
    
    echo "⚙️ 設定変更メニュー"
    echo "=================="
    echo "1. 現在の設定表示"
    echo "2. 自動化有効/無効切り替え"
    echo "3. スキャン間隔変更"
    echo "4. モード変更"
    echo ""
    read -p "選択 (1-4): " choice
    
    case "$choice" in
        1)
            python3 "$PYTHON_CLICKER" --status
            ;;
        2)
            echo "現在の設定:"
            python3 "$PYTHON_CLICKER" --status | grep "有効"
            echo ""
            read -p "有効にしますか？ (y/n): " enable
            if [ "$enable" = "y" ]; then
                python3 "$PYTHON_CLICKER" --enable
            else
                python3 "$PYTHON_CLICKER" --disable
            fi
            ;;
        3)
            read -p "新しいスキャン間隔(秒): " interval
            python3 "$PYTHON_CLICKER" --interval "$interval"
            ;;
        4)
            echo "モード選択:"
            echo "  aggressive: 積極的自動化"
            echo "  conservative: 保守的自動化"
            echo "  claude_only: Claude関連のみ"
            read -p "モード: " mode
            python3 "$PYTHON_CLICKER" --mode "$mode"
            ;;
        *)
            echo "❌ 無効な選択"
            ;;
    esac
}

# テスト実行
test_tools() {
    echo "🧪 ツールテスト実行"
    echo "=================="
    
    # Python版テスト
    echo "Python版テスト:"
    if python3 "$PYTHON_CLICKER" --status >/dev/null 2>&1; then
        echo "  ✅ Python版 OK"
    else
        echo "  ❌ Python版 NG"
    fi
    
    # Swift版テスト
    echo "Swift版テスト:"
    if swift --version >/dev/null 2>&1; then
        echo "  ✅ Swift OK"
    else
        echo "  ❌ Swift NG"
    fi
    
    # AppleScript版テスト
    echo "AppleScript版テスト:"
    if osascript -e 'return "test"' >/dev/null 2>&1; then
        echo "  ✅ AppleScript OK"
    else
        echo "  ❌ AppleScript NG"
    fi
    
    echo ""
    echo "推奨設定:"
    echo "  メイン: Python版 (高機能)"
    echo "  軽量: AppleScript版 (シンプル)"
    echo "  高速: Swift版 (ネイティブ)"
}

# ログ表示
show_logs() {
    echo "📋 最新ログ (最後20行)"
    echo "===================="
    if [ -f "$LOG_FILE" ]; then
        tail -20 "$LOG_FILE"
    else
        echo "ログファイルが見つかりません"
    fi
    
    echo ""
    echo "全ログ表示: tail -f $LOG_FILE"
}

# メイン処理
main() {
    case "${1:-help}" in
        start)
            start_automation "$2"
            ;;
        stop)
            stop_automation
            ;;
        status)
            show_status
            ;;
        install)
            install_dependencies
            ;;
        test)
            test_tools
            ;;
        config)
            configure
            ;;
        logs)
            show_logs
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "❌ 未知のコマンド: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 実行
main "$@"