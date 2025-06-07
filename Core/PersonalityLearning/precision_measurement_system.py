#!/usr/bin/env python3
"""
MIRRALISM PersonalityLearning精度測定システム
95%精度の明確な定義・測定・評価を実現

Author: MIRRALISM Technical Team
Version: 1.0 (Precision Definition System)
Created: 2025-06-10 (CTO緊急指示対応)
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import statistics


@dataclass
class PrecisionMeasurement:
    """精度測定結果データクラス"""
    measurement_id: str
    timestamp: str
    precision_type: str  # "client_understanding", "proposal_accuracy"
    measured_value: float  # 0.0-1.0
    sample_count: int
    evaluator: str  # "suetake", "client", "automated"
    confidence_interval: Tuple[float, float]
    statistical_significance: bool
    measurement_context: Dict[str, Any]


class PersonalityLearningPrecisionSystem:
    """
    PersonalityLearning95%精度測定・評価システム
    
    明確な定義による測定可能な精度指標を確立
    """

    def __init__(self, project_root: Optional[Path] = None):
        """精度測定システム初期化"""
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.setup_logging()
        
        # 精度定義設定
        self.precision_definitions = {
            "client_understanding": {
                "description": "クライアントの価値観・課題・ニーズの理解精度",
                "measurement_method": "末武さんによる評価（1-5スケール）",
                "target_accuracy": 0.95,
                "minimum_samples": 30,
                "evaluation_criteria": [
                    "価値観の正確な把握",
                    "課題の本質的理解", 
                    "ニーズの具体化精度",
                    "提案適合度"
                ]
            },
            "proposal_accuracy": {
                "description": "提案内容がクライアント要求に適合する精度",
                "measurement_method": "クライアント満足度 + 末武さん評価",
                "target_accuracy": 0.95,
                "minimum_samples": 20,
                "evaluation_criteria": [
                    "要求仕様との適合度",
                    "価値提供の具体性",
                    "実現可能性",
                    "コストパフォーマンス"
                ]
            },
            "behavior_prediction": {
                "description": "クライアントの反応・行動予測精度",
                "measurement_method": "予測vs実際の結果比較",
                "target_accuracy": 0.95,
                "minimum_samples": 50,
                "evaluation_criteria": [
                    "意思決定パターン予測",
                    "反応タイミング予測",
                    "優先順位予測",
                    "懸念事項予測"
                ]
            }
        }
        
        # 測定履歴保存パス
        self.measurements_file = self.project_root / "Data" / "personality_learning_precision.json"
        self.measurements_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 既存測定履歴読み込み
        self.measurement_history = self._load_measurement_history()
        
        logger.info("PersonalityLearning精度測定システム初期化完了")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - PRECISION_SYSTEM - %(levelname)s - %(message)s"
        )
        global logger
        logger = logging.getLogger(__name__)

    def _load_measurement_history(self) -> List[Dict[str, Any]]:
        """測定履歴読み込み"""
        try:
            if self.measurements_file.exists():
                with open(self.measurements_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("measurements", [])
            return []
        except Exception as e:
            logger.warning(f"測定履歴読み込みエラー: {e}")
            return []

    def _save_measurement_history(self):
        """測定履歴保存"""
        try:
            save_data = {
                "metadata": {
                    "version": "1.0",
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "precision_definitions": self.precision_definitions
                },
                "measurements": self.measurement_history
            }
            
            with open(self.measurements_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"測定履歴保存完了: {self.measurements_file}")
            
        except Exception as e:
            logger.error(f"測定履歴保存エラー: {e}")

    def record_measurement(
        self, 
        precision_type: str,
        measured_value: float,
        sample_count: int,
        evaluator: str,
        context: Dict[str, Any]
    ) -> PrecisionMeasurement:
        """
        精度測定結果記録
        
        Args:
            precision_type: 測定対象タイプ
            measured_value: 測定値（0.0-1.0）
            sample_count: サンプル数
            evaluator: 評価者
            context: 測定文脈情報
            
        Returns:
            PrecisionMeasurement: 測定結果
        """
        measurement_id = f"{precision_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 信頼区間計算（簡易版）
        confidence_interval = self._calculate_confidence_interval(measured_value, sample_count)
        
        # 統計的有意性判定
        statistical_significance = self._check_statistical_significance(
            precision_type, sample_count, measured_value
        )
        
        measurement = PrecisionMeasurement(
            measurement_id=measurement_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            precision_type=precision_type,
            measured_value=measured_value,
            sample_count=sample_count,
            evaluator=evaluator,
            confidence_interval=confidence_interval,
            statistical_significance=statistical_significance,
            measurement_context=context
        )
        
        # 履歴に追加
        self.measurement_history.append({
            "measurement_id": measurement.measurement_id,
            "timestamp": measurement.timestamp,
            "precision_type": measurement.precision_type,
            "measured_value": measurement.measured_value,
            "sample_count": measurement.sample_count,
            "evaluator": measurement.evaluator,
            "confidence_interval": measurement.confidence_interval,
            "statistical_significance": measurement.statistical_significance,
            "measurement_context": measurement.measurement_context
        })
        
        # 保存
        self._save_measurement_history()
        
        logger.info(f"精度測定記録完了: {measurement_id}, 精度: {measured_value:.1%}")
        
        return measurement

    def _calculate_confidence_interval(self, measured_value: float, sample_count: int) -> Tuple[float, float]:
        """信頼区間計算（95%信頼区間）"""
        if sample_count < 10:
            # サンプル数少ない場合は広い区間
            margin = 0.2
        else:
            # 正規近似による信頼区間
            import math
            z_score = 1.96  # 95%信頼区間
            standard_error = math.sqrt(measured_value * (1 - measured_value) / sample_count)
            margin = z_score * standard_error
            
        lower = max(0.0, measured_value - margin)
        upper = min(1.0, measured_value + margin)
        
        return (lower, upper)

    def _check_statistical_significance(
        self, precision_type: str, sample_count: int, measured_value: float
    ) -> bool:
        """統計的有意性判定"""
        definition = self.precision_definitions.get(precision_type, {})
        minimum_samples = definition.get("minimum_samples", 30)
        
        # 最小サンプル数チェック
        if sample_count < minimum_samples:
            return False
            
        # 95%目標との差の有意性（簡易版）
        target = definition.get("target_accuracy", 0.95)
        if abs(measured_value - target) < 0.05:  # 5%以内なら有意
            return True
            
        return sample_count >= minimum_samples

    def get_current_precision_status(self) -> Dict[str, Any]:
        """現在の精度状況取得"""
        status = {
            "summary": {
                "total_measurements": len(self.measurement_history),
                "precision_types": list(self.precision_definitions.keys()),
                "last_measurement": None,
                "overall_status": "未測定"
            },
            "by_type": {}
        }
        
        if self.measurement_history:
            # 最新測定
            latest = max(self.measurement_history, key=lambda x: x["timestamp"])
            status["summary"]["last_measurement"] = latest["timestamp"]
            
            # タイプ別集計
            for precision_type in self.precision_definitions.keys():
                type_measurements = [
                    m for m in self.measurement_history 
                    if m["precision_type"] == precision_type
                ]
                
                if type_measurements:
                    latest_type = max(type_measurements, key=lambda x: x["timestamp"])
                    avg_precision = statistics.mean([m["measured_value"] for m in type_measurements])
                    
                    status["by_type"][precision_type] = {
                        "latest_measurement": latest_type,
                        "average_precision": avg_precision,
                        "measurement_count": len(type_measurements),
                        "target_achieved": avg_precision >= self.precision_definitions[precision_type]["target_accuracy"]
                    }
                else:
                    status["by_type"][precision_type] = {
                        "latest_measurement": None,
                        "average_precision": 0.0,
                        "measurement_count": 0,
                        "target_achieved": False
                    }
        
        # 全体状況判定
        if status["summary"]["total_measurements"] == 0:
            status["summary"]["overall_status"] = "未測定"
        else:
            achieved_types = sum(1 for type_status in status["by_type"].values() if type_status["target_achieved"])
            total_types = len(self.precision_definitions)
            
            if achieved_types == total_types:
                status["summary"]["overall_status"] = "95%目標達成"
            elif achieved_types > 0:
                status["summary"]["overall_status"] = f"部分達成（{achieved_types}/{total_types}）"
            else:
                status["summary"]["overall_status"] = "目標未達成"
        
        return status

    def generate_precision_report(self) -> Dict[str, Any]:
        """精度測定レポート生成"""
        status = self.get_current_precision_status()
        
        report = {
            "report_metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "report_type": "precision_measurement_report",
                "version": "1.0"
            },
            "precision_definitions": self.precision_definitions,
            "current_status": status,
            "recommendations": self._generate_recommendations(status),
            "measurement_history": self.measurement_history
        }
        
        return report

    def _generate_recommendations(self, status: Dict[str, Any]) -> List[str]:
        """改善推奨事項生成"""
        recommendations = []
        
        if status["summary"]["total_measurements"] == 0:
            recommendations.append("【緊急】まず基本的な精度測定を実施してください")
            recommendations.append("client_understandingから開始することを推奨")
            
        for precision_type, type_status in status["by_type"].items():
            definition = self.precision_definitions[precision_type]
            
            if type_status["measurement_count"] == 0:
                recommendations.append(f"【要対応】{precision_type}の測定を開始してください")
                
            elif type_status["measurement_count"] < definition["minimum_samples"]:
                needed = definition["minimum_samples"] - type_status["measurement_count"]
                recommendations.append(f"【統計的信頼性】{precision_type}：あと{needed}サンプル必要")
                
            elif not type_status["target_achieved"]:
                current = type_status["average_precision"]
                target = definition["target_accuracy"]
                gap = target - current
                recommendations.append(f"【精度向上】{precision_type}：{gap:.1%}の改善が必要")
        
        return recommendations

# 使用例・テスト関数
def run_precision_system_test():
    """精度測定システムテスト実行"""
    system = PersonalityLearningPrecisionSystem()
    
    # テスト測定記録
    test_measurement = system.record_measurement(
        precision_type="client_understanding",
        measured_value=0.87,
        sample_count=25,
        evaluator="suetake",
        context={
            "client": "黒澤工務店",
            "measurement_date": "2025-06-10",
            "notes": "初期測定テスト"
        }
    )
    
    # 現在状況確認
    status = system.get_current_precision_status()
    
    # レポート生成
    report = system.generate_precision_report()
    
    logger.info("精度測定システムテスト完了")
    return {
        "test_measurement": test_measurement,
        "current_status": status,
        "report": report
    }

if __name__ == "__main__":
    run_precision_system_test() 