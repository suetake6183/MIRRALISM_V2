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
    organizer = FlexibleFileOrganizer()

    print("🏗️ MIRRALISM V2 柔軟ファイル自動整理システム")
    print("=" * 50)

    # 現在の統計表示
    stats = organizer.get_stats()
    print(f"📊 今日の作成数: {stats['today']['files_created']}")
    print(f"🎯 現在モード: {stats['current_mode']} (制限: {stats['current_limit']})")
    print(
        f"📁 分散状況: Analytics({stats['directories']['analytics']}) Reports({stats['directories']['reports']}) Strategy({stats['directories']['strategy']}) Temp({stats['directories']['temp']})"
    )

    print("\n選択肢:")
    print("1. 現在の散らかりを整理")
    print("2. プロジェクトモード設定")
    print("3. 統計表示")
    print("4. 終了")

    choice = input("\n選択してください (1-4): ").strip()

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


if __name__ == "__main__":
    main()
