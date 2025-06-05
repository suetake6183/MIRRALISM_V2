#!/usr/bin/env python3
"""
MIRRALISM V2 柔軟ファイル自動整理システム
=====================================

V1失敗教訓：
- REDIRECTファイル28,066個の無制限生成
- ファイル制限の固定化による実用性欠如
- 分類・命名規則の統一不足

V2改善：
- 段階的警告＋承認制システム
- プロジェクトモード（期間限定制限緩和）
- インテリジェント検出・予防
- 柔軟な制限調整機能
"""

import datetime
import json
import logging
import os
import re
import shutil
from pathlib import Path
from typing import Dict
from typing import Tuple

# ログ設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FlexibleFileOrganizer:
    """柔軟ファイル自動整理システム"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.config_file = self.root_dir / "scripts" / "organizer_config.json"
        self.stats_file = self.root_dir / "Data" / "analytics" / "file_stats.json"
        self.load_config()
        self.ensure_directories()

    def load_config(self):
        """設定ファイル読み込み・初期化"""
        default_config = {
            "current_mode": "normal",
            "daily_limits": {"normal": 50, "analysis": 200, "migration": 500},
            "warning_levels": {
                "notification": 50,
                "confirmation": 100,
                "detailed_approval": 200,
            },
            "file_rules": {
                "analysis": {
                    "patterns": ["*_analysis_*.txt", "*_analysis_*.md"],
                    "destination": "Data/analytics/",
                },
                "reports": {
                    "patterns": ["*_report_*.md", "*_test_results.txt"],
                    "destination": "Documentation/reports/",
                },
                "strategy": {
                    "patterns": [
                        "STRATEGIC_*.md",
                        "*_BRIEFING.md",
                        "*_REQUIRED_*.md",
                    ],
                    "destination": "Documentation/strategy/",
                },
                "migration": {
                    "patterns": ["*_compatibility_*.md", "*migration*.md"],
                    "destination": "Documentation/migration/",
                },
                "temp": {
                    "patterns": ["temp_*.txt", "*.tmp", "*.log"],
                    "destination": "Data/temp/",
                    "retention_days": 7,
                },
                "forbidden": {
                    "patterns": ["*REDIRECT*", "*_duplicate_*", "*コピー*"],
                    "action": "block",
                    "reason": "V1失敗パターン検出",
                },
            },
            "today_stats": {
                "date": "",
                "files_created": 0,
                "warnings_issued": 0,
                "manual_approvals": 0,
            },
        }

        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
                # 新しいキーがあれば追加
                for key, value in default_config.items():
                    if key not in self.config:
                        self.config[key] = value
        else:
            self.config = default_config

        # 日付チェック・リセット
        today = datetime.date.today().isoformat()
        if self.config["today_stats"]["date"] != today:
            self.config["today_stats"] = {
                "date": today,
                "files_created": 0,
                "warnings_issued": 0,
                "manual_approvals": 0,
            }
            self.save_config()

        # オートラン設定のデフォルト値追加
        if "auto_run" not in self.config:
            self.config["auto_run"] = {
                "enabled": False,
                "default_action": "clean_mess",
                "auto_confirm": True,
                "auto_mode": "migration",
                "schedule": {"enabled": False, "interval_hours": 24, "last_run": ""},
                "safety": {
                    "max_files_per_run": 100,
                    "backup_before_move": False,
                    "dry_run_first": False,
                },
            }
            self.save_config()

    def save_config(self):
        """設定ファイル保存"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def ensure_directories(self):
        """必要ディレクトリの存在確認・作成"""
        dirs = [
            "Data/analytics",
            "Data/temp",
            "Documentation/reports",
            "Documentation/strategy",
            "Documentation/migration",
            "scripts",
        ]
        for dir_path in dirs:
            (self.root_dir / dir_path).mkdir(parents=True, exist_ok=True)

    def get_current_limit(self) -> int:
        """現在の制限値取得"""
        mode = self.config["current_mode"]
        return self.config["daily_limits"][mode]

    def set_project_mode(self, mode: str):
        """プロジェクトモード設定"""
        if mode in self.config["daily_limits"]:
            self.config["current_mode"] = mode
            self.save_config()
            logger.info(
                f"Project mode set to '{mode}': {self.get_current_limit()} files/day"
            )
            return True
        return False

    def set_daily_limit(self, limit: int, reason: str = "Manual adjustment"):
        """今日の制限を動的変更"""
        mode = self.config["current_mode"]
        self.config["daily_limits"][mode] = limit
        self.config["today_stats"]["manual_approvals"] += 1
        self.save_config()
        logger.info(f"Daily limit adjusted to {limit}: {reason}")

    def classify_file(self, file_path: str) -> Tuple[str, str]:
        """ファイル分類・移動先決定"""
        file_name = os.path.basename(file_path)

        for category, rules in self.config["file_rules"].items():
            for pattern in rules["patterns"]:
                if self._match_pattern(file_name, pattern):
                    if category == "forbidden":
                        return "forbidden", rules.get("reason", "Forbidden file type")
                    return category, rules["destination"]

        return "unknown", "Data/temp/"

    def _match_pattern(self, filename: str, pattern: str) -> bool:
        """パターンマッチング（ワイルドカード対応）"""
        regex_pattern = pattern.replace("*", ".*").replace("?", ".")
        return bool(re.match(regex_pattern, filename, re.IGNORECASE))

    def clean_current_mess(self) -> Dict[str, int]:
        """現在の散らかり状況を整理"""
        results = {"moved": 0, "errors": 0, "skipped": 0}

        print("🧹 現在の散らかったファイルを整理中...")

        # ルートディレクトリの対象ファイル検出
        target_files = []
        for item in self.root_dir.iterdir():
            if item.is_file() and not item.name.startswith("."):
                category, _ = self.classify_file(item.name)
                if category != "unknown":
                    target_files.append(item)

        print(f"📁 {len(target_files)}個のファイルを整理します")

        # 一時的にmigrationモードに切り替え
        original_mode = self.config["current_mode"]
        self.set_project_mode("migration")

        for file_path in target_files:
            success, message = self.organize_file(str(file_path))
            if success:
                results["moved"] += 1
                print(f"  ✅ {file_path.name}")
            else:
                results["errors"] += 1
                print(f"  ❌ {file_path.name}: {message}")

        # 元のモードに戻す
        self.config["current_mode"] = original_mode
        self.save_config()

        return results

    def assess_risk_level(self, target_files: list) -> tuple[bool, str, list]:
        """危険度判定とリスクファイル特定"""
        safety_config = self.config.get("auto_run", {}).get("safety", {})
        force_conditions = safety_config.get("force_confirm_conditions", {})
        high_risk_patterns = safety_config.get("high_risk_patterns", [])

        risk_factors = []
        high_risk_files = []
        force_confirm = False

        # ファイル数チェック
        threshold = force_conditions.get("file_count_threshold", 50)
        if len(target_files) >= threshold:
            risk_factors.append(f"大量ファイル操作: {len(target_files)}件 (閾値: {threshold})")
            force_confirm = True

        # 重要ファイルチェック
        for file_path in target_files:
            file_name = file_path.name
            file_size_mb = file_path.stat().st_size / (1024 * 1024)

            # サイズチェック
            size_threshold = force_conditions.get("large_file_size_mb", 10)
            if file_size_mb > size_threshold:
                risk_factors.append(f"大容量ファイル: {file_name} ({file_size_mb:.1f}MB)")
                high_risk_files.append(file_path)
                force_confirm = True

            # パターンマッチング
            for pattern in high_risk_patterns:
                import fnmatch

                if fnmatch.fnmatch(file_name, pattern):
                    risk_factors.append(f"重要ファイル: {file_name} (パターン: {pattern})")
                    high_risk_files.append(file_path)

                    # 特に重要なファイルは強制確認
                    critical_files = ["CLAUDE.md", "README.md", "package.json", "*.py"]
                    if any(fnmatch.fnmatch(file_name, crit) for crit in critical_files):
                        force_confirm = True

        # 禁止パターンチェック
        forbidden_patterns = (
            self.config.get("file_rules", {}).get("forbidden", {}).get("patterns", [])
        )
        for file_path in target_files:
            for pattern in forbidden_patterns:
                import fnmatch

                if fnmatch.fnmatch(file_path.name, pattern):
                    risk_factors.append(f"禁止パターン検出: {file_path.name}")
                    force_confirm = True

        return force_confirm, risk_factors, high_risk_files

    def auto_run_cleanup(self) -> Dict[str, int]:
        """オートラン：自動整理実行"""
        if not self.config.get("auto_run", {}).get("enabled", False):
            print("⚠️ オートランが無効です。設定を確認してください。")
            return {"moved": 0, "errors": 0, "skipped": 0}

        auto_config = self.config["auto_run"]
        safety_config = auto_config.get("safety", {})

        print("🤖 オートラン自動整理開始...")
        print(f"🎯 モード: {auto_config.get('auto_mode', 'migration')}")
        print(f"🔧 アクション: {auto_config.get('default_action', 'clean_mess')}")

        # 安全制限チェック
        max_files = safety_config.get("max_files_per_run", 100)

        # ルートディレクトリの対象ファイル検出
        target_files = []
        for item in self.root_dir.iterdir():
            if item.is_file() and not item.name.startswith("."):
                category, _ = self.classify_file(item.name)
                if category != "unknown":
                    target_files.append(item)

        if len(target_files) > max_files:
            print(f"⚠️ ファイル数が制限を超えています: {len(target_files)} > {max_files}")
            print("安全のため実行を停止します。")
            return {"moved": 0, "errors": 0, "skipped": len(target_files)}

        print(f"📁 {len(target_files)}個のファイルを自動整理します")

        # 危険度判定
        force_confirm, risk_factors, high_risk_files = self.assess_risk_level(
            target_files
        )

        if risk_factors:
            print("\n⚠️ リスク要因が検出されました:")
            for factor in risk_factors:
                print(f"  - {factor}")

        # 強制確認判定
        auto_confirm_enabled = auto_config.get("auto_confirm", True)

        if force_confirm:
            print("\n🚨 危険な操作が検出されました。手動確認が必要です。")
            if high_risk_files:
                print("重要ファイル:")
                for f in high_risk_files[:5]:  # 最初の5件のみ表示
                    print(f"  - {f.name}")
                if len(high_risk_files) > 5:
                    print(f"  ... 他{len(high_risk_files)-5}件")

            confirm = input("本当に続行しますか？ (yes/NO): ").lower().strip()
            if confirm != "yes":
                print("❌ 安全のため中断されました")
                return {"moved": 0, "errors": 0, "skipped": len(target_files)}
            print("✅ 手動確認: 承認済み")

        elif auto_confirm_enabled:
            print("✅ 自動確認: 承認済み (リスクなし)")
        else:
            confirm = input("続行しますか？ (y/N): ").lower().strip()
            if confirm not in ["y", "yes"]:
                print("❌ 中断されました")
                return {"moved": 0, "errors": 0, "skipped": len(target_files)}

        # 自動モード設定
        original_mode = self.config["current_mode"]
        auto_mode = auto_config.get("auto_mode", "migration")
        self.set_project_mode(auto_mode)

        # ファイル整理実行
        results = {"moved": 0, "errors": 0, "skipped": 0}
        for file_path in target_files:
            success, message = self.organize_file(str(file_path))
            if success:
                results["moved"] += 1
                print(f"  ✅ {file_path.name}")
            else:
                results["errors"] += 1
                print(f"  ❌ {file_path.name}: {message}")

        # 元のモードに戻す
        self.config["current_mode"] = original_mode
        self.save_config()

        print(f"🎉 オートラン完了: {results['moved']}移動, {results['errors']}エラー")
        return results

    def organize_file(self, source_path: str) -> Tuple[bool, str]:
        """ファイル整理実行"""
        source = Path(source_path)
        if not source.exists():
            return False, "❌ ファイル不存在"

        # 分類・移動先決定
        category, destination_dir = self.classify_file(source.name)

        if category == "forbidden":
            return False, f"🚨 {destination_dir} (V1失敗パターン)"

        destination_path = self.root_dir / destination_dir
        destination_path.mkdir(parents=True, exist_ok=True)

        # 重複回避処理
        final_destination = self._get_unique_destination(destination_path, source.name)

        try:
            shutil.move(str(source), str(final_destination))
            logger.info(
                f"✅ {source.name} → {final_destination.relative_to(self.root_dir)}"
            )
            return (
                True,
                f"✅ 移動完了: {final_destination.relative_to(self.root_dir)}",
            )

        except Exception as e:
            logger.error(f"❌ 移動失敗: {e}")
            return False, f"❌ 移動失敗: {e}"

    def _get_unique_destination(self, dest_dir: Path, filename: str) -> Path:
        """重複回避ファイル名生成"""
        base_path = dest_dir / filename
        if not base_path.exists():
            return base_path

        # タイムスタンプ付きファイル名生成
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        unique_name = f"{name}_{timestamp}{ext}"

        return dest_dir / unique_name

    def get_stats(self) -> Dict:
        """統計情報取得"""
        return {
            "today": self.config["today_stats"],
            "current_mode": self.config["current_mode"],
            "current_limit": self.get_current_limit(),
            "directories": {
                "analytics": (
                    len(list((self.root_dir / "Data" / "analytics").glob("*")))
                    if (self.root_dir / "Data" / "analytics").exists()
                    else 0
                ),
                "reports": (
                    len(list((self.root_dir / "Documentation" / "reports").glob("*")))
                    if (self.root_dir / "Documentation" / "reports").exists()
                    else 0
                ),
                "strategy": (
                    len(list((self.root_dir / "Documentation" / "strategy").glob("*")))
                    if (self.root_dir / "Documentation" / "strategy").exists()
                    else 0
                ),
                "temp": (
                    len(list((self.root_dir / "Data" / "temp").glob("*")))
                    if (self.root_dir / "Data" / "temp").exists()
                    else 0
                ),
            },
        }


def main():
    """メイン実行"""
    import argparse

    parser = argparse.ArgumentParser(description="MIRRALISM V2 柔軟ファイル自動整理システム")
    parser.add_argument("--auto", action="store_true", help="オートラン実行")
    parser.add_argument("--enable-auto", action="store_true", help="オートラン有効化")
    parser.add_argument("--disable-auto", action="store_true", help="オートラン無効化")
    parser.add_argument("--status", action="store_true", help="オートラン状態確認")

    args = parser.parse_args()
    organizer = FlexibleFileOrganizer()

    # オートラン制御
    if args.enable_auto:
        organizer.config["auto_run"]["enabled"] = True
        organizer.save_config()
        print("✅ オートランを有効にしました")
        return

    if args.disable_auto:
        organizer.config["auto_run"]["enabled"] = False
        organizer.save_config()
        print("❌ オートランを無効にしました")
        return

    if args.status:
        auto_config = organizer.config.get("auto_run", {})
        print(f"🤖 オートラン状態: {'有効' if auto_config.get('enabled', False) else '無効'}")
        print(f"🎯 デフォルトアクション: {auto_config.get('default_action', 'clean_mess')}")
        print(f"🔧 自動確認: {'有効' if auto_config.get('auto_confirm', True) else '無効'}")
        return

    # オートラン実行
    if args.auto:
        results = organizer.auto_run_cleanup()
        print(
            f"\n🎉 オートラン完了: {results['moved']}移動, {results['errors']}エラー, {results['skipped']}スキップ"
        )
        return

    # 従来の対話モード
    print("🏗️ MIRRALISM V2 柔軟ファイル自動整理システム")
    print("=" * 50)

    # 現在の統計表示
    stats = organizer.get_stats()
    print(f"📊 今日の作成数: {stats['today']['files_created']}")
    print(f"🎯 現在モード: {stats['current_mode']} (制限: {stats['current_limit']})")
    print(
        f"📁 分散状況: Analytics({stats['directories']['analytics']}) Reports({stats['directories']['reports']}) Strategy({stats['directories']['strategy']}) Temp({stats['directories']['temp']})"
    )

    auto_config = organizer.config.get("auto_run", {})
    auto_status = "有効" if auto_config.get("enabled", False) else "無効"
    print(f"🤖 オートラン: {auto_status}")

    print("\n選択肢:")
    print("1. 現在の散らかりを整理")
    print("2. プロジェクトモード設定")
    print("3. 統計表示")
    print("4. オートラン実行")
    print("5. オートラン設定")
    print("6. 終了")

    choice = input("\n選択してください (1-6): ").strip()

    if choice == "1":
        results = organizer.clean_current_mess()
        print(f"\n🎉 整理完了: {results['moved']}移動, {results['errors']}エラー")

    elif choice == "2":
        print("利用可能モード: normal, analysis, migration")
        mode = input("モードを選択: ").strip()
        if organizer.set_project_mode(mode):
            print(f"✅ {mode}モードに設定しました")
        else:
            print("❌ 無効なモード")

    elif choice == "3":
        stats = organizer.get_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))

    elif choice == "4":
        results = organizer.auto_run_cleanup()
        print(f"\n🎉 オートラン完了: {results['moved']}移動, {results['errors']}エラー")

    elif choice == "5":
        print("\nオートラン設定:")
        print("1. オートラン有効化")
        print("2. オートラン無効化")
        print("3. 設定確認")
        sub_choice = input("選択 (1-3): ").strip()

        if sub_choice == "1":
            organizer.config["auto_run"]["enabled"] = True
            organizer.save_config()
            print("✅ オートランを有効にしました")
        elif sub_choice == "2":
            organizer.config["auto_run"]["enabled"] = False
            organizer.save_config()
            print("❌ オートランを無効にしました")
        elif sub_choice == "3":
            auto_config = organizer.config.get("auto_run", {})
            print(json.dumps(auto_config, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
