# isort: skip_file
"""
SuperWhisper統合コアモジュール（MIRRALISM V2）
作成者: 技術責任者
作成日: 2025年6月3日
目的: SuperWhisper音声データとPersonalityLearning統合

🔧 重要な修正統合:
- 日本語環境時刻バグ修正適用
- PersonalityLearning V2データベース連携
- 53%→95%精度進化システム統合
- TaskMaster連携準備
"""

import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

# MIRRALISM Core統合
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "Core"))

try:
    from PersonalityLearning.integrated_system import (
        MirralismPersonalityLearning,
    )  # isort: skip
except ImportError as e:
    logging.warning(f"PersonalityLearning統合モジュールが見つかりません: {e}")
    MirralismPersonalityLearning = None


class SuperWhisperMirralismIntegration:
    """SuperWhisper-MIRRALISM統合システム"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        統合システム初期化

        Args:
            project_root: MIRRALISMプロジェクトルート
        """
        self.project_root = project_root or Path(__file__).parent.parent.parent.parent
        self.setup_logging()

        # PersonalityLearning統合初期化
        self.personality_learning = None
        if MirralismPersonalityLearning:
            try:
                self.personality_learning = MirralismPersonalityLearning()
                logging.info("✅ PersonalityLearning統合システム初期化完了")
            except Exception as e:
                logging.error(f"❌ PersonalityLearning初期化失敗: {e}")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def process_voice_input(
        self, audio_data: Dict[str, Any], classification: str = "thought"
    ) -> Dict[str, Any]:
        """
        音声入力の統合処理

        Args:
            audio_data: SuperWhisperからの音声データ
            classification: データ分類（thought, task, idea等）

        Returns:
            処理結果
        """
        try:
            # 🔧 時刻修正適用
            audio_data = self._apply_datetime_fix(audio_data)

            # PersonalityLearning分析
            analysis_result = None
            if self.personality_learning and audio_data.get("text_content"):
                analysis_result = self._analyze_with_personality_learning(
                    audio_data["text_content"],
                    source_type="voice",
                    quality_score=audio_data.get("quality_score", 1.0),
                )

            # 統合データ作成
            integrated_data = {
                **audio_data,
                "analysis_result": analysis_result,
                "processing_timestamp": datetime.now(timezone.utc).isoformat(),
                "integration_version": "v2.1_mirralism",
                "classification": classification,
            }

            # 保存・配置処理
            save_result = self._save_integrated_data(integrated_data)

            self.logger.info(f"✅ 音声データ統合処理完了: {audio_data.get('notion_id', 'unknown')}")

            return {
                "success": True,
                "integrated_data": integrated_data,
                "save_result": save_result,
                "analysis_summary": (
                    analysis_result.get("summary") if analysis_result else None
                ),
            }

        except Exception as e:
            self.logger.error(f"❌ 音声統合処理エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_data": audio_data,
            }

    def _apply_datetime_fix(self, audio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        時刻バグ修正適用（時刻統合システムから移植）

        Args:
            audio_data: 音声データ

        Returns:
            修正済み音声データ
        """
        if "created_time" in audio_data:
            raw_time = audio_data["created_time"]

            # 不完全時刻の修正
            if isinstance(raw_time, str):
                # "2025-05-31" → "2025-05-31T00:00:00+00:00"
                if len(raw_time) == 10 and raw_time.count("-") == 2:
                    audio_data["created_time"] = f"{raw_time}T00:00:00+00:00"
                    audio_data["datetime_fix_applied"] = True
                    self.logger.info(
                        f"🔧 時刻修正適用: {raw_time} → {audio_data['created_time']}"
                    )

        return audio_data

    def _analyze_with_personality_learning(
        self,
        text_content: str,
        source_type: str = "voice",
        quality_score: float = 1.0,
    ) -> Optional[Dict[str, Any]]:
        """
        PersonalityLearning分析実行

        Args:
            text_content: テキスト内容
            source_type: データソース種別
            quality_score: 音声品質スコア

        Returns:
            分析結果
        """
        if not self.personality_learning:
            return None

        try:
            # 音声データ準備
            voice_data = None
            if source_type == "voice":
                voice_data = {
                    "quality_score": quality_score,
                    "source": "superwhisper",
                    "weight_multiplier": 1.5,
                }

            # 統合分析実行
            result = self.personality_learning.analyze_entry(
                content=text_content,
                source_type=source_type,
                voice_data=voice_data,
            )

            if result.get("success", False):
                # 学習進捗記録
                analysis_accuracy = result.get("analysis", {}).get(
                    "suetake_likeness_index", 0.0
                )

                # 進化ステータス更新
                evolution_status = result.get("evolution_status", {})
                if evolution_status.get("stage_updated", False):
                    self.logger.info(
                        f"🎯 精度進化: {evolution_status.get('new_stage', 'unknown')}"
                    )

                return {
                    "success": True,
                    "confidence": analysis_accuracy,
                    "analysis": result.get("analysis", {}),
                    "evolution_status": evolution_status,
                    "summary": f"精度: {analysis_accuracy}% | 重み: {quality_score}",
                }
            else:
                self.logger.warning(
                    f"⚠️ PersonalityLearning分析失敗: {result.get('error', 'unknown')}"
                )
                return None

        except Exception as e:
            self.logger.error(f"❌ PersonalityLearning分析エラー: {e}")
            return None

    def _save_integrated_data(self, integrated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        統合データ保存

        Args:
            integrated_data: 統合済みデータ

        Returns:
            保存結果
        """
        try:
            # 分類に応じた保存先決定
            classification = integrated_data.get("classification", "thought")

            if classification == "thought":
                save_path = self.project_root / "Data" / "personal_thoughts"
            elif classification == "task":
                save_path = self.project_root / "Data" / "tasks"
            else:
                save_path = self.project_root / "Data" / "voice_inputs"

            save_path.mkdir(parents=True, exist_ok=True)

            # ファイル名生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            notion_id = integrated_data.get("notion_id", "unknown")
            filename = f"superwhisper_{timestamp}_{notion_id}.json"

            # データ保存
            import json

            file_path = save_path / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(integrated_data, f, ensure_ascii=False, indent=2)

            self.logger.info(f"✅ データ保存完了: {file_path}")

            return {
                "success": True,
                "file_path": str(file_path),
                "classification": classification,
            }

        except Exception as e:
            self.logger.error(f"❌ データ保存エラー: {e}")
            return {"success": False, "error": str(e)}

    def get_integration_status(self) -> Dict[str, Any]:
        """
        統合システム状態取得

        Returns:
            システム状態
        """
        return {
            "datetime_fix_available": True,
            "personality_learning_available": self.personality_learning is not None,
            "project_root": str(self.project_root),
            "version": "v2.1_mirralism",
            "components": {
                "superwhisper_integration": True,
                "datetime_fix": True,
                "personality_learning": self.personality_learning is not None,
                "data_storage": True,
            },
        }


# モジュール初期化
def get_integration_instance(
    project_root: Optional[Path] = None,
) -> SuperWhisperMirralismIntegration:
    """統合システムインスタンス取得"""
    return SuperWhisperMirralismIntegration(project_root)


if __name__ == "__main__":
    # テスト実行
    integration = get_integration_instance()
    status = integration.get_integration_status()

    print("🚀 SuperWhisper-MIRRALISM統合システム")
    print("=" * 50)
    for key, value in status.items():
        print(f"{key}: {value}")
