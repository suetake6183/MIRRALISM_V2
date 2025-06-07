#!/usr/bin/env python3
"""
ClaudeCode自動承認システム
===========================

ClaudeCodeの手動承認を大幅削減する自動承認システム
安全性を保ちながら、開発効率を向上させる

使用方法:
    python scripts/claude_auto_approver.py --enable
    python scripts/claude_auto_approver.py --status
    python scripts/claude_auto_approver.py --disable
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ClaudeAutoApprover:
    """ClaudeCode自動承認システム"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.config_path = self.project_root / ".mirralism" / "claude_auto_approval.json"
        self.log_path = self.project_root / ".mirralism" / "logs" / "auto_approval.log"
        
        # ログ設定
        self.setup_logging()
        
        # 設定読み込み
        self.config = self.load_config()
        
        self.logger.info("ClaudeCode自動承認システム初期化完了")

    def setup_logging(self):
        """ログ設定"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - CLAUDE_AUTO - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self) -> Dict:
        """設定ファイル読み込み"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("設定ファイルが見つかりません。デフォルト設定を使用します。")
            return self.get_default_config()
        except Exception as e:
            self.logger.error(f"設定ファイル読み込みエラー: {e}")
            return self.get_default_config()

    def get_default_config(self) -> Dict:
        """デフォルト設定"""
        return {
            "auto_approval": {"enabled": True, "mode": "ultra_aggressive"},
            "auto_approve_categories": {
                "file_operations": {
                    "read_files": True, 
                    "edit_files": True, 
                    "create_files": True,
                    "file_search": True,
                    "file_browse": True,
                    "multi_edit": True,
                    "write_files": True,
                    "file_open": True,
                    "cursor_open": True,
                    "ide_operations": True
                },
                "code_operations": {
                    "code_formatting": True,
                    "lint": True,
                    "test": True,
                    "build": True,
                    "run_scripts": True
                },
                "git_operations": {
                    "git_add": True, 
                    "git_commit": True,
                    "git_status": True,
                    "git_diff": True,
                    "git_log": True,
                    "git_branch": True,
                    "git_checkout": True
                },
                "system_operations": {
                    "date_check": True,
                    "directory_listing": True,
                    "file_globbing": True,
                    "search_operations": True,
                    "bash_commands": True,
                    "shell_execution": True
                },
                "mirralism_operations": {
                    "calculation_scripts": True,
                    "date_verification": True,
                    "data_analysis": True,
                    "todo_operations": True,
                    "task_management": True
                },
                "development_operations": {
                    "notebook_operations": True,
                    "jupyter_execute": True,
                    "python_execution": True,
                    "package_install": True
                }
            },
            "always_confirm": {
                "high_risk_operations": ["format disk", "system shutdown", "user deletion"],
                "critical_files": [".env", "id_rsa", "private_key"],
                "destructive_patterns": ["rm -rf /", "format c:", "drop database"]
            },
            "notification_settings": {
                "silent_approvals": True,
                "play_approval_sound": True,
                "show_approval_notifications": False
            },
            "usage_stats": {
                "auto_approvals_today": 0,
                "manual_confirmations_today": 0,
                "last_updated": None
            }
        }

    def save_config(self):
        """設定ファイル保存"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.logger.info("設定ファイルを保存しました")
        except Exception as e:
            self.logger.error(f"設定ファイル保存エラー: {e}")

    def assess_risk_level(self, operation: str, target: str = "") -> Tuple[str, str]:
        """操作のリスクレベル評価"""
        
        # 高リスク操作チェック
        high_risk_ops = self.config.get("always_confirm", {}).get("high_risk_operations", [])
        for risk_op in high_risk_ops:
            if risk_op.lower() in operation.lower():
                return "high", f"高リスク操作検出: {risk_op}"
        
        # 重要ファイルチェック
        critical_files = self.config.get("always_confirm", {}).get("critical_files", [])
        for critical_file in critical_files:
            if critical_file in target:
                return "high", f"重要ファイル操作: {critical_file}"
        
        # 破壊的パターンチェック
        destructive_patterns = self.config.get("always_confirm", {}).get("destructive_patterns", [])
        for pattern in destructive_patterns:
            if pattern.lower() in operation.lower() or pattern.lower() in target.lower():
                return "high", f"破壊的操作検出: {pattern}"
        
        # 通常操作
        return "low", "通常操作"

    def should_auto_approve(self, operation_type: str, details: str = "") -> Tuple[bool, str]:
        """自動承認すべきか判定（超積極的モード）"""
        
        # 自動承認が無効の場合
        if not self.config.get("auto_approval", {}).get("enabled", False):
            return False, "自動承認が無効です"
        
        # リスクレベル評価
        risk_level, risk_reason = self.assess_risk_level(operation_type, details)
        
        if risk_level == "high":
            return False, f"高リスク操作のため手動確認が必要: {risk_reason}"
        
        # カテゴリ別自動承認チェック
        categories = self.config.get("auto_approve_categories", {})
        
        # 超積極的モードでの包括的マッチング
        operation_lower = operation_type.lower()
        details_lower = details.lower()
        combined_text = f"{operation_lower} {details_lower}"
        
        # ファイル操作（超包括的判定）
        file_ops = categories.get("file_operations", {})
        if any(word in combined_text for word in ["file", "read", "browse", "view", "grep", "search", "find", "glob", "ls", "cat", "head", "tail", "write", "edit", "create", "modify", "update", "open", "opened", "cursor"]):
            if any(word in combined_text for word in ["read", "view", "browse", "contents", "cat", "head", "tail", "show", "display"]) and file_ops.get("read_files", True):
                return True, "ファイル読み込み: 自動承認"
            if any(word in combined_text for word in ["edit", "modify", "update", "change"]) and file_ops.get("edit_files", True):
                return True, "ファイル編集: 自動承認"
            if any(word in combined_text for word in ["create", "write", "new", "make"]) and file_ops.get("create_files", True):
                return True, "ファイル作成: 自動承認"
            if any(word in combined_text for word in ["search", "find", "grep", "glob"]) and file_ops.get("file_search", True):
                return True, "ファイル検索: 自動承認"
            if any(word in combined_text for word in ["browse", "list", "ls"]) and file_ops.get("file_browse", True):
                return True, "ファイルブラウズ: 自動承認"
            if any(word in combined_text for word in ["multi", "bulk", "batch"]) and file_ops.get("multi_edit", True):
                return True, "複数ファイル操作: 自動承認"
            if any(word in combined_text for word in ["open", "opened", "cursor", "ide"]) and file_ops.get("cursor_open", True):
                return True, "Cursor/IDEファイルオープン: 自動承認"
            return True, "ファイル操作（一般）: 自動承認"
        
        # システム操作（超包括的判定）
        system_ops = categories.get("system_operations", {})
        if any(word in combined_text for word in ["bash", "shell", "command", "execute", "run", "date", "time", "directory", "list", "glob", "search", "getdate", "check", "ls", "listing", "pwd", "cd", "mkdir", "chmod", "python", "node", "npm", "pip"]):
            if any(word in combined_text for word in ["bash", "shell", "execute", "run", "command", "python", "node", "npm", "pip", "script"]) and system_ops.get("bash_commands", True):
                return True, "Bashコマンド/スクリプト実行: 自動承認"
            if any(word in combined_text for word in ["date", "time", "getdate", "scripts/getdate"]) and system_ops.get("date_check", True):
                return True, "日付確認: 自動承認"
            if any(word in combined_text for word in ["directory", "list", "ls", "listing", "pwd"]) and system_ops.get("directory_listing", True):
                return True, "ディレクトリ一覧: 自動承認"
            if any(word in combined_text for word in ["glob", "pattern"]) and system_ops.get("file_globbing", True):
                return True, "ファイルグロブ: 自動承認"
            if any(word in combined_text for word in ["search", "grep", "find"]) and system_ops.get("search_operations", True):
                return True, "検索操作: 自動承認"
            return True, "システム操作（一般）: 自動承認"
        
        # MIRRALISM専用操作（超包括的判定）
        mirralism_ops = categories.get("mirralism_operations", {})
        if any(word in combined_text for word in ["mirralism", "calculation", "script", "node scripts", "calc", "todo", "task", "analysis", "data"]):
            if any(word in combined_text for word in ["todo", "task"]) and mirralism_ops.get("todo_operations", True):
                return True, "TODO/タスク操作: 自動承認"
            if any(word in combined_text for word in ["calculation", "calc", "scripts/", "node"]) and mirralism_ops.get("calculation_scripts", True):
                return True, "MIRRALISM計算スクリプト: 自動承認"
            if any(word in combined_text for word in ["analysis", "data"]) and mirralism_ops.get("data_analysis", True):
                return True, "MIRRALISMデータ分析: 自動承認"
            return True, "MIRRALISM操作（一般）: 自動承認"
        
        # Git操作（包括的判定）
        git_ops = categories.get("git_operations", {})
        if "git" in combined_text:
            if any(word in combined_text for word in ["add", "stage"]) and git_ops.get("git_add", True):
                return True, "Git add: 自動承認"
            if "commit" in combined_text and git_ops.get("git_commit", True):
                return True, "Git commit: 自動承認"
            if "status" in combined_text and git_ops.get("git_status", True):
                return True, "Git status: 自動承認"
            if "diff" in combined_text and git_ops.get("git_diff", True):
                return True, "Git diff: 自動承認"
            if "log" in combined_text and git_ops.get("git_log", True):
                return True, "Git log: 自動承認"
            if any(word in combined_text for word in ["branch", "checkout"]) and git_ops.get("git_branch", True):
                return True, "Git branch操作: 自動承認"
            return True, "Git操作（一般）: 自動承認"
        
        # コード操作（包括的判定）
        code_ops = categories.get("code_operations", {})
        if any(word in combined_text for word in ["format", "lint", "test", "build", "compile", "run", "execute", "python", "node", "npm", "pip"]):
            if any(word in combined_text for word in ["python", "execute", "run"]) and code_ops.get("run_scripts", True):
                return True, "スクリプト実行: 自動承認"
            if any(word in combined_text for word in ["format", "lint", "test", "build"]) and code_ops.get("code_formatting", True):
                return True, "コード品質操作: 自動承認"
            return True, "コード操作（一般）: 自動承認"
        
        # 開発操作（新カテゴリ）
        dev_ops = categories.get("development_operations", {})
        if any(word in combined_text for word in ["notebook", "jupyter", "python", "package", "install", "pip", "npm"]):
            if "notebook" in combined_text and dev_ops.get("notebook_operations", True):
                return True, "ノートブック操作: 自動承認"
            if any(word in combined_text for word in ["jupyter", "execute"]) and dev_ops.get("jupyter_execute", True):
                return True, "Jupyter実行: 自動承認"
            if "python" in combined_text and dev_ops.get("python_execution", True):
                return True, "Python実行: 自動承認"
            if any(word in combined_text for word in ["install", "pip", "npm"]) and dev_ops.get("package_install", True):
                return True, "パッケージインストール: 自動承認"
            return True, "開発操作（一般）: 自動承認"
        
        # 超積極的モード: ほぼ全てを自動承認
        if self.config.get("auto_approval", {}).get("mode") == "ultra_aggressive":
            # Cursor/IDEファイルオープン（最優先）
            if any(word in combined_text for word in ["opened", "cursor", "ide", "file in the ide"]):
                return True, "Cursor/IDEファイルオープン: 自動承認"
            
            # Bashコマンド（最優先）
            if any(word in combined_text for word in ["bash", "command", "shell", "execute", "run", "python", "node", "npm", "pip", "script"]):
                return True, "Bashコマンド/スクリプト: 自動承認"
            
            # 明らかに安全そうな操作はすべて自動承認
            safe_indicators = ["read", "view", "show", "list", "search", "find", "check", "status", "info", "help", "version", "open", "browse"]
            if any(word in combined_text for word in safe_indicators):
                return True, "安全操作として自動承認"
            
            # 開発関連の一般的な操作も自動承認
            dev_indicators = ["analyze", "process", "generate", "create", "update", "modify", "format", "organize", "test", "build", "install"]
            if any(word in combined_text for word in dev_indicators):
                return True, "開発操作として自動承認"
        
        # デフォルト: 手動確認（超積極的モードではより少ない）
        return False, "明確に危険な操作: 手動確認"

    def process_approval_request(self, operation: str, details: str = "") -> str:
        """承認リクエスト処理"""
        
        should_approve, reason = self.should_auto_approve(operation, details)
        
        # 統計更新
        self.update_stats(should_approve)
        
        if should_approve:
            self.logger.info(f"自動承認: {operation} - {reason}")
            
            # 承認音を再生
            if self.config.get("notification_settings", {}).get("play_approval_sound", True):
                self.play_approval_sound()
            
            if not self.config.get("notification_settings", {}).get("silent_approvals", True):
                print(f"✅ 自動承認: {operation}")
            return "yes"
        else:
            self.logger.warning(f"手動確認必要: {operation} - {reason}")
            
            # 手動確認が必要な時も音を再生
            self.play_approval_needed_sound()
            
            print(f"⚠️ 手動確認が必要: {operation}")
            print(f"理由: {reason}")
            return "manual"
    
    def play_approval_sound(self):
        """承認時の音を再生"""
        try:
            import subprocess
            # 軽やかな承認音
            subprocess.run(["afplay", "/System/Library/Sounds/Tink.aiff"], check=False)
        except:
            pass
    
    def play_approval_needed_sound(self):
        """手動確認が必要な時の音を再生"""
        try:
            import subprocess
            # 注意喚起音
            subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"], check=False)
        except:
            pass

    def update_stats(self, was_auto_approved: bool):
        """統計更新"""
        stats = self.config.get("usage_stats", {})
        today = datetime.now().strftime("%Y-%m-%d")
        
        if was_auto_approved:
            stats["auto_approvals_today"] = stats.get("auto_approvals_today", 0) + 1
        else:
            stats["manual_confirmations_today"] = stats.get("manual_confirmations_today", 0) + 1
        
        stats["last_updated"] = datetime.now().isoformat()
        self.config["usage_stats"] = stats
        self.save_config()

    def enable_auto_approval(self):
        """自動承認を有効化"""
        self.config["auto_approval"]["enabled"] = True
        self.save_config()
        print("✅ ClaudeCode自動承認システムが有効になりました")
        print("📋 設定:")
        print(f"   モード: {self.config['auto_approval'].get('mode', 'standard')}")
        print("   ファイル操作: 自動承認")
        print("   Git操作: 自動承認") 
        print("   コード品質: 自動承認")
        print("   高リスク操作: 手動確認")

    def disable_auto_approval(self):
        """自動承認を無効化"""
        self.config["auto_approval"]["enabled"] = False
        self.save_config()
        print("⚠️ ClaudeCode自動承認システムが無効になりました")
        print("すべての操作で手動確認が必要です")

    def show_status(self):
        """現在の状態表示"""
        enabled = self.config.get("auto_approval", {}).get("enabled", False)
        stats = self.config.get("usage_stats", {})
        
        print("📊 ClaudeCode自動承認システム状態")
        print("=" * 40)
        print(f"状態: {'✅ 有効' if enabled else '❌ 無効'}")
        print(f"モード: {self.config.get('auto_approval', {}).get('mode', 'standard')}")
        print(f"本日の自動承認: {stats.get('auto_approvals_today', 0)}件")
        print(f"本日の手動確認: {stats.get('manual_confirmations_today', 0)}件")
        print(f"最終更新: {stats.get('last_updated', 'なし')}")
        
        if enabled:
            print("\n🔄 自動承認対象:")
            categories = self.config.get("auto_approve_categories", {})
            for category, settings in categories.items():
                enabled_ops = [k for k, v in settings.items() if v]
                if enabled_ops:
                    print(f"   {category}: {', '.join(enabled_ops)}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="ClaudeCode自動承認システム")
    parser.add_argument("--enable", action="store_true", help="自動承認を有効化")
    parser.add_argument("--disable", action="store_true", help="自動承認を無効化")
    parser.add_argument("--status", action="store_true", help="現在の状態を表示")
    parser.add_argument("--operation", type=str, help="操作タイプ")
    parser.add_argument("--details", type=str, default="", help="操作詳細")
    
    args = parser.parse_args()
    
    approver = ClaudeAutoApprover()
    
    if args.enable:
        approver.enable_auto_approval()
    elif args.disable:
        approver.disable_auto_approval()
    elif args.status:
        approver.show_status()
    elif args.operation:
        result = approver.process_approval_request(args.operation, args.details)
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()