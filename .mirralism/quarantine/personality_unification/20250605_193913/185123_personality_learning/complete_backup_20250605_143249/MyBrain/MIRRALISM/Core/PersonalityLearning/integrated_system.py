#!/usr/bin/env python3
"""
MIRRALISM PersonalityLearning 統合システム
=======================================

V2データベース + PersonalityLearningCore の完全統合
53% → 95% 精度進化の実現

統合対象:
- database.py (V2スキーマ)
- personality_learning_core.py (V1互換性保持)
- TaskMaster連携
- SuperWhisper統合

作成者: MIRRALISM V2 統合チーム
作成日: 2025年6月3日
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

# パス設定（同一ディレクトリのモジュールをインポート）
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from database import PersonalityLearningDatabase
    from personality_learning_core import PersonalityLearningCore
except ImportError:
    # フォールバック: 直接ファイルパスから読み込み
    import importlib.util

    # database.py
    db_spec = importlib.util.spec_from_file_location(
        "database", current_dir / "database.py"
    )
    db_module = importlib.util.module_from_spec(db_spec)
    db_spec.loader.exec_module(db_module)
    PersonalityLearningDatabase = db_module.PersonalityLearningDatabase

    # personality_learning_core.py
    core_spec = importlib.util.spec_from_file_location(
        "personality_learning_core",
        current_dir / "personality_learning_core.py",
    )
    core_module = importlib.util.module_from_spec(core_spec)
    core_spec.loader.exec_module(core_module)
    PersonalityLearningCore = core_module.PersonalityLearningCore

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MirralismPersonalityLearning:
    """
    MIRRALISM PersonalityLearning 完全統合システム

    機能統合:
    - V2データベース (10テーブル + 18インデックス)
    - PersonalityLearningCore (V1互換性)
    - TaskMaster連携 (学習効果相関)
    - SuperWhisper統合 (音声データ1.5倍重み付け)

    進化目標: 53% → 95% 精度実現
    """

    def __init__(self, db_path: Optional[str] = None):
        """統合システム初期化"""

        # パス設定
        if db_path is None:
            current_dir = Path(__file__).parent
            db_path = str(current_dir / "personality_learning_v2.db")

        # コンポーネント初期化
        self.database = PersonalityLearningDatabase(db_path)
        self.core = PersonalityLearningCore(db_path)

        # 統合システム設定
        self.version = "2.0_MIRRALISM_INTEGRATED"
        self.target_accuracy = 95.0
        self.current_accuracy = self.core.get_learned_accuracy()

        # 進化段階定義
        self.evolution_stages = {
            53.0: "V1_baseline",
            61.0: "V1_learned",
            70.0: "V2_training",
            80.0: "V2_validation",
            90.0: "V2_production_ready",
            95.0: "V2_target_achieved",
        }

        logger.info(f"MIRRALISM統合システム初期化完了 - 現在精度: {self.current_accuracy}%")

    def analyze_entry(
        self,
        content: str,
        source_type: str = "journal",
        voice_data: Optional[Dict] = None,
        task_context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        統合分析エントリーポイント

        Args:
            content: 分析対象テキスト
            source_type: データソース ("journal", "voice", "task", "interaction")
            voice_data: SuperWhisper音声データ (optional)
            task_context: TaskMaster連携データ (optional)

        Returns:
            Dict: 統合分析結果 + データベース記録
        """
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()

        try:
            # Core分析実行
            if source_type == "voice" and voice_data:
                # SuperWhisper統合分析
                # process_voice_input expects the voice metadata and the
                # transcribed content in a single dictionary. Previously only
                # ``{"content": content, "metadata": voice_data}`` was passed
                # which resulted in quality and confidence information being
                # ignored.  Merge the parameters correctly so that voice
                # related scores are taken into account.
                core_voice_data = {"content": content, **voice_data}
                core_result = self.core.process_voice_input(core_voice_data)
            else:
                # 標準分析
                core_result = self.core.analyze_journal_entry(
                    content, source_type, task_context
                )

            if not core_result["success"]:
                return core_result

            # 分析データ拡張
            enhanced_analysis = self._enhance_analysis(
                core_result, source_type, voice_data, task_context
            )

            # データベース記録
            self._record_to_database(enhanced_analysis, analysis_id, start_time)

            # 精度進化チェック
            evolution_update = self._check_evolution_progress(enhanced_analysis)

            # 最終結果統合
            final_result = {
                **enhanced_analysis,
                "analysis_id": analysis_id,
                "database_recorded": True,
                "evolution_status": evolution_update,
                "processing_time_total": (datetime.now() - start_time).total_seconds(),
            }

            logger.info(
                f"統合分析完了: {analysis_id}, 精度: {enhanced_analysis['analysis']['suetake_likeness_index']}%"
            )

            return final_result

        except Exception as e:
            logger.error(f"統合分析エラー: {e}")
            return {
                "success": False,
                "error": f"統合分析失敗: {str(e)}",
                "analysis_id": analysis_id,
                "timestamp": datetime.now().isoformat(),
            }

    def _enhance_analysis(
        self,
        core_result: Dict,
        source_type: str,
        voice_data: Optional[Dict] = None,
        task_context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """分析結果の拡張（統合機能追加）"""

        enhanced = core_result.copy()
        analysis = enhanced["analysis"]

        # V2統合拡張
        analysis["mirralism_integration"] = {
            "database_version": "v2",
            "integration_level": "full",
            "source_type": source_type,
            "accuracy_evolution_stage": self._get_evolution_stage(
                analysis["suetake_likeness_index"]
            ),
        }

        # SuperWhisper統合情報
        if source_type == "voice" and voice_data:
            analysis["voice_integration"] = {
                "weight_multiplier": self.core.voice_weight_multiplier,
                "audio_duration": voice_data.get("duration", 0),
                "confidence_score": voice_data.get("confidence", 0.5),
                "transcription_quality": voice_data.get("quality", "medium"),
            }

        # TaskMaster連携情報
        if task_context:
            analysis["task_integration"] = {
                "task_id": task_context.get("task_id"),
                "task_title": task_context.get("title"),
                "completion_status": task_context.get("status"),
                "learning_correlation": self._calculate_task_learning_correlation(
                    analysis["suetake_likeness_index"], task_context
                ),
            }

        return enhanced

    def _record_to_database(
        self, analysis_result: Dict, analysis_id: str, start_time: datetime
    ):
        """統合分析結果のデータベース記録"""

        analysis = analysis_result["analysis"]
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

        # 1. 分析履歴記録
        self.database.record_analysis(
            analysis_id=analysis_id,
            analysis_type="journal",
            input_text=analysis_result["content"],
            result={
                "suetake_likeness": analysis["suetake_likeness_index"],
                "tech_keywords": analysis["tech_keyword_count"],
                "integrity_keywords": analysis["integrity_keyword_count"],
                "insights": analysis["insights"],
            },
            confidence=analysis.get("confidence_score", 0.8),
            processing_time=processing_time,
        )

        # 2. キーワード学習更新
        content = analysis_result["content"]
        for keyword in self.core.tech_keywords:
            if keyword in content:
                self.database.learn_keyword(
                    keyword=keyword,
                    category="technical",
                    context=f"Found in {analysis_result['source']} analysis",
                    sentiment=0.2,
                )

        for keyword in self.core.integrity_keywords:
            if keyword in content:
                self.database.learn_keyword(
                    keyword=keyword,
                    category="integrity",
                    context=f"Found in {analysis_result['source']} analysis",
                    sentiment=0.3,
                )

        # 3. 精度測定記録
        if analysis["suetake_likeness_index"] > self.current_accuracy:
            self.database.record_accuracy_measurement(
                emotion=0.8,  # プレースホルダー
                expression=0.85,  # プレースホルダー
                value=analysis["suetake_likeness_index"] / 100.0,
                overall=analysis["suetake_likeness_index"] / 100.0,
                suggestions=f"統合分析により精度向上: {analysis['suetake_likeness_index']}%",
            )

    def _check_evolution_progress(self, analysis_result: Dict) -> Dict[str, Any]:
        """精度進化プロセスチェック"""

        current_score = analysis_result["analysis"]["suetake_likeness_index"]

        # 進化段階判定
        evolution_stage = self._get_evolution_stage(current_score)
        # progress_percentageを100%以内に制限（データベース制約対応）
        progress_percentage = min((current_score / self.target_accuracy) * 100, 100.0)

        # マイルストーン達成判定
        milestone_achieved = (
            current_score >= 90.0 and current_score > self.current_accuracy
        )

        if milestone_achieved:
            logger.info(f"🎉 マイルストーン達成! 精度: {current_score}%")

        # 学習進捗記録（制約対応: current値も1.0以内に制限）
        self.database.record_learning_progress(
            phase=evolution_stage,
            target=self.target_accuracy / 100.0,
            current=min(current_score / 100.0, 1.0),  # 1.0以内に制限
            method="integrated_mirralism_analysis",
            notes=f"統合分析による進捗: {current_score}% → 目標: {self.target_accuracy}%",
        )

        # 精度更新
        if current_score > self.current_accuracy:
            self.current_accuracy = current_score
            self.core.update_learning_accuracy(current_score)

        return {
            "evolution_stage": evolution_stage,
            "progress_percentage": progress_percentage,
            "milestone_achieved": milestone_achieved,
            "accuracy_improved": current_score > self.current_accuracy,
            "current_accuracy": self.current_accuracy,
            "target_accuracy": self.target_accuracy,
        }

    def _get_evolution_stage(self, accuracy: float) -> str:
        """精度に基づく進化段階取得"""
        # データベース制約に準拠したフェーズ名にマッピング
        evolution_mapping = {
            53.0: "initial",  # V1_baseline
            61.0: "initial",  # V1_learned
            70.0: "training",  # V2_training
            80.0: "validation",  # V2_validation
            90.0: "production",  # V2_production_ready
            95.0: "production",  # V2_target_achieved
        }

        # ``dict_items`` does not guarantee ``reversed`` support on all
        # Python versions.  Sort the thresholds explicitly in descending
        # order so the function behaves consistently on Python 3.9+.
        for threshold, stage in sorted(
            evolution_mapping.items(), key=lambda x: x[0], reverse=True
        ):
            if accuracy >= threshold:
                return stage
        return "initial"

    def _calculate_task_learning_correlation(
        self, accuracy: float, task_context: Dict
    ) -> float:
        """TaskMaster連携: タスク完了と学習効果の相関計算"""

        base_correlation = 0.5

        # タスク種別による学習影響度
        task_title = task_context.get("title", "").lower()

        if "personality" in task_title or "learning" in task_title:
            base_correlation += 0.3
        elif "database" in task_title or "integration" in task_title:
            base_correlation += 0.2
        elif "mirralism" in task_title or "v2" in task_title:
            base_correlation += 0.25

        # 精度による補正
        accuracy_factor = (accuracy - 50.0) / 50.0  # 50%を基準とした正規化

        return min(base_correlation + accuracy_factor * 0.2, 1.0)

    def correlate_with_task(
        self,
        task_id: int,
        task_title: str,
        task_status: str,
        learning_elements: int = 0,
    ) -> bool:
        """TaskMaster連携: タスク完了と学習効果の相関記録"""

        try:
            # 学習影響度計算
            learning_impact = self._calculate_task_learning_correlation(
                self.current_accuracy,
                {"title": task_title, "status": task_status},
            )

            # データベース記録
            self.database.correlate_task_learning(
                task_id=task_id,
                task_title=task_title,
                learning_impact=learning_impact,
                elements_discovered=learning_elements,
                accuracy_before=self.current_accuracy,
                accuracy_after=self.current_accuracy,  # 実分析後に更新
            )

            logger.info(f"TaskMaster連携記録: Task {task_id}, 学習影響度: {learning_impact}")
            return True

        except Exception as e:
            logger.error(f"TaskMaster連携エラー: {e}")
            return False

    def register_voice_analysis(
        self,
        file_path: str,
        transcription: str,
        duration: float,
        confidence: float = 0.8,
    ) -> Optional[int]:
        """SuperWhisper統合: 音声データ登録"""

        try:
            # データベース登録
            voice_id = self.database.register_voice_data(
                file_path=file_path,
                file_name=os.path.basename(file_path),
                duration=duration,
                transcription=transcription,
                confidence=confidence,
            )

            logger.info(f"SuperWhisper音声データ登録: {file_path}, ID: {voice_id}")
            return voice_id

        except Exception as e:
            logger.error(f"音声データ登録エラー: {e}")
            return None

    def get_evolution_status(self) -> Dict[str, Any]:
        """53%→95%進化状況取得"""

        return {
            "current_accuracy": self.current_accuracy,
            "target_accuracy": self.target_accuracy,
            "progress_percentage": (self.current_accuracy / self.target_accuracy) * 100,
            "evolution_stage": self._get_evolution_stage(self.current_accuracy),
            "accuracy_gap": self.target_accuracy - self.current_accuracy,
            "database_status": self.database.get_learning_stats(),
            "version": self.version,
        }

    def get_system_health(self) -> Dict[str, Any]:
        """統合システム健全性チェック"""

        try:
            core_status = self.core.get_system_status()
            db_stats = self.database.get_learning_stats()
            evolution_status = self.get_evolution_status()

            return {
                "system_healthy": True,
                "core_system": core_status,
                "database_stats": db_stats,
                "evolution_progress": evolution_status,
                "integration_level": "full",
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"システム健全性チェックエラー: {e}")
            return {
                "system_healthy": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def close(self):
        """統合システム終了処理"""
        if hasattr(self, "database"):
            self.database.close()
        logger.info("MIRRALISM統合システム終了")


# グローバルインスタンス（シングルトンパターン）
_mirralism_instance = None


def get_mirralism_system(
    db_path: Optional[str] = None,
) -> MirralismPersonalityLearning:
    """MIRRALISMシステムのグローバルインスタンス取得"""
    global _mirralism_instance

    if _mirralism_instance is None:
        _mirralism_instance = MirralismPersonalityLearning(db_path)

    return _mirralism_instance


# テスト実行用
if __name__ == "__main__":
    # 統合システムテスト
    system = get_mirralism_system()

    print("🚀 MIRRALISM統合システムテスト開始")
    print("=" * 50)

    # 基本分析テスト
    test_content = """
    MIRRALISM V2の統合開発が順調に進んでいます。
    PersonalityLearningシステムの実装により、
    技術的な課題解決と品質向上を実現できています。
    """

    result = system.analyze_entry(content=test_content, source_type="journal")

    print(f"✅ 分析結果: {result['analysis']['suetake_likeness_index']}%")
    print(f"📊 進化状況: {result['evolution_status']['evolution_stage']}")

    # システム健全性チェック
    health = system.get_system_health()
    print(f"💚 システム健全性: {health['system_healthy']}")

    print("\n🎉 MIRRALISM統合システムテスト完了!")

    system.close()
