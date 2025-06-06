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
            "auto_approval": {"enabled": True, "mode": "aggressive"},
            "auto_approve_categories": {
                "file_operations": {"read_files": True, "edit_files": True},
                "code_operations": {"code_formatting": True},
                "git_operations": {"git_add": True, "git_commit": True}
            },
            "always_confirm": {
                "high_risk_operations": ["system_config_changes", "bulk_file_deletion"]
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
        """自動承認すべきか判定"""
        
        # 自動承認が無効の場合
        if not self.config.get("auto_approval", {}).get("enabled", False):
            return False, "自動承認が無効です"
        
        # リスクレベル評価
        risk_level, risk_reason = self.assess_risk_level(operation_type, details)
        
        if risk_level == "high":
            return False, f"高リスク操作のため手動確認が必要: {risk_reason}"
        
        # カテゴリ別自動承認チェック
        categories = self.config.get("auto_approve_categories", {})
        
        # ファイル操作
        if "file" in operation_type.lower():
            file_ops = categories.get("file_operations", {})
            if "read" in operation_type.lower() and file_ops.get("read_files", False):
                return True, "ファイル読み込み: 自動承認"
            if "edit" in operation_type.lower() and file_ops.get("edit_files", False):
                return True, "ファイル編集: 自動承認"
            if "create" in operation_type.lower() and file_ops.get("create_files", False):
                return True, "ファイル作成: 自動承認"
        
        # Git操作
        if "git" in operation_type.lower():
            git_ops = categories.get("git_operations", {})
            if "add" in operation_type.lower() and git_ops.get("git_add", False):
                return True, "Git add: 自動承認"
            if "commit" in operation_type.lower() and git_ops.get("git_commit", False):
                return True, "Git commit: 自動承認"
        
        # コード操作
        if any(word in operation_type.lower() for word in ["format", "lint", "test"]):
            code_ops = categories.get("code_operations", {})
            if code_ops.get("code_formatting", False):
                return True, "コード品質操作: 自動承認"
        
        # デフォルト: 手動確認
        return False, "該当カテゴリなし: 手動確認"

    def process_approval_request(self, operation: str, details: str = "") -> str:
        """承認リクエスト処理"""
        
        should_approve, reason = self.should_auto_approve(operation, details)
        
        # 統計更新
        self.update_stats(should_approve)
        
        if should_approve:
            self.logger.info(f"自動承認: {operation} - {reason}")
            if not self.config.get("notification_settings", {}).get("silent_approvals", False):
                print(f"✅ 自動承認: {operation}")
            return "yes"
        else:
            self.logger.warning(f"手動確認必要: {operation} - {reason}")
            print(f"⚠️ 手動確認が必要: {operation}")
            print(f"理由: {reason}")
            return "manual"

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