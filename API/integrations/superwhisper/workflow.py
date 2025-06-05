#!/usr/bin/env python3
"""
SuperWhisper 自動処理ワークフロー（MIRRALISM V2）
=============================================

完全自動化フロー:
1. SuperWhisper音声データ検知
2. 時刻バグ修正 + PersonalityLearning統合分析
3. TaskMaster連携（必要に応じて）
4. 分類別データ保存
5. 進化ステータス更新

作成者: MIRRALISM統合チーム
作成日: 2025年6月3日
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

# MIRRALISM統合インポート
sys.path.append(str(Path(__file__).parent))
from core import SuperWhisperMirralismIntegration

# TaskMaster統合準備
try:
    sys.path.append(str(Path(__file__).parent.parent.parent.parent))
    # TaskMaster統合は後のフェーズで実装
    TASKMASTER_AVAILABLE = False
except ImportError:
    TASKMASTER_AVAILABLE = False


class SuperWhisperAutoWorkflow:
    """SuperWhisper自動処理ワークフロー"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        ワークフロー初期化

        Args:
            project_root: MIRRALISMプロジェクトルート
        """
        self.project_root = project_root or Path(__file__).parent.parent.parent.parent
        self.integration = SuperWhisperMirralismIntegration(self.project_root)
        self.setup_logging()

        # 処理統計
        self.session_stats = {
            "processed_count": 0,
            "success_count": 0,
            "error_count": 0,
            "personality_learning_updates": 0,
            "task_correlations": 0,
            "session_start": datetime.now().isoformat(),
        }

        self.logger.info("🚀 SuperWhisper自動ワークフロー開始")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def process_audio_input(self, audio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        音声入力の完全自動処理

        Args:
            audio_data: SuperWhisperからの音声データ

        Returns:
            処理結果
        """
        self.session_stats["processed_count"] += 1
        process_id = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            self.logger.info(f"🎤 音声処理開始: {process_id}")

            # Phase 1: 基本統合処理
            integration_result = self.integration.process_voice_input(
                audio_data,
                classification=self._classify_audio_content(audio_data),
            )

            if not integration_result["success"]:
                raise Exception(f"統合処理失敗: {integration_result.get('error', 'unknown')}")

            # Phase 2: PersonalityLearning分析拡張
            enhanced_analysis = self._enhance_personality_analysis(
                integration_result["integrated_data"]
            )

            # Phase 3: TaskMaster相関分析（Phase 3で実装）
            task_correlation = self._analyze_task_correlation(enhanced_analysis)

            # Phase 4: 自動分類・保存
            final_result = self._finalize_processing(
                enhanced_analysis, task_correlation, process_id
            )

            # 統計更新
            self.session_stats["success_count"] += 1
            if enhanced_analysis.get("personality_learning_updated", False):
                self.session_stats["personality_learning_updates"] += 1
            if task_correlation.get("correlation_found", False):
                self.session_stats["task_correlations"] += 1

            self.logger.info(f"✅ 音声処理完了: {process_id}")

            return {
                "success": True,
                "process_id": process_id,
                "integration_result": integration_result,
                "enhanced_analysis": enhanced_analysis,
                "task_correlation": task_correlation,
                "final_result": final_result,
                "session_stats": self.session_stats,
            }

        except Exception as e:
            self.session_stats["error_count"] += 1
            self.logger.error(f"❌ 音声処理エラー ({process_id}): {e}")

            return {
                "success": False,
                "process_id": process_id,
                "error": str(e),
                "audio_data": audio_data,
                "session_stats": self.session_stats,
            }

    def _classify_audio_content(self, audio_data: Dict[str, Any]) -> str:
        """
        音声内容の自動分類

        Args:
            audio_data: 音声データ

        Returns:
            分類結果 (thought, task, idea, reflection, etc.)
        """
        text_content = audio_data.get("text_content", "").lower()

        # キーワードベース分類
        task_keywords = [
            "タスク",
            "やること",
            "todo",
            "する必要",
            "実装",
            "作業",
        ]
        idea_keywords = ["アイデア", "考え", "思いつき", "ひらめき", "発想"]
        reflection_keywords = ["振り返り", "反省", "学び", "気づき", "感想"]

        # 分類判定
        if any(keyword in text_content for keyword in task_keywords):
            return "task"
        elif any(keyword in text_content for keyword in idea_keywords):
            return "idea"
        elif any(keyword in text_content for keyword in reflection_keywords):
            return "reflection"
        else:
            return "thought"  # デフォルト

    def _enhance_personality_analysis(
        self, integrated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PersonalityLearning分析の拡張処理

        Args:
            integrated_data: 統合済みデータ

        Returns:
            拡張分析結果
        """
        enhanced = integrated_data.copy()

        # PersonalityLearning結果の詳細分析
        analysis_result = enhanced.get("analysis_result")
        if analysis_result and analysis_result.get("success"):
            # 精度進化チェック
            confidence = analysis_result.get("confidence", 0.0)
            evolution_status = analysis_result.get("evolution_status", {})

            # 学習効果指標計算
            learning_impact = self._calculate_learning_impact(
                confidence, evolution_status
            )

            enhanced["personality_learning_enhanced"] = {
                "learning_impact": learning_impact,
                "confidence_score": confidence,
                "evolution_stage": evolution_status.get("current_stage", "unknown"),
                "voice_weight_applied": True,
                "analysis_timestamp": datetime.now().isoformat(),
            }

            # 高精度判定
            if confidence > 80.0:
                enhanced["high_confidence_analysis"] = True
                enhanced["personality_learning_updated"] = True
                self.logger.info(f"🎯 高精度分析達成: {confidence}%")

        return enhanced

    def _calculate_learning_impact(
        self, confidence: float, evolution_status: Dict
    ) -> float:
        """
        学習効果影響度計算

        Args:
            confidence: 分析精度
            evolution_status: 進化ステータス

        Returns:
            学習影響度 (0.0-1.0)
        """
        base_impact = confidence / 100.0

        # 進化ステージボーナス
        stage_bonus = 0.0
        if evolution_status.get("stage_updated", False):
            stage_bonus = 0.2

        # 音声データボーナス（1.5倍重み付け反映）
        voice_bonus = 0.1

        return min(1.0, base_impact + stage_bonus + voice_bonus)

    def _analyze_task_correlation(
        self, enhanced_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        TaskMaster相関分析（Phase 3で詳細実装）

        Args:
            enhanced_data: 拡張分析データ

        Returns:
            TaskMaster相関結果
        """
        # 現在は基本的な相関検知のみ
        classification = enhanced_data.get("classification", "thought")
        text_content = enhanced_data.get("text_content", "")

        correlation_result = {
            "correlation_found": False,
            "suggested_actions": [],
            "task_keywords": [],
            "classification": classification,
        }

        # タスク関連キーワード検知
        if classification == "task":
            task_keywords = self._extract_task_keywords(text_content)
            if task_keywords:
                correlation_result.update(
                    {
                        "correlation_found": True,
                        "task_keywords": task_keywords,
                        "suggested_actions": [
                            "TaskMaster新規タスク作成を検討",
                            "既存タスクとの関連性確認",
                        ],
                    }
                )

        return correlation_result

    def _extract_task_keywords(self, text_content: str) -> List[str]:
        """
        タスク関連キーワード抽出

        Args:
            text_content: テキスト内容

        Returns:
            抽出されたキーワード
        """
        keywords = []
        task_patterns = [
            "実装",
            "作成",
            "修正",
            "更新",
            "追加",
            "削除",
            "テスト",
            "デプロイ",
            "設計",
            "分析",
            "検証",
            "レビュー",
        ]

        for pattern in task_patterns:
            if pattern in text_content:
                keywords.append(pattern)

        return keywords

    def _finalize_processing(
        self,
        enhanced_data: Dict[str, Any],
        task_correlation: Dict[str, Any],
        process_id: str,
    ) -> Dict[str, Any]:
        """
        処理最終化

        Args:
            enhanced_data: 拡張分析データ
            task_correlation: TaskMaster相関データ
            process_id: 処理ID

        Returns:
            最終処理結果
        """
        final_data = {
            **enhanced_data,
            "task_correlation": task_correlation,
            "process_id": process_id,
            "workflow_version": "v2.1_auto",
            "finalized_timestamp": datetime.now().isoformat(),
        }

        # 処理結果サマリー
        summary = {
            "classification": enhanced_data.get("classification", "unknown"),
            "personality_learning_confidence": enhanced_data.get(
                "analysis_result", {}
            ).get("confidence", 0.0),
            "task_correlation_found": task_correlation.get("correlation_found", False),
            "learning_impact": enhanced_data.get(
                "personality_learning_enhanced", {}
            ).get("learning_impact", 0.0),
            "process_id": process_id,
        }

        final_data["processing_summary"] = summary

        # 追加保存（詳細ログ）
        self._save_processing_log(final_data)

        return final_data

    def _save_processing_log(self, final_data: Dict[str, Any]):
        """
        処理ログ保存

        Args:
            final_data: 最終処理データ
        """
        try:
            log_dir = self.project_root / "Data" / "processing_logs"
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = (
                log_dir / f"superwhisper_workflow_{final_data['process_id']}.json"
            )

            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2, default=str)

            self.logger.info(f"📝 処理ログ保存: {log_file}")

        except Exception as e:
            self.logger.error(f"❌ 処理ログ保存失敗: {e}")

    def get_session_summary(self) -> Dict[str, Any]:
        """
        セッション要約取得

        Returns:
            セッション統計
        """
        session_duration = (
            datetime.now() - datetime.fromisoformat(self.session_stats["session_start"])
        ).total_seconds()

        return {
            **self.session_stats,
            "session_duration_seconds": session_duration,
            "success_rate": (
                self.session_stats["success_count"]
                / max(1, self.session_stats["processed_count"])
            )
            * 100,
            "integration_status": self.integration.get_integration_status(),
        }


# ワークフロー実行インターフェース
def process_superwhisper_input(audio_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    SuperWhisper入力の自動処理エントリーポイント

    Args:
        audio_data: SuperWhisperからの音声データ

    Returns:
        処理結果
    """
    workflow = SuperWhisperAutoWorkflow()
    return workflow.process_audio_input(audio_data)


if __name__ == "__main__":
    # テスト実行
    test_audio = {
        "text_content": "MIRRALISMプロジェクトのPersonalityLearning統合を完了させる必要がある",
        "created_time": "2025-06-03T19:30:00+09:00",
        "notion_id": "test_123",
        "quality_score": 0.95,
    }

    result = process_superwhisper_input(test_audio)

    print("🚀 SuperWhisper自動ワークフローテスト")
    print("=" * 50)
    print(f"成功: {result['success']}")
    if result["success"]:
        summary = result["final_result"]["processing_summary"]
        print(f"分類: {summary['classification']}")
        print(f"PersonalityLearning精度: {summary['personality_learning_confidence']}%")
        print(f"TaskMaster相関: {summary['task_correlation_found']}")
        print(f"学習影響度: {summary['learning_impact']:.2f}")
    else:
        print(f"エラー: {result['error']}")
