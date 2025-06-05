#!/usr/bin/env python3
"""
MIRRALISM PersonalityLearning Engine Basic - Unit Tests
V1教訓活用版の品質保証テスト

作成日: 2025年6月5日
技術者: MIRRALISM自律技術者
目的: CTOの品質要求に対応した包括的テスト
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# テスト対象のインポート
sys.path.append(str(Path(__file__).parent.parent / "Core" / "PersonalityLearning"))

try:
    from mirralism_personality_engine_basic import MirralismPersonalityEngineBasic
except ImportError as e:
    print(f"インポートエラー: {e}")
    print(
        "Core/PersonalityLearning/mirralism_personality_engine_basic.py が存在することを確認してください"
    )
    sys.exit(1)


class TestMirralismPersonalityEngineBasic(unittest.TestCase):
    """MIRRALISM PersonalityEngine Basic ユニットテスト"""

    def setUp(self):
        """テスト準備"""
        # 一時データベースファイル作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()

        # エンジン初期化
        self.engine = MirralismPersonalityEngineBasic(db_path=self.temp_db.name)

    def tearDown(self):
        """テスト後処理"""
        # 一時ファイル削除
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_engine_initialization(self):
        """エンジン初期化テスト"""
        self.assertEqual(self.engine.version, "MIRRALISM_Basic_V2.0")
        self.assertEqual(self.engine.v1_learned_accuracy, 61.0)
        self.assertEqual(self.engine.target_accuracy, 95.0)
        self.assertEqual(len(self.engine.basic_traits), 10)

    def test_v1_lessons_applied(self):
        """V1教訓適用確認テスト"""
        status = self.engine.get_status()
        v1_lessons = status["v1_lessons_applied"]

        self.assertTrue(v1_lessons["file_unification"])
        self.assertTrue(v1_lessons["accuracy_inheritance"])
        self.assertTrue(v1_lessons["redirect_prevention"])
        self.assertTrue(v1_lessons["ssot_principle"])

    def test_basic_content_analysis(self):
        """基本コンテンツ分析テスト"""
        test_content = """
        技術的な実装について相談したいことがあります。
        品質を向上させるため、誠実に責任を持って開発を進めます。
        チームとの協力を大切にします。
        """

        result = self.engine.analyze_content(test_content)

        # 基本構造テスト
        self.assertTrue(result["success"])
        self.assertEqual(result["version"], "MIRRALISM_Basic_V2.0")
        self.assertIn("accuracy", result)
        self.assertIn("personality_profile", result)
        self.assertIn("processing_time", result)

        # 精度テスト
        accuracy = result["accuracy"]
        self.assertEqual(accuracy["v1_baseline"], 61.0)
        self.assertGreaterEqual(accuracy["current"], 61.0)
        self.assertLessEqual(accuracy["current"], 95.0)

    def test_personality_trait_analysis(self):
        """性格特性分析テスト"""
        # 技術志向テスト
        tech_content = "技術実装システム開発コードCTO"
        result = self.engine.analyze_content(tech_content)

        profile = result["personality_profile"]
        self.assertGreater(profile["technical_orientation"], 0.3)

        # 誠実性テスト
        integrity_content = "誠実責任品質信頼安全保護正確"
        result = self.engine.analyze_content(integrity_content)

        profile = result["personality_profile"]
        self.assertGreater(profile["integrity_focus"], 0.5)

        # 関係性テスト
        relationship_content = "協力チーム相談サポート理解共感"
        result = self.engine.analyze_content(relationship_content)

        profile = result["personality_profile"]
        self.assertGreater(profile["relationship_value"], 0.3)

    def test_accuracy_improvement(self):
        """精度向上テスト"""
        # 技術・誠実性キーワード含有コンテンツ
        enhanced_content = """
        技術的な実装について相談したいことがあります。
        システムの品質と効率を最適化するため、
        誠実に責任を持って開発を進めたいと考えています。
        """
        enhanced_result = self.engine.analyze_content(enhanced_content)

        # 精度向上確認
        enhanced_accuracy = enhanced_result["accuracy"]["current"]
        self.assertGreater(enhanced_accuracy, 61.0)

    def test_database_functionality(self):
        """データベース機能テスト"""
        test_content = "データベーステスト用コンテンツ"

        # 分析実行（データベース保存含む）
        result = self.engine.analyze_content(test_content, {"test": True})

        # データベースファイル存在確認
        self.assertTrue(os.path.exists(self.engine.db_path))

        # 精度履歴取得テスト
        history = self.engine.get_accuracy_history()
        self.assertIsInstance(history, list)

    def test_error_handling(self):
        """エラーハンドリングテスト"""
        # 空文字列テスト
        result = self.engine.analyze_content("")
        self.assertTrue(result["success"])

        # None入力テスト
        result = self.engine.analyze_content("test", None)
        self.assertTrue(result["success"])

    def test_performance(self):
        """パフォーマンステスト"""
        test_content = "パフォーマンステスト用のコンテンツです。" * 100

        result = self.engine.analyze_content(test_content)

        # 処理時間が1秒以内であること
        self.assertLess(result["processing_time"], 1.0)
        self.assertTrue(result["success"])

    def test_big_five_calculation(self):
        """Big Five計算テスト"""
        test_content = "技術協力誠実責任"
        result = self.engine.analyze_content(test_content)

        profile = result["personality_profile"]

        # Big Five要素が存在すること
        self.assertIn("openness", profile)
        self.assertIn("conscientiousness", profile)
        self.assertIn("extraversion", profile)
        self.assertIn("agreeableness", profile)
        self.assertIn("neuroticism", profile)

        # スコアが0-1の範囲であること
        for trait in [
            "openness",
            "conscientiousness",
            "extraversion",
            "agreeableness",
            "neuroticism",
        ]:
            self.assertGreaterEqual(profile[trait], 0.0)
            self.assertLessEqual(profile[trait], 1.0)

    def test_mirralism_specific_traits(self):
        """MIRRALISM特化特性テスト"""
        test_content = "技術誠実関係性"
        result = self.engine.analyze_content(test_content)

        profile = result["personality_profile"]

        # MIRRALISM特化要素が存在すること
        self.assertIn("technical_orientation", profile)
        self.assertIn("integrity_focus", profile)
        self.assertIn("relationship_value", profile)
        self.assertIn("growth_mindset", profile)
        self.assertIn("stress_resilience", profile)

    def test_status_reporting(self):
        """状態レポートテスト"""
        status = self.engine.get_status()

        required_keys = [
            "version",
            "current_accuracy",
            "v1_baseline",
            "target_accuracy",
            "database_path",
            "traits_count",
            "status",
        ]

        for key in required_keys:
            self.assertIn(key, status)

        self.assertEqual(status["status"], "active")


class TestV1LessonsLearned(unittest.TestCase):
    """V1教訓活用テスト"""

    def test_file_unification_principle(self):
        """ファイル統合原則テスト"""
        # 単一ファイルでの実装確認
        engine = MirralismPersonalityEngineBasic()

        # SSOT原則の適用確認
        self.assertTrue(hasattr(engine, "v1_lessons"))
        self.assertTrue(engine.v1_lessons["ssot_principle"])

    def test_accuracy_inheritance(self):
        """精度継承テスト"""
        engine = MirralismPersonalityEngineBasic()

        # V1学習済み精度の継承確認
        self.assertEqual(engine.v1_learned_accuracy, 61.0)
        self.assertEqual(engine.current_accuracy, 61.0)

    def test_redirect_prevention(self):
        """REDIRECT問題防止テスト"""
        engine = MirralismPersonalityEngineBasic()

        # REDIRECT防止設定の確認
        self.assertTrue(engine.v1_lessons["redirect_prevention"])

        # ファイルサイズ制限なし（基本実装では不要）
        # 統合アーキテクチャの採用確認
        self.assertTrue(engine.v1_lessons["unified_architecture"])


if __name__ == "__main__":
    # テスト実行
    print("=== MIRRALISM PersonalityEngine Basic Unit Tests ===")
    print("V1教訓活用・品質保証テスト実行中...")

    # テストスイート作成
    test_suite = unittest.TestSuite()

    # 基本機能テスト
    test_suite.addTest(unittest.makeSuite(TestMirralismPersonalityEngineBasic))

    # V1教訓テスト
    test_suite.addTest(unittest.makeSuite(TestV1LessonsLearned))

    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # 結果サマリー
    print(f"\n=== Test Results ===")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%"
    )

    if result.failures:
        print(f"\n=== Failures ===")
        for test, traceback in result.failures:
            print(f"{test}: {traceback}")

    if result.errors:
        print(f"\n=== Errors ===")
        for test, traceback in result.errors:
            print(f"{test}: {traceback}")

    # 成功判定
    if len(result.failures) == 0 and len(result.errors) == 0:
        print(f"\n✅ All tests passed! MIRRALISM PersonalityEngine Basic is ready.")
    else:
        print(f"\n❌ Some tests failed. Please review and fix issues.")
        sys.exit(1)
