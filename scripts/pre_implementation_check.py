#!/usr/bin/env python3
"""
MIRRALISM 設計書準拠チェックシステム
=====================================

開発時に設計書との整合性を自動チェックし、
scriptsディレクトリ問題の再発を防止
"""

from pathlib import Path


class DesignViolationError(Exception):
    """設計書違反エラー"""


class DesignComplianceChecker:
    """設計書準拠チェッカー"""

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.design_directories = self._load_design_directories()

    def _load_design_directories(self):
        """設計書で承認されたディレクトリ一覧を取得"""
        return {
            # Core System
            "Core/PersonalityLearning/",
            "Core/Classification/",
            "Core/Search/",
            "Core/Learning/",
            "Core/intake/",
            # Prototype Environment
            "Prototype/experiments/",
            "Prototype/testing/",
            "Prototype/development/",
            # API Integration
            "API/exports/",
            "API/integrations/",
            "API/integrations/superwhisper/",
            "API/webhooks/",
            # Documentation
            "Documentation/decisions/",
            "Documentation/guides/",
            "Documentation/migration/",
            "Documentation/reports/",
            "Documentation/strategy/",
            # Data Storage
            "Data/analytics/",
            "Data/temp/",
            "Data/export/",
            "Data/backup/",
            # Contents Creation
            "Contents/youtube_scripts/",
            "Contents/newsletter/",
            "Contents/blog/",
            "Contents/social/",
            # 正式承認済み
            "scripts/",  # 2025年6月3日承認
        }

    def check_directory_compliance(self, new_directory):
        """
        新規ディレクトリの設計書準拠チェック

        Args:
            new_directory (str): チェック対象ディレクトリ

        Raises:
            DesignViolationError: 設計書に記載されていない場合
        """
        # 末尾のスラッシュを統一
        normalized_dir = new_directory.rstrip("/") + "/"

        if normalized_dir not in self.design_directories:
            raise DesignViolationError(
                f"🚨 設計書違反検出！\n"
                f"ディレクトリ '{new_directory}' は設計書に記載されていません。\n"
                f"✅ 正しい手順:\n"
                f"  1. 事前に設計チームに相談\n"
                f"  2. 設計書を更新\n"
                f"  3. 承認後に実装\n"
                f"📋 承認済みディレクトリ一覧:\n"
                + "\n".join(f"  - {d}" for d in sorted(self.design_directories))
            )

    def test_compliance_check(self):
        """
        コンプライアンスチェック機能のテスト

        Returns:
            dict: テスト結果
        """
        results = {
            "valid_directories": [],
            "invalid_directories": [],
            "test_passed": True,
        }

        # 有効なディレクトリのテスト
        valid_tests = [
            "scripts/",
            "Core/PersonalityLearning/",
            "Data/analytics/",
        ]
        for test_dir in valid_tests:
            try:
                self.check_directory_compliance(test_dir)
                results["valid_directories"].append(test_dir)
            except DesignViolationError:
                results["test_passed"] = False

        # 無効なディレクトリのテスト
        invalid_tests = [
            "unauthorized_dir/",
            "random_folder/",
            "test_directory/",
        ]
        for test_dir in invalid_tests:
            try:
                self.check_directory_compliance(test_dir)
                results["test_passed"] = False  # 例外が出ないのは問題
            except DesignViolationError:
                results["invalid_directories"].append(test_dir)

        return results


def main():
    """メイン実行関数"""
    checker = DesignComplianceChecker()

    print("🧪 設計書準拠チェック機能テスト")
    print("=" * 40)

    # 機能テスト実行
    results = checker.test_compliance_check()

    print("✅ 承認済みディレクトリテスト:")
    for dir_name in results["valid_directories"]:
        print(f"  ✓ {dir_name} → OK")

    print("\n🚨 未承認ディレクトリテスト:")
    for dir_name in results["invalid_directories"]:
        print(f"  ✓ {dir_name} → 正しく拒否")

    print(f"\n📊 テスト結果: {'✅ 合格' if results['test_passed'] else '❌ 失敗'}")

    # 実際の違反例デモ
    print("\n" + "=" * 40)
    print("🎭 実際の違反例デモ:")
    try:
        checker.check_directory_compliance("unauthorized_test_dir/")
    except DesignViolationError as e:
        print(f"✅ 期待通りエラーが発生:\n{e}")


if __name__ == "__main__":
    main()
