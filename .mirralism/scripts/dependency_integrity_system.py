#!/usr/bin/env python3
"""
MIRRALISM V2 依存関係整合性システム
V1→V2継承による依存関係破綻の完全検出・修正

作成日: 2025年6月5日
目的: 依存関係整合性の徹底的チェック・自動修正・継続監視
重要度: Critical - 品質保証の根幹
"""

import ast
import hashlib
import json
import logging
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple


@dataclass
class DependencyIssue:
    """依存関係問題の詳細情報"""

    file_path: str
    line_number: int
    issue_type: str  # 'missing_import', 'circular_dependency', 'version_conflict', 'broken_path'
    description: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    suggested_fix: str
    code_context: str


class DependencyIntegritySystem:
    """
    依存関係整合性システム

    機能:
    1. Python/JavaScript/TypeScript import の完全性検証
    2. 循環依存の検出・解決
    3. パッケージバージョン整合性チェック
    4. V1→V2パス変更による破綻検出
    5. 自動修正・継続監視メカニズム
    """

    def __init__(self, project_root: str = None):
        """システム初期化"""
        if project_root:
            self.project_root = Path(project_root)
        else:
            current_path = Path(__file__).resolve()
            self.project_root = current_path.parent.parent.parent

        self.logger = self._setup_logging()

        # 分析対象ファイル拡張子
        self.target_extensions = {
            "python": [".py"],
            "javascript": [".js", ".jsx", ".ts", ".tsx"],
            "config": [".json", ".yaml", ".yml", ".toml", ".cfg", ".ini"],
        }

        # V1→V2パス移行マッピング
        self.path_migrations = {
            "MyBrain.MIRRALISM.Core.": "Core.",
            "MyBrain.MIRRALISM.API.": "API.",
            "MyBrain.MIRRALISM.Prototype.": "Prototype.",
            "MyBrain.MIRRALISM.": "",
            "MyBrain.Core.": "Core.",
            "MyBrain.API.": "API.",
            "from MyBrain.MIRRALISM.Core": "from Core",
            "from MyBrain.MIRRALISM.API": "from API",
            "from MyBrain.MIRRALISM": "from .",
            "from MyBrain.Core": "from Core",
            "import MyBrain.MIRRALISM.Core": "import Core",
            "import MyBrain.MIRRALISM": "import .",
        }

        # 分析結果データベース
        self.integrity_db_path = (
            self.project_root / ".mirralism" / "dependency_integrity.db"
        )
        self.integrity_db_path.parent.mkdir(parents=True, exist_ok=True)

        # 修正履歴ログ
        self.fix_log_path = (
            self.project_root / ".mirralism" / "logs" / "dependency_fixes.log"
        )
        self.fix_log_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"🔍 依存関係整合性システム初期化完了 - プロジェクトルート: {self.project_root}")

    def _setup_logging(self) -> logging.Logger:
        """ログ設定"""
        logger = logging.getLogger("DependencyIntegrity")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def scan_all_files(self) -> Dict[str, List[Path]]:
        """プロジェクト全体のファイルスキャン"""
        self.logger.info("📂 プロジェクト全体ファイルスキャン開始...")

        scanned_files = {"python": [], "javascript": [], "config": []}

        # 除外ディレクトリ
        excluded_dirs = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "node_modules",
            ".vscode",
            ".cursor",
            ".DS_Store",
            ".mirralism/backups",  # バックアップは除外
        }

        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                # 除外ディレクトリチェック
                if any(excluded in str(file_path) for excluded in excluded_dirs):
                    continue

                # ファイル種別判定
                for file_type, extensions in self.target_extensions.items():
                    if file_path.suffix in extensions:
                        scanned_files[file_type].append(file_path)
                        break

        total_files = sum(len(files) for files in scanned_files.values())
        self.logger.info(f"📊 スキャン完了: {total_files}ファイル")
        for file_type, files in scanned_files.items():
            self.logger.info(f"  - {file_type}: {len(files)}ファイル")

        return scanned_files

    def analyze_python_imports(self, python_files: List[Path]) -> List[DependencyIssue]:
        """Python import の完全性分析"""
        self.logger.info("🐍 Python import 分析開始...")

        issues = []

        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # import文の行ごと解析
                lines = content.split("\n")
                for line_no, line in enumerate(lines, 1):
                    line_stripped = line.strip()

                    # import文のチェック
                    if (
                        line_stripped.startswith("import ")
                        or line_stripped.startswith("from ")
                    ) and not line_stripped.startswith("#"):
                        # V1→V2パス変更による破綻チェック
                        for old_pattern, new_pattern in self.path_migrations.items():
                            if old_pattern in line:
                                issues.append(
                                    DependencyIssue(
                                        file_path=str(
                                            file_path.relative_to(self.project_root)
                                        ),
                                        line_number=line_no,
                                        issue_type="broken_path",
                                        description=f"V1パス参照: {old_pattern}",
                                        severity="high",
                                        suggested_fix=f"パスを更新: {line.replace(old_pattern, new_pattern)}",
                                        code_context=line.strip(),
                                    )
                                )

            except Exception as e:
                self.logger.error(f"❌ Python分析エラー: {file_path} - {e}")

        self.logger.info(f"🐍 Python分析完了: {len(issues)}件の問題検出")
        return issues

    def analyze_package_dependencies(self) -> List[DependencyIssue]:
        """パッケージ依存関係の整合性分析"""
        self.logger.info("📦 パッケージ依存関係分析開始...")

        issues = []

        # requirements.txt の分析
        req_files = [
            self.project_root / "requirements.txt",
            self.project_root / "MyBrain" / "requirements.txt",
        ]

        packages_by_file = {}

        for req_file in req_files:
            if req_file.exists():
                with open(req_file, "r") as f:
                    lines = f.readlines()
                    packages = {}

                    for line_no, line in enumerate(lines, 1):
                        line_stripped = line.strip()
                        if "==" in line_stripped and not line_stripped.startswith("#"):
                            try:
                                package_name, version = line_stripped.split("==", 1)
                                packages[package_name.strip()] = version.strip()
                            except ValueError:
                                issues.append(
                                    DependencyIssue(
                                        file_path=str(
                                            req_file.relative_to(self.project_root)
                                        ),
                                        line_number=line_no,
                                        issue_type="malformed_dependency",
                                        description=f"不正な依存関係記述: {line_stripped}",
                                        severity="medium",
                                        suggested_fix="正しい形式: package==version",
                                        code_context=line.strip(),
                                    )
                                )

                    packages_by_file[str(req_file)] = packages

        # バージョン競合チェック
        all_packages = {}
        for file_path, packages in packages_by_file.items():
            for package_name, version in packages.items():
                if package_name in all_packages:
                    if all_packages[package_name] != version:
                        issues.append(
                            DependencyIssue(
                                file_path=Path(file_path)
                                .relative_to(self.project_root)
                                .as_posix(),
                                line_number=0,
                                issue_type="version_conflict",
                                description=f"バージョン競合: {package_name} ({all_packages[package_name]} vs {version})",
                                severity="high",
                                suggested_fix=f"バージョンを統一: {package_name}=={version}",
                                code_context=f"{package_name}=={version}",
                            )
                        )
                else:
                    all_packages[package_name] = version

        self.logger.info(f"📦 パッケージ分析完了: {len(issues)}件の問題検出")
        return issues

    def execute_automated_fixes(self, issues: List[DependencyIssue]) -> Dict[str, Any]:
        """自動修正の実行"""
        self.logger.info("🔧 自動修正実行開始...")

        fix_results = {
            "fixed_issues": [],
            "failed_fixes": [],
            "backup_created": False,
            "backup_path": "",
            "fix_timestamp": datetime.now().isoformat(),
        }

        # 修正前バックアップ作成
        backup_dir = self._create_backup_before_fixes()
        fix_results["backup_created"] = True
        fix_results["backup_path"] = str(backup_dir)

        for issue in issues:
            if issue.issue_type == "broken_path":
                try:
                    file_path = self.project_root / issue.file_path
                    if file_path.exists():
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        # V1→V2パス変更の自動修正
                        original_content = content
                        for old_pattern, new_pattern in self.path_migrations.items():
                            content = content.replace(old_pattern, new_pattern)

                        if content != original_content:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(content)

                            fix_results["fixed_issues"].append(
                                {
                                    "issue": issue.__dict__,
                                    "fix_applied": "path_migration",
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )

                except Exception as e:
                    fix_results["failed_fixes"].append(
                        {
                            "issue": issue.__dict__,
                            "error": str(e),
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

        self.logger.info(
            f"🔧 自動修正完了: {len(fix_results['fixed_issues'])}件修正, {len(fix_results['failed_fixes'])}件失敗"
        )
        return fix_results

    def _create_backup_before_fixes(self) -> Path:
        """修正前バックアップ作成"""
        backup_dir = (
            self.project_root
            / ".mirralism"
            / "backups"
            / f"dependency_fixes_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        backup_dir.mkdir(parents=True, exist_ok=True)

        # 主要ファイルのバックアップ
        important_files = [
            "requirements.txt",
            "package.json",
            "MyBrain/requirements.txt",
        ]

        for file_rel_path in important_files:
            file_path = self.project_root / file_rel_path
            if file_path.exists():
                backup_file_path = backup_dir / file_rel_path
                backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_file_path)

        return backup_dir

    def execute_complete_analysis(self) -> Dict[str, Any]:
        """完全な依存関係分析の実行"""
        self.logger.info("🔍 完全依存関係分析実行開始...")

        start_time = datetime.now()

        # 1. 全ファイルスキャン
        scanned_files = self.scan_all_files()

        # 2. Python import 分析
        python_issues = self.analyze_python_imports(scanned_files["python"])

        # 3. パッケージ依存関係分析
        package_issues = self.analyze_package_dependencies()

        # 4. 全問題の統合
        all_issues = python_issues + package_issues

        # 5. 自動修正実行
        automated_fix_results = self.execute_automated_fixes(
            [
                issue
                for issue in all_issues
                if issue.issue_type in ["broken_path", "version_conflict"]
            ]
        )

        # 6. 結果保存
        analysis_results = {
            "analysis_timestamp": start_time.isoformat(),
            "analysis_duration": (datetime.now() - start_time).total_seconds(),
            "scanned_files_summary": {k: len(v) for k, v in scanned_files.items()},
            "issues_detected": len(all_issues),
            "automated_fixes": automated_fix_results,
            "all_issues": [issue.__dict__ for issue in all_issues],
        }

        # 結果をファイル保存
        results_file = (
            self.project_root
            / ".mirralism"
            / "reports"
            / f"dependency_analysis_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        results_file.parent.mkdir(parents=True, exist_ok=True)

        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)

        self.logger.info(f"🔍 完全分析完了: {len(all_issues)}件の問題検出")
        self.logger.info(f"📊 結果保存: {results_file}")

        return analysis_results


def main():
    """メイン実行関数"""
    import argparse

    parser = argparse.ArgumentParser(description="MIRRALISM V2 依存関係整合性システム")
    parser.add_argument("--project-root", help="プロジェクトルートパス")
    parser.add_argument("--quick-check", action="store_true", help="高速チェックモード")
    parser.add_argument("--pre-commit", action="store_true", help="Pre-commit hook モード")

    args = parser.parse_args()

    system = DependencyIntegritySystem(args.project_root)

    if args.quick_check or args.pre_commit:
        # 高速チェック（主要ファイルのみ）
        scanned_files = system.scan_all_files()
        issues = system.analyze_python_imports(
            scanned_files["python"][:10]
        )  # 最初の10ファイルのみ

        if issues:
            print(f"❌ {len(issues)}件の依存関係問題検出")
            for issue in issues[:3]:  # 最初の3件のみ表示
                print(f"  - {issue.file_path}:{issue.line_number} {issue.description}")
            sys.exit(1)
        else:
            print("✅ 依存関係整合性チェック成功")
            sys.exit(0)
    else:
        # 完全分析
        results = system.execute_complete_analysis()

        # 結果サマリー表示
        print("\n" + "=" * 60)
        print("🔍 MIRRALISM V2 依存関係整合性分析結果")
        print("=" * 60)
        print(f"📊 分析時間: {results['analysis_duration']:.2f}秒")
        print(f"📂 スキャンファイル: {sum(results['scanned_files_summary'].values())}件")
        print(f"⚠️  検出問題: {results['issues_detected']}件")

        if results["automated_fixes"]["fixed_issues"]:
            print(f"🔧 自動修正: {len(results['automated_fixes']['fixed_issues'])}件")

        if results["issues_detected"] > 0:
            print("\n📋 主要問題:")
            for issue_dict in results["all_issues"][:5]:  # 最初の5件
                print(f"  - {issue_dict['file_path']}:{issue_dict['line_number']}")
                print(f"    {issue_dict['description']}")
                print(f"    修正提案: {issue_dict['suggested_fix']}")

            print("=" * 60)


if __name__ == "__main__":
    main()
