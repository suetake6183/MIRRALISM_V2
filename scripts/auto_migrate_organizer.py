#!/usr/bin/env python3
"""
MIRRALISM V2 マイグレーション自動整理フック
==========================================

TaskMaster連携でマイグレーション時にファイル整理を自動実行
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import datetime
import json

from file_organizer import FlexibleFileOrganizer


class MigrationOrganizer:
    """マイグレーション連携ファイル整理"""

    def __init__(self):
        self.organizer = FlexibleFileOrganizer()
        self.log_file = (
            self.organizer.root_dir / "Data" / "analytics" / "migration_log.json"
        )

    def pre_migration_cleanup(self):
        """マイグレーション前クリーンアップ"""
        print("🚀 マイグレーション前ファイル整理...")

        # migrationモードに切り替え
        self.organizer.set_project_mode("migration")

        # 現在の散らかりを整理
        results = self.organizer.clean_current_mess()

        # ログ記録
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "pre_migration_cleanup",
            "results": results,
            "files_organized": results["moved"],
            "errors": results["errors"],
        }

        self._save_log(log_entry)

        print(f"✅ マイグレーション前整理完了: {results['moved']}ファイル移動")
        return results

    def post_migration_validation(self):
        """マイグレーション後検証"""
        print("🔍 マイグレーション後検証...")

        # 残存散らかりチェック
        remaining_files = []
        for item in self.organizer.root_dir.iterdir():
            if item.is_file() and not item.name.startswith("."):
                category, _ = self.organizer.classify_file(item.name)
                if category != "unknown":
                    remaining_files.append(item.name)

        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "post_migration_validation",
            "remaining_files": remaining_files,
            "clean_status": len(remaining_files) == 0,
        }

        self._save_log(log_entry)

        if remaining_files:
            print(f"⚠️ {len(remaining_files)}個のファイルがまだ散らかっています: {remaining_files}")
            return False
        else:
            print("✅ ディレクトリ完全クリーン！")
            return True

    def _save_log(self, log_entry):
        """ログ保存"""
        logs = []
        if self.log_file.exists():
            with open(self.log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)

        logs.append(log_entry)

        # 最新50件のみ保持
        logs = logs[-50:]

        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)


def main():
    """メイン実行"""
    if len(sys.argv) < 2:
        print("使用法: python auto_migrate_organizer.py [pre|post|full]")
        return

    migrator = MigrationOrganizer()

    command = sys.argv[1]

    if command == "pre":
        migrator.pre_migration_cleanup()
    elif command == "post":
        migrator.post_migration_validation()
    elif command == "full":
        print("🔄 完全マイグレーション整理実行...")
        pre_results = migrator.pre_migration_cleanup()
        post_clean = migrator.post_migration_validation()
        print(f"🎉 完了: {pre_results['moved']}ファイル整理, クリーン状態: {post_clean}")
    else:
        print(f"❌ 無効なコマンド: {command}")


if __name__ == "__main__":
    main()
