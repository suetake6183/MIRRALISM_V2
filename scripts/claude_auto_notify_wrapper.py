#!/usr/bin/env python3
"""
ClaudeCode自動通知ラッパー
========================

ClaudeCodeの出力を監視して自動的に作業完了通知を送信するシステム
標準出力を監視して、完了パターンを検出すると自動通知

使用方法:
    # ClaudeCodeコマンドをラップして実行
    python scripts/claude_auto_notify_wrapper.py "claude-code status"
    
    # 既存のプロセスの出力を監視
    echo "作業が完了しました" | python scripts/claude_auto_notify_wrapper.py --monitor
"""

import argparse
import re
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import List, Optional

# claude_completion_notifierをインポート
sys.path.append(str(Path(__file__).parent))
from claude_completion_notifier import ClaudeCompletionNotifier


class ClaudeAutoNotifyWrapper:
    """ClaudeCode自動通知ラッパー"""
    
    def __init__(self):
        self.notifier = ClaudeCompletionNotifier()
        self.monitoring = False
        
        # 完了検出パターン
        self.completion_patterns = [
            # 日本語パターン
            r'(完了|終了|成功|できました|しました)(?:\s|$|。)',
            r'✅.*(?:完了|成功|終了)',
            r'❌.*(?:エラー|失敗|問題)',
            r'⚠️.*(?:警告|注意|確認)',
            
            # 英語パターン  
            r'(completed?|finished?|success|done)(?:\s|$|\.)',
            r'✅.*(?:completed?|success|done)',
            r'❌.*(?:error|failed?|problem)',
            r'⚠️.*(?:warning|caution|attention)',
            
            # 技術的完了パターン
            r'Process completed',
            r'Task finished',
            r'Build successful',
            r'Tests passed',
            r'Installation complete',
            
            # MIRRALISM特有パターン
            r'MIRRALISM.*(?:完了|成功)',
            r'PersonalityLearning.*(?:完了|更新)',
            r'統合.*(?:完了|成功)',
            r'実装.*(?:完了|成功)'
        ]
        
        # エラー検出パターン
        self.error_patterns = [
            r'error:|Error:|ERROR:',
            r'exception:|Exception:|EXCEPTION:',
            r'failed:|Failed:|FAILED:',
            r'❌',
            r'エラー|失敗|例外'
        ]
        
        # 警告検出パターン
        self.warning_patterns = [
            r'warning:|Warning:|WARNING:',
            r'caution:|Caution:|CAUTION:',
            r'⚠️',
            r'警告|注意|確認が必要'
        ]

    def detect_completion_in_text(self, text: str) -> Optional[str]:
        """テキストから完了タイプを検出"""
        text_clean = text.strip()
        
        # エラーパターンチェック（優先度高）
        for pattern in self.error_patterns:
            if re.search(pattern, text_clean, re.IGNORECASE):
                return "error"
        
        # 警告パターンチェック
        for pattern in self.warning_patterns:
            if re.search(pattern, text_clean, re.IGNORECASE):
                return "warning"
        
        # 完了パターンチェック
        for pattern in self.completion_patterns:
            if re.search(pattern, text_clean, re.IGNORECASE):
                return "success"
        
        return None

    def monitor_output(self, process: subprocess.Popen):
        """プロセス出力を監視"""
        if not process.stdout:
            return
            
        lines_buffer = []
        
        for line in iter(process.stdout.readline, b''):
            try:
                line_text = line.decode('utf-8').strip()
                if line_text:
                    print(line_text)  # 元の出力も表示
                    lines_buffer.append(line_text)
                    
                    # 最新5行を監視対象とする
                    if len(lines_buffer) > 5:
                        lines_buffer.pop(0)
                    
                    # 完了検出
                    combined_text = '\n'.join(lines_buffer)
                    completion_type = self.detect_completion_in_text(combined_text)
                    
                    if completion_type:
                        # 通知送信
                        self.notifier.notify_completion(
                            message=line_text[:100] + ("..." if len(line_text) > 100 else ""),
                            completion_type=completion_type
                        )
                        lines_buffer.clear()  # バッファクリア
                        
            except UnicodeDecodeError:
                # バイナリ出力はスキップ
                continue

    def wrap_command(self, command: List[str]):
        """コマンドをラップして実行・監視"""
        try:
            print(f"🚀 ClaudeCode監視開始: {' '.join(command)}")
            
            # プロセス開始
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=False
            )
            
            # 出力監視スレッド開始
            monitor_thread = threading.Thread(
                target=self.monitor_output, 
                args=(process,)
            )
            monitor_thread.daemon = True
            monitor_thread.start()
            
            # プロセス完了まで待機
            return_code = process.wait()
            
            # 監視スレッド終了まで少し待機
            monitor_thread.join(timeout=2)
            
            # 最終通知
            if return_code == 0:
                self.notifier.notify_completion(
                    "コマンド実行が正常に完了しました",
                    "success"
                )
            else:
                self.notifier.notify_completion(
                    f"コマンド実行がエラーで終了しました (exit code: {return_code})",
                    "error"
                )
            
            return return_code
            
        except KeyboardInterrupt:
            print("\n⚠️ 実行が中断されました")
            self.notifier.notify_completion(
                "コマンド実行が中断されました",
                "warning"
            )
            return 1
        except Exception as e:
            print(f"❌ エラー: {e}")
            self.notifier.notify_completion(
                f"実行エラー: {str(e)}",
                "error"
            )
            return 1

    def monitor_stdin(self):
        """標準入力を監視"""
        print("📨 標準入力監視開始 (Ctrl+Cで終了)")
        
        try:
            while True:
                line = input()
                if line.strip():
                    completion_type = self.detect_completion_in_text(line)
                    if completion_type:
                        self.notifier.notify_completion(
                            line[:100] + ("..." if len(line) > 100 else ""),
                            completion_type
                        )
        except KeyboardInterrupt:
            print("\n📨 監視終了")
        except EOFError:
            print("\n📨 入力終了")

    def setup_shell_integration(self):
        """シェル統合セットアップ"""
        shell_script = '''
# ClaudeCode自動通知統合
claude_notify() {
    local command="$@"
    echo "🚀 ClaudeCode監視実行: $command"
    python3 "%(script_path)s" --wrap -- $command
}

# エイリアス設定
alias cn='claude_notify'
alias claude-notify='claude_notify'

# 完了通知関数
notify_done() {
    local message="${1:-作業が完了しました}"
    python3 "%(script_path)s" --notify "$message"
}

alias done='notify_done'
''' % {"script_path": Path(__file__).resolve()}
        
        print("🔧 シェル統合用スクリプト:")
        print("=" * 50)
        print(shell_script)
        print("=" * 50)
        print("📋 使用方法:")
        print("1. 上記スクリプトを ~/.bashrc または ~/.zshrc に追加")
        print("2. source ~/.bashrc (または ~/.zshrc) で再読み込み")
        print("3. claude_notify <コマンド> で監視付き実行")
        print("4. done で手動完了通知")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="ClaudeCode自動通知ラッパー")
    parser.add_argument("--wrap", action="store_true", help="コマンドをラップして実行")
    parser.add_argument("--monitor", action="store_true", help="標準入力を監視")
    parser.add_argument("--notify", type=str, help="手動で通知送信")
    parser.add_argument("--setup", action="store_true", help="シェル統合セットアップ")
    parser.add_argument("command", nargs="*", help="実行するコマンド")
    
    args = parser.parse_args()
    wrapper = ClaudeAutoNotifyWrapper()
    
    if args.notify:
        wrapper.notifier.notify_completion(args.notify)
    elif args.setup:
        wrapper.setup_shell_integration()
    elif args.monitor:
        wrapper.monitor_stdin()
    elif args.wrap and args.command:
        return wrapper.wrap_command(args.command)
    elif args.command:
        # --wrap が指定されていない場合でも、コマンドがあれば実行
        return wrapper.wrap_command(args.command)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())