#!/usr/bin/env python3
"""
MIRRALISM Scientific Measurement Framework
進化的適応性を持つPersonalityLearning科学的測定システム

戦略的目標:
- 技術進化への適応性確保
- 測定精度の科学的根拠確立
- 競合優位性の技術的基盤構築
"""

import json
import logging
import sqlite3
import statistics
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Protocol
from typing import Tuple

import numpy as np
from scipy import stats

# ログ設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MeasurementStrategy(Enum):
    """測定戦略の進化的定義"""

    STATISTICAL_BASELINE = "statistical_baseline"
    CROSS_VALIDATION = "cross_validation"
    BAYESIAN_INFERENCE = "bayesian_inference"
    QUANTUM_MEASUREMENT = "quantum_measurement"  # 将来対応
    NEURAL_CORRELATION = "neural_correlation"  # 将来対応


class EvolutionStage(Enum):
    """進化段階の定義"""

    V1_BASELINE = "v1_baseline"  # 53.0%
    V1_LEARNED = "v1_learned"  # 61.0%
    V2_TRAINING = "v2_training"  # 70.0%
    V2_VALIDATION = "v2_validation"  # 80.0%
    V2_PRODUCTION = "v2_production"  # 90.0%
    V2_TARGET = "v2_target"  # 95.0%


@dataclass
class MeasurementResult:
    """科学的測定結果の構造化"""

    accuracy: float
    confidence_interval: Tuple[float, float]
    statistical_significance: float
    measurement_method: str
    sample_size: int
    timestamp: datetime
    metadata: Dict[str, Any]
    evidence_trace: List[str]


class MeasurementProtocol(Protocol):
    """測定プロトコルのインターフェース（将来拡張用）"""

    def measure(self, data: Any) -> MeasurementResult:
        """測定実行"""
        ...

    def validate(self, result: MeasurementResult) -> bool:
        """結果検証"""
        ...


class PluginableMeasurementFramework:
    """プラグイン型測定フレームワーク

    将来の技術変化に対応するための拡張可能アーキテクチャ
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or "scientific_measurements.db"
        self.measurement_plugins: Dict[str, MeasurementProtocol] = {}
        self.evolution_tracker = EvolutionTracker()
        self._initialize_database()
        self._register_core_plugins()

        logger.info("科学的測定フレームワーク初期化完了")

    def _initialize_database(self):
        """データベース初期化"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    accuracy REAL NOT NULL,
                    confidence_lower REAL NOT NULL,
                    confidence_upper REAL NOT NULL,
                    statistical_significance REAL NOT NULL,
                    measurement_method TEXT NOT NULL,
                    sample_size INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    evidence_trace TEXT NOT NULL
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS evolution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stage TEXT NOT NULL,
                    accuracy REAL NOT NULL,
                    achievement_date TEXT NOT NULL,
                    validation_method TEXT NOT NULL,
                    evidence TEXT NOT NULL
                )
            """
            )

    def _register_core_plugins(self):
        """コア測定プラグインの登録"""
        self.register_plugin("statistical_baseline", StatisticalBaselineMeasurement())
        self.register_plugin("cross_validation", CrossValidationMeasurement())
        # 将来的に追加: quantum_measurement, neural_correlation

    def register_plugin(self, name: str, plugin: MeasurementProtocol):
        """新しい測定プラグインの登録（拡張ポイント）"""
        self.measurement_plugins[name] = plugin
        logger.info(f"測定プラグイン登録: {name}")

    def measure_accuracy_scientifically(
        self,
        personality_data: List[Dict],
        method: str = "statistical_baseline",
        validation_mode: bool = True,
    ) -> MeasurementResult:
        """科学的精度測定の実行

        Args:
            personality_data: PersonalityLearning分析データ
            method: 使用する測定手法
            validation_mode: 検証モード（統計的有意性確認）

        Returns:
            科学的根拠を持つ測定結果
        """
        if method not in self.measurement_plugins:
            raise ValueError(f"未対応の測定手法: {method}")

        plugin = self.measurement_plugins[method]
        result = plugin.measure(personality_data)

        if validation_mode and not plugin.validate(result):
            logger.warning("測定結果の検証に失敗")

        # 結果の永続化
        self._store_measurement(result)

        # 進化段階の評価
        self.evolution_tracker.evaluate_progress(result.accuracy)

        logger.info(
            f"科学的測定完了: 精度={result.accuracy:.3f}, 信頼区間={result.confidence_interval}"
        )

        return result

    def _store_measurement(self, result: MeasurementResult):
        """測定結果の保存"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO measurements (
                    accuracy, confidence_lower, confidence_upper,
                    statistical_significance, measurement_method, sample_size,
                    timestamp, metadata, evidence_trace
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    result.accuracy,
                    result.confidence_interval[0],
                    result.confidence_interval[1],
                    result.statistical_significance,
                    result.measurement_method,
                    result.sample_size,
                    result.timestamp.isoformat(),
                    json.dumps(result.metadata),
                    json.dumps(result.evidence_trace),
                ),
            )

    def get_measurement_history(self, limit: int = 100) -> List[MeasurementResult]:
        """測定履歴の取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT * FROM measurements
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (limit,),
            )

            results = []
            for row in cursor.fetchall():
                results.append(
                    MeasurementResult(
                        accuracy=row[1],
                        confidence_interval=(row[2], row[3]),
                        statistical_significance=row[4],
                        measurement_method=row[5],
                        sample_size=row[6],
                        timestamp=datetime.fromisoformat(row[7]),
                        metadata=json.loads(row[8]),
                        evidence_trace=json.loads(row[9]),
                    )
                )

            return results

    def generate_scientific_report(self) -> Dict[str, Any]:
        """科学的測定レポートの生成"""
        history = self.get_measurement_history()

        if not history:
            return {"error": "測定データが不足しています"}

        accuracies = [r.accuracy for r in history]

        report = {
            "measurement_count": len(history),
            "current_accuracy": accuracies[0] if accuracies else 0,
            "average_accuracy": statistics.mean(accuracies),
            "accuracy_std": statistics.stdev(accuracies) if len(accuracies) > 1 else 0,
            "improvement_trend": self._calculate_trend(accuracies),
            "statistical_summary": {
                "min": min(accuracies),
                "max": max(accuracies),
                "median": statistics.median(accuracies),
                "quartiles": [
                    np.percentile(accuracies, 25),
                    np.percentile(accuracies, 75),
                ],
            },
            "evolution_status": self.evolution_tracker.get_current_status(),
            "validation_summary": {
                "validated_measurements": sum(
                    1 for r in history if r.statistical_significance < 0.05
                ),
                "total_measurements": len(history),
                "confidence_rate": sum(
                    1 for r in history if r.statistical_significance < 0.05
                )
                / len(history),
            },
        }

        return report

    def _calculate_trend(self, accuracies: List[float]) -> str:
        """精度向上トレンドの計算"""
        if len(accuracies) < 2:
            return "insufficient_data"

        # 線形回帰による傾向分析
        x = list(range(len(accuracies)))
        slope, _, r_value, p_value, _ = stats.linregress(x, accuracies)

        if p_value < 0.05:  # 統計的有意
            if slope > 0.001:
                return "significant_improvement"
            elif slope < -0.001:
                return "significant_decline"
            else:
                return "stable"
        else:
            return "no_significant_trend"


class StatisticalBaselineMeasurement:
    """統計的ベースライン測定"""

    def measure(self, data: List[Dict]) -> MeasurementResult:
        """統計的測定の実行"""
        if not data:
            raise ValueError("測定データが空です")

        # PersonalityLearning精度の統計的計算
        accuracies = []
        for entry in data:
            if "suetake_likeness_index" in entry:
                accuracies.append(entry["suetake_likeness_index"])

        if not accuracies:
            raise ValueError("精度データが見つかりません")

        # 統計的指標の計算
        mean_accuracy = statistics.mean(accuracies)
        std_accuracy = statistics.stdev(accuracies) if len(accuracies) > 1 else 0
        sample_size = len(accuracies)

        # 信頼区間の計算（95%信頼区間）
        confidence_interval = self._calculate_confidence_interval(
            mean_accuracy, std_accuracy, sample_size
        )

        # 統計的有意性（t検定）
        if sample_size > 1:
            t_stat, p_value = stats.ttest_1samp(accuracies, 0.5)  # 50%をヌル仮説
        else:
            p_value = 1.0

        return MeasurementResult(
            accuracy=mean_accuracy,
            confidence_interval=confidence_interval,
            statistical_significance=p_value,
            measurement_method="statistical_baseline",
            sample_size=sample_size,
            timestamp=datetime.now(),
            metadata={
                "std_deviation": std_accuracy,
                "raw_accuracies": accuracies,
                "t_statistic": t_stat if sample_size > 1 else None,
            },
            evidence_trace=[
                f"サンプルサイズ: {sample_size}",
                f"平均精度: {mean_accuracy:.3f}",
                f"標準偏差: {std_accuracy:.3f}",
                f"p値: {p_value:.3f}",
            ],
        )

    def validate(self, result: MeasurementResult) -> bool:
        """結果の検証"""
        # 基本的な妥当性チェック
        if not (0 <= result.accuracy <= 1):
            return False

        if result.sample_size < 1:
            return False

        # 統計的有意性のチェック
        if result.statistical_significance > 0.05:
            logger.warning("統計的有意性が不十分です")

        return True

    def _calculate_confidence_interval(
        self, mean: float, std: float, n: int, confidence: float = 0.95
    ) -> Tuple[float, float]:
        """信頼区間の計算"""
        if n <= 1:
            return (mean, mean)

        # t分布を使用（サンプルサイズが小さい場合）
        alpha = 1 - confidence
        t_critical = stats.t.ppf(1 - alpha / 2, n - 1)
        margin_of_error = t_critical * (std / np.sqrt(n))

        return (max(0, mean - margin_of_error), min(1, mean + margin_of_error))


class CrossValidationMeasurement:
    """交差検証による測定"""

    def measure(self, data: List[Dict]) -> MeasurementResult:
        """交差検証による精度測定"""
        if len(data) < 5:
            # サンプルが少ない場合はベースライン測定にフォールバック
            return StatisticalBaselineMeasurement().measure(data)

        # 5-fold交差検証
        fold_size = len(data) // 5
        accuracies = []

        for i in range(5):
            start_idx = i * fold_size
            end_idx = start_idx + fold_size if i < 4 else len(data)

            fold_data = data[start_idx:end_idx]
            fold_accuracies = [
                entry["suetake_likeness_index"]
                for entry in fold_data
                if "suetake_likeness_index" in entry
            ]

            if fold_accuracies:
                accuracies.append(statistics.mean(fold_accuracies))

        if not accuracies:
            raise ValueError("交差検証用データが不足")

        mean_accuracy = statistics.mean(accuracies)
        std_accuracy = statistics.stdev(accuracies) if len(accuracies) > 1 else 0

        # 信頼区間
        confidence_interval = self._calculate_cv_confidence_interval(accuracies)

        # 統計的有意性
        _, p_value = stats.ttest_1samp(accuracies, 0.5)

        return MeasurementResult(
            accuracy=mean_accuracy,
            confidence_interval=confidence_interval,
            statistical_significance=p_value,
            measurement_method="cross_validation",
            sample_size=len(data),
            timestamp=datetime.now(),
            metadata={
                "cv_folds": 5,
                "fold_accuracies": accuracies,
                "cv_std": std_accuracy,
            },
            evidence_trace=[
                f"5-fold交差検証実施",
                f"フォールド精度: {accuracies}",
                f"平均精度: {mean_accuracy:.3f}",
                f"CV標準偏差: {std_accuracy:.3f}",
            ],
        )

    def validate(self, result: MeasurementResult) -> bool:
        """結果の検証"""
        return StatisticalBaselineMeasurement().validate(result)

    def _calculate_cv_confidence_interval(
        self, accuracies: List[float], confidence: float = 0.95
    ) -> Tuple[float, float]:
        """交差検証の信頼区間計算"""
        if len(accuracies) <= 1:
            return (accuracies[0], accuracies[0]) if accuracies else (0, 0)

        mean = statistics.mean(accuracies)
        std = statistics.stdev(accuracies)
        n = len(accuracies)

        alpha = 1 - confidence
        t_critical = stats.t.ppf(1 - alpha / 2, n - 1)
        margin_of_error = t_critical * (std / np.sqrt(n))

        return (max(0, mean - margin_of_error), min(1, mean + margin_of_error))


class EvolutionTracker:
    """進化段階追跡システム"""

    def __init__(self):
        self.stage_thresholds = {
            EvolutionStage.V1_BASELINE: 0.53,
            EvolutionStage.V1_LEARNED: 0.61,
            EvolutionStage.V2_TRAINING: 0.70,
            EvolutionStage.V2_VALIDATION: 0.80,
            EvolutionStage.V2_PRODUCTION: 0.90,
            EvolutionStage.V2_TARGET: 0.95,
        }
        self.current_stage = EvolutionStage.V1_BASELINE

    def evaluate_progress(self, accuracy: float) -> EvolutionStage:
        """進化段階の評価"""
        for stage, threshold in reversed(list(self.stage_thresholds.items())):
            if accuracy >= threshold:
                if stage != self.current_stage:
                    logger.info(f"進化段階更新: {self.current_stage} → {stage}")
                    self.current_stage = stage
                break

        return self.current_stage

    def get_current_status(self) -> Dict[str, Any]:
        """現在の進化状況"""
        return {
            "current_stage": self.current_stage.value,
            "stage_thresholds": {s.value: t for s, t in self.stage_thresholds.items()},
            "next_milestone": self._get_next_milestone(),
            "progress_percentage": self._calculate_progress_percentage(),
        }

    def _get_next_milestone(self) -> Optional[Dict[str, Any]]:
        """次のマイルストーン"""
        stages = list(EvolutionStage)
        try:
            current_idx = stages.index(self.current_stage)
            if current_idx < len(stages) - 1:
                next_stage = stages[current_idx + 1]
                return {
                    "stage": next_stage.value,
                    "threshold": self.stage_thresholds[next_stage],
                }
        except ValueError:
            pass
        return None

    def _calculate_progress_percentage(self) -> float:
        """進捗パーセンテージ"""
        total_stages = len(self.stage_thresholds)
        current_position = (
            list(self.stage_thresholds.keys()).index(self.current_stage) + 1
        )
        return (current_position / total_stages) * 100


# 将来拡張用のプラグインインターフェース例
class QuantumMeasurementPlugin:
    """量子測定プラグイン（将来実装）"""

    def measure(self, data: Any) -> MeasurementResult:
        """量子測定手法（プレースホルダー）"""
        raise NotImplementedError("量子測定は将来実装予定")

    def validate(self, result: MeasurementResult) -> bool:
        """量子測定結果の検証"""
        raise NotImplementedError("量子測定は将来実装予定")


class NeuralCorrelationPlugin:
    """神経相関測定プラグイン（将来実装）"""

    def measure(self, data: Any) -> MeasurementResult:
        """神経相関による測定（プレースホルダー）"""
        raise NotImplementedError("神経相関測定は将来実装予定")

    def validate(self, result: MeasurementResult) -> bool:
        """神経相関結果の検証"""
        raise NotImplementedError("神経相関測定は将来実装予定")


def main():
    """デモンストレーション"""
    framework = PluginableMeasurementFramework()

    # テストデータ
    test_data = [
        {"suetake_likeness_index": 0.85, "source": "test1"},
        {"suetake_likeness_index": 0.90, "source": "test2"},
        {"suetake_likeness_index": 0.82, "source": "test3"},
        {"suetake_likeness_index": 0.88, "source": "test4"},
        {"suetake_likeness_index": 0.91, "source": "test5"},
    ]

    # 科学的測定実行
    result = framework.measure_accuracy_scientifically(test_data)
    print(f"測定結果: {result.accuracy:.3f} (信頼区間: {result.confidence_interval})")

    # レポート生成
    report = framework.generate_scientific_report()
    print("科学的レポート:", json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
