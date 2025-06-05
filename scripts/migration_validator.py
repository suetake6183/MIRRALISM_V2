#!/usr/bin/env python3
"""
MIRRALISM V2 マイグレーション検証・ロールバックシステム
==================================================

マイグレーション後の品質保証と問題発生時の自動ロールバック機能
"""

import datetime
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.parent


class MigrationValidator:
    """マイグレーション検証システム"""

    def __init__(self, project_root: Optional[Path] = None):
        self.root_dir = project_root or PROJECT_ROOT
        self.validation_config = self._load_validation_config()
        self.results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "overall_status": "unknown",
            "checks": [],
            "errors": [],
            "warnings": [],
        }

    def _load_validation_config(self) -> Dict:
        """検証設定読み込み"""
        return {
            "critical_checks": [
                "file_structure",
                "core_systems",
                "dependencies",
                "database_integrity",
                "configuration_validity",
            ],
            "performance_checks": [
                "import_test",
                "basic_functionality",
                "date_calculation_system",
            ],
            "file_structure_requirements": {
                "Core/PersonalityLearning": ["unified_system.py", "database.py"],
                "scripts": ["getDate.js", "migrate_installer.py"],
                ".mirralism": ["migration_config.json"],
                "Clients": ["Database", "Profiles", "Systems"],
            },
            "thresholds": {
                "max_import_time": 5.0,
                "max_calculation_time": 1.0,
                "required_accuracy": 100.0,
            },
        }

    def validate_file_structure(self) -> bool:
        """ファイル構造検証"""
        check_name = "file_structure_validation"
        errors = []
        warnings = []

        requirements = self.validation_config["file_structure_requirements"]

        for base_path, required_items in requirements.items():
            base_dir = self.root_dir / base_path

            if not base_dir.exists():
                errors.append(f"必須ディレクトリが存在しません: {base_path}")
                continue

            for item in required_items:
                item_path = base_dir / item

                if not item_path.exists():
                    if item.endswith((".py", ".js", ".json")):
                        errors.append(f"必須ファイルが存在しません: {base_path}/{item}")
                    else:
                        if not any((base_dir / subdir).exists() for subdir in [item]):
                            warnings.append(f"推奨ディレクトリが存在しません: {base_path}/{item}")

        success = len(errors) == 0
        self.results["checks"].append(
            {
                "name": check_name,
                "status": "passed" if success else "failed",
                "errors": errors,
                "warnings": warnings,
            }
        )

        if errors:
            self.results["errors"].extend(errors)
        if warnings:
            self.results["warnings"].extend(warnings)

        return success

    def validate_core_systems(self) -> bool:
        """コアシステム検証"""
        check_name = "core_systems_validation"
        errors = []
        warnings = []

        # PersonalityLearning システム検証
        try:
            personality_dir = self.root_dir / "Core" / "PersonalityLearning"

            # データベースファイル確認
            db_file = personality_dir / "MIRRALISM_UNIFIED.db"
            if not db_file.exists():
                errors.append("MIRRALISM_UNIFIED.db が見つかりません")
            elif db_file.stat().st_size == 0:
                errors.append("MIRRALISM_UNIFIED.db が空ファイルです")

            # 重要なPythonファイル確認
            critical_files = [
                "unified_system.py",
                "database.py",
                "mirralism_personality_engine_basic.py",
            ]

            for file_name in critical_files:
                file_path = personality_dir / file_name
                if not file_path.exists():
                    errors.append(f"重要ファイルが見つかりません: {file_name}")
                elif file_path.stat().st_size < 100:  # 100バイト未満は異常
                    warnings.append(f"ファイルサイズが小さすぎます: {file_name}")

        except Exception as e:
            errors.append(f"PersonalityLearning システム検証エラー: {e}")

        # 日付計算システム検証
        try:
            date_script = self.root_dir / "scripts" / "getDate.js"
            if not date_script.exists():
                errors.append("getDate.js が見つかりません")
            else:
                # 実際に日付スクリプトを実行してみる
                result = subprocess.run(
                    ["node", str(date_script)],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode != 0:
                    errors.append(f"getDate.js 実行エラー: {result.stderr}")

        except Exception as e:
            errors.append(f"日付システム検証エラー: {e}")

        success = len(errors) == 0
        self.results["checks"].append(
            {
                "name": check_name,
                "status": "passed" if success else "failed",
                "errors": errors,
                "warnings": warnings,
            }
        )

        if errors:
            self.results["errors"].extend(errors)
        if warnings:
            self.results["warnings"].extend(warnings)

        return success

    def validate_dependencies(self) -> bool:
        """依存関係検証"""
        check_name = "dependencies_validation"
        errors = []
        warnings = []

        # Python 依存関係
        try:
            import sqlite3
            import pathlib
            import json
        except ImportError as e:
            errors.append(f"Python標準ライブラリインポートエラー: {e}")

        # Node.js 検証
        try:
            result = subprocess.run(
                ["node", "--version"], capture_output=True, text=True
            )
            if result.returncode != 0:
                errors.append("Node.js が正常に動作しません")
            else:
                version = result.stdout.strip()
                major_version = int(version.replace("v", "").split(".")[0])
                if major_version < 18:
                    warnings.append(f"Node.js バージョンが古い可能性があります: {version}")
        except Exception as e:
            errors.append(f"Node.js 検証エラー: {e}")

        # Git 検証
        try:
            result = subprocess.run(
                ["git", "status"], cwd=self.root_dir, capture_output=True, text=True
            )
            if result.returncode != 0:
                warnings.append("Git リポジトリ状態に問題がある可能性があります")
        except Exception as e:
            warnings.append(f"Git 検証警告: {e}")

        success = len(errors) == 0
        self.results["checks"].append(
            {
                "name": check_name,
                "status": "passed" if success else "failed",
                "errors": errors,
                "warnings": warnings,
            }
        )

        if errors:
            self.results["errors"].extend(errors)
        if warnings:
            self.results["warnings"].extend(warnings)

        return success

    def validate_database_integrity(self) -> bool:
        """データベース整合性検証"""
        check_name = "database_integrity_validation"
        errors = []
        warnings = []

        try:
            import sqlite3

            db_file = (
                self.root_dir / "Core" / "PersonalityLearning" / "MIRRALISM_UNIFIED.db"
            )

            if not db_file.exists():
                errors.append("データベースファイルが存在しません")
                success = False
            else:
                # データベース接続テスト
                try:
                    conn = sqlite3.connect(str(db_file))
                    cursor = conn.cursor()

                    # テーブル存在確認
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()

                    if not tables:
                        warnings.append("データベースにテーブルが存在しません")
                    else:
                        table_names = [table[0] for table in tables]
                        expected_tables = [
                            "personality_data",
                            "analysis_results",
                            "user_sessions",
                        ]

                        for expected in expected_tables:
                            if expected not in table_names:
                                warnings.append(f"期待されるテーブルが見つかりません: {expected}")

                    conn.close()
                    success = True

                except sqlite3.Error as e:
                    errors.append(f"データベース接続エラー: {e}")
                    success = False

        except ImportError:
            errors.append("sqlite3 モジュールが利用できません")
            success = False
        except Exception as e:
            errors.append(f"データベース検証エラー: {e}")
            success = False

        self.results["checks"].append(
            {
                "name": check_name,
                "status": "passed" if success else "failed",
                "errors": errors,
                "warnings": warnings,
            }
        )

        if errors:
            self.results["errors"].extend(errors)
        if warnings:
            self.results["warnings"].extend(warnings)

        return success

    def validate_configuration(self) -> bool:
        """設定検証"""
        check_name = "configuration_validation"
        errors = []
        warnings = []

        # CLAUDE.md 確認
        claude_md = self.root_dir / "CLAUDE.md"
        if not claude_md.exists():
            errors.append("CLAUDE.md が見つかりません")
        else:
            try:
                content = claude_md.read_text(encoding="utf-8")
                if "MIRRALISM V2" not in content:
                    warnings.append("CLAUDE.md にMIRRALISM V2 設定が見つかりません")
                if "node scripts/getDate.js" not in content:
                    warnings.append("CLAUDE.md に日付確認スクリプトの指示がありません")
            except Exception as e:
                warnings.append(f"CLAUDE.md 読み込みエラー: {e}")

        # .mirralism 設定確認
        mirralism_dir = self.root_dir / ".mirralism"
        if not mirralism_dir.exists():
            errors.append(".mirralism 設定ディレクトリが存在しません")
        else:
            config_file = mirralism_dir / "migration_config.json"
            if config_file.exists():
                try:
                    with open(config_file, "r", encoding="utf-8") as f:
                        config = json.load(f)
                    if "version" not in config:
                        warnings.append("migration_config.json にバージョン情報がありません")
                except Exception as e:
                    warnings.append(f"migration_config.json 読み込みエラー: {e}")

        success = len(errors) == 0
        self.results["checks"].append(
            {
                "name": check_name,
                "status": "passed" if success else "failed",
                "errors": errors,
                "warnings": warnings,
            }
        )

        if errors:
            self.results["errors"].extend(errors)
        if warnings:
            self.results["warnings"].extend(warnings)

        return success

    def run_performance_tests(self) -> bool:
        """パフォーマンステスト実行"""
        check_name = "performance_tests"
        errors = []
        warnings = []

        # 日付計算システムテスト
        try:
            import time

            start_time = time.time()

            result = subprocess.run(
                ["node", str(self.root_dir / "scripts" / "getDate.js")],
                capture_output=True,
                text=True,
                timeout=self.validation_config["thresholds"]["max_calculation_time"],
            )

            execution_time = time.time() - start_time

            if result.returncode == 0:
                if (
                    execution_time
                    > self.validation_config["thresholds"]["max_calculation_time"]
                ):
                    warnings.append(f"日付計算が遅いです: {execution_time:.2f}秒")
            else:
                errors.append("日付計算システムが正常に動作しません")

        except subprocess.TimeoutExpired:
            errors.append("日付計算システムがタイムアウトしました")
        except Exception as e:
            errors.append(f"パフォーマンステストエラー: {e}")

        success = len(errors) == 0
        self.results["checks"].append(
            {
                "name": check_name,
                "status": "passed" if success else "failed",
                "errors": errors,
                "warnings": warnings,
            }
        )

        if errors:
            self.results["errors"].extend(errors)
        if warnings:
            self.results["warnings"].extend(warnings)

        return success

    def run_full_validation(self) -> bool:
        """完全検証実行"""
        print("🔍 MIRRALISM V2 マイグレーション検証開始")
        print("=" * 50)

        validation_functions = [
            ("ファイル構造", self.validate_file_structure),
            ("コアシステム", self.validate_core_systems),
            ("依存関係", self.validate_dependencies),
            ("データベース整合性", self.validate_database_integrity),
            ("設定ファイル", self.validate_configuration),
            ("パフォーマンス", self.run_performance_tests),
        ]

        all_passed = True

        for test_name, test_func in validation_functions:
            print(f"\n🧪 {test_name}検証中...")
            try:
                passed = test_func()
                status = "✅ 成功" if passed else "❌ 失敗"
                print(f"   {status}")

                if not passed:
                    all_passed = False

            except Exception as e:
                print(f"   ❌ エラー: {e}")
                self.results["errors"].append(f"{test_name}検証エラー: {e}")
                all_passed = False

        self.results["overall_status"] = "passed" if all_passed else "failed"

        # 結果サマリー表示
        print("\n" + "=" * 50)
        print("🎯 検証結果サマリー")
        print(f"全体ステータス: {'✅ 成功' if all_passed else '❌ 失敗'}")
        print(f"エラー数: {len(self.results['errors'])}")
        print(f"警告数: {len(self.results['warnings'])}")

        if self.results["errors"]:
            print("\n❌ エラー:")
            for error in self.results["errors"]:
                print(f"  - {error}")

        if self.results["warnings"]:
            print("\n⚠️ 警告:")
            for warning in self.results["warnings"]:
                print(f"  - {warning}")

        return all_passed

    def save_validation_report(self, output_file: Optional[Path] = None) -> Path:
        """検証レポート保存"""
        if output_file is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = (
                self.root_dir / ".mirralism" / f"validation_report_{timestamp}.json"
            )

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"📊 検証レポート保存: {output_file}")
        return output_file


class AutoRollbackSystem:
    """自動ロールバックシステム"""

    def __init__(self, project_root: Optional[Path] = None):
        self.root_dir = project_root or PROJECT_ROOT
        self.backup_dir = self.root_dir / ".mirralism" / "backups"

    def check_rollback_needed(self, validation_results: Dict) -> bool:
        """ロールバック必要性判定"""
        critical_failures = 0

        for check in validation_results.get("checks", []):
            if check["status"] == "failed":
                # 重要なチェックの失敗数をカウント
                if check["name"] in [
                    "file_structure_validation",
                    "core_systems_validation",
                ]:
                    critical_failures += 1

        # 2つ以上の重要な検証に失敗した場合はロールバック推奨
        return critical_failures >= 2

    def find_latest_backup(self) -> Optional[str]:
        """最新バックアップ検索"""
        if not self.backup_dir.exists():
            return None

        backup_dirs = [
            d
            for d in self.backup_dir.iterdir()
            if d.is_dir() and d.name.startswith("pre_migration_")
        ]

        if not backup_dirs:
            return None

        # タイムスタンプで最新を選択
        latest = max(backup_dirs, key=lambda d: d.stat().st_mtime)
        return latest.name.replace("pre_migration_", "")

    def suggest_rollback(self, validation_results: Dict) -> bool:
        """ロールバック提案"""
        if not self.check_rollback_needed(validation_results):
            return False

        backup_id = self.find_latest_backup()
        if not backup_id:
            print("⚠️ 利用可能なバックアップが見つかりません")
            return False

        print(f"🔄 重要な検証に失敗しました。ロールバックを推奨します。")
        print(f"最新バックアップ: {backup_id}")
        print("ロールバックを実行しますか？ (y/N): ", end="")

        try:
            response = input().lower().strip()
            return response in ["y", "yes"]
        except KeyboardInterrupt:
            return False


def main():
    """メイン実行"""
    import argparse

    parser = argparse.ArgumentParser(description="MIRRALISM V2 Migration Validator")
    parser.add_argument("--project-root", help="プロジェクトルートディレクトリ")
    parser.add_argument("--output", help="レポート出力ファイル")
    parser.add_argument(
        "--auto-rollback", action="store_true", help="重要な検証失敗時に自動ロールバック提案"
    )

    args = parser.parse_args()

    # バリデーター初期化
    project_root = Path(args.project_root) if args.project_root else None
    validator = MigrationValidator(project_root)

    # 検証実行
    validation_passed = validator.run_full_validation()

    # レポート保存
    output_file = Path(args.output) if args.output else None
    validator.save_validation_report(output_file)

    # 自動ロールバック判定
    if args.auto_rollback and not validation_passed:
        rollback_system = AutoRollbackSystem(project_root)
        if rollback_system.suggest_rollback(validator.results):
            backup_id = rollback_system.find_latest_backup()
            if backup_id:
                print(
                    f"ロールバック実行: python scripts/migrate_installer.py rollback --backup-id {backup_id}"
                )

    # 終了コード
    sys.exit(0 if validation_passed else 1)


if __name__ == "__main__":
    main()
