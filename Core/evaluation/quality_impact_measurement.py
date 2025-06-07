#!/usr/bin/env python3
"""
MIRRALISM Evaluation Quality Impact Measurement
Purpose: Quantitative measurement of quality infrastructure impact on evaluation system
Design: Real-time metrics collection with historical comparison

Created: 2025-06-07
Version: 1.0.0
"""

import json
import time
import psutil
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
import statistics
from collections import defaultdict


@dataclass
class PerformanceMetric:
    """パフォーマンスメトリクス"""
    timestamp: datetime
    metric_type: str
    value: float
    unit: str
    context: Dict[str, any] = None


@dataclass
class QualityImpactReport:
    """品質影響レポート"""
    measurement_period: str
    baseline_period: str
    system_stability: Dict[str, float]
    evaluation_accuracy: Dict[str, float]
    development_efficiency: Dict[str, float]
    overall_improvement: float
    recommendations: List[str]


class QualityImpactMeasurement:
    """品質基盤影響測定システム"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "Data" / "quality_measurement"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # データベース初期化
        self.db_path = self.data_dir / "quality_impact.db"
        self._init_database()
        
        # ベースライン期間（品質基盤導入前）
        self.baseline_start = datetime(2025, 6, 1)
        self.baseline_end = datetime(2025, 6, 7, 19, 0)  # Phase 1開始前
        
        # 測定期間（品質基盤導入後）
        self.measurement_start = datetime(2025, 6, 7, 19, 0)  # Phase 1開始
        
        # ログ設定
        logging.basicConfig(level=logging.INFO)
        
    def _init_database(self):
        """データベース初期化"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # パフォーマンスメトリクステーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL,
                    context TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # システム安定性メトリクス
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stability_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    uptime_seconds REAL,
                    error_count INTEGER,
                    crash_count INTEGER,
                    recovery_time_seconds REAL,
                    memory_usage_mb REAL,
                    cpu_usage_percent REAL,
                    disk_usage_percent REAL
                )
            """)
            
            # 評価精度メトリクス
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accuracy_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    evaluation_id TEXT,
                    predicted_score REAL,
                    actual_score REAL,
                    accuracy_percentage REAL,
                    confidence_score REAL,
                    processing_time_ms REAL
                )
            """)
            
            # 開発効率メトリクス
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS efficiency_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    task_type TEXT,
                    completion_time_minutes REAL,
                    error_resolution_time_minutes REAL,
                    code_quality_score REAL,
                    automation_level_percent REAL
                )
            """)
            
            conn.commit()
            
    def collect_system_stability_metrics(self):
        """システム安定性メトリクス収集"""
        try:
            # システムリソース情報
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage('/')
            
            # プロセス稼働時間（概算）
            uptime = time.time() - psutil.boot_time()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO stability_metrics 
                    (timestamp, uptime_seconds, error_count, crash_count, 
                     recovery_time_seconds, memory_usage_mb, cpu_usage_percent, disk_usage_percent)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    uptime,
                    0,  # エラーカウント（別途実装）
                    0,  # クラッシュカウント（別途実装）
                    0,  # 復旧時間（別途実装）
                    memory.used / 1024 / 1024,  # MB
                    cpu_percent,
                    disk.percent
                ))
                conn.commit()
                
            logging.info(f"📊 System stability metrics collected: CPU {cpu_percent}%, Memory {memory.percent}%")
            
        except Exception as e:
            logging.error(f"Failed to collect system metrics: {e}")
            
    def collect_evaluation_accuracy_metrics(self, evaluation_id: str, predicted_score: float, 
                                          actual_score: float, processing_time_ms: float):
        """評価精度メトリクス収集"""
        accuracy = (1 - abs(predicted_score - actual_score) / 5.0) * 100  # 5点満点での精度
        confidence = min(100, accuracy + 10)  # 簡易信頼度計算
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO accuracy_metrics 
                (timestamp, evaluation_id, predicted_score, actual_score, 
                 accuracy_percentage, confidence_score, processing_time_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                evaluation_id,
                predicted_score,
                actual_score,
                accuracy,
                confidence,
                processing_time_ms
            ))
            conn.commit()
            
        logging.info(f"🎯 Evaluation accuracy recorded: {accuracy:.1f}% for evaluation {evaluation_id}")
        
    def collect_development_efficiency_metrics(self, task_type: str, completion_time_minutes: float,
                                             error_resolution_time_minutes: float = 0,
                                             code_quality_score: float = 100,
                                             automation_level: float = 100):
        """開発効率メトリクス収集"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO efficiency_metrics 
                (timestamp, task_type, completion_time_minutes, error_resolution_time_minutes,
                 code_quality_score, automation_level_percent)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                task_type,
                completion_time_minutes,
                error_resolution_time_minutes,
                code_quality_score,
                automation_level
            ))
            conn.commit()
            
        logging.info(f"⚡ Development efficiency recorded: {task_type} completed in {completion_time_minutes:.1f}min")
        
    def calculate_system_stability_impact(self) -> Dict[str, float]:
        """システム安定性影響計算"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # ベースライン期間のデータ
            cursor.execute("""
                SELECT AVG(memory_usage_mb), AVG(cpu_usage_percent), COUNT(*) as error_count
                FROM stability_metrics 
                WHERE timestamp BETWEEN ? AND ?
            """, (self.baseline_start.isoformat(), self.baseline_end.isoformat()))
            baseline_data = cursor.fetchone()
            
            # 測定期間のデータ
            cursor.execute("""
                SELECT AVG(memory_usage_mb), AVG(cpu_usage_percent), COUNT(*) as error_count
                FROM stability_metrics 
                WHERE timestamp >= ?
            """, (self.measurement_start.isoformat(),))
            current_data = cursor.fetchone()
            
        if not baseline_data or not current_data or baseline_data[0] is None or current_data[0] is None:
            # ベースラインデータが不足の場合は、V1仮定値と比較
            v1_baseline_memory = 2048.0  # MB (V1での平均メモリ使用量)
            v1_baseline_cpu = 45.0       # % (V1での平均CPU使用量)
            v1_baseline_errors = 10      # V1での平均エラー数
            
            if current_data and current_data[0] is not None:
                memory_improvement = ((v1_baseline_memory - current_data[0]) / v1_baseline_memory) * 100
                cpu_improvement = ((v1_baseline_cpu - current_data[1]) / v1_baseline_cpu) * 100
                error_improvement = ((v1_baseline_errors - current_data[2]) / max(v1_baseline_errors, 1)) * 100
            else:
                return {"downtime_reduction": 0, "resource_efficiency": 0, "error_rate_reduction": 0}
        else:
            # 改善率計算
            memory_improvement = ((baseline_data[0] - current_data[0]) / baseline_data[0]) * 100 if baseline_data[0] > 0 else 0
            cpu_improvement = ((baseline_data[1] - current_data[1]) / baseline_data[1]) * 100 if baseline_data[1] > 0 else 0
            error_improvement = ((baseline_data[2] - current_data[2]) / max(baseline_data[2], 1)) * 100
        
        return {
            "downtime_reduction": max(0, error_improvement),
            "resource_efficiency": max(0, (memory_improvement + cpu_improvement) / 2),
            "error_rate_reduction": max(0, error_improvement)
        }
        
    def calculate_evaluation_accuracy_impact(self) -> Dict[str, float]:
        """評価精度影響計算"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 測定期間の精度データ
            cursor.execute("""
                SELECT AVG(accuracy_percentage), AVG(confidence_score), AVG(processing_time_ms)
                FROM accuracy_metrics 
                WHERE timestamp >= ?
            """, (self.measurement_start.isoformat(),))
            current_data = cursor.fetchone()
            
        if not current_data or current_data[0] is None:
            return {"precision_improvement": 0, "confidence_increase": 0, "speed_improvement": 0}
            
        # V1ベースライン（仮定値）
        baseline_accuracy = 53.0  # V1の53%精度
        baseline_confidence = 60.0
        baseline_processing_time = 1000.0  # 1秒
        
        accuracy_improvement = ((current_data[0] - baseline_accuracy) / baseline_accuracy) * 100 if current_data[0] else 0
        confidence_improvement = ((current_data[1] - baseline_confidence) / baseline_confidence) * 100 if current_data[1] else 0
        speed_improvement = ((baseline_processing_time - current_data[2]) / baseline_processing_time) * 100 if current_data[2] else 0
        
        return {
            "precision_improvement": max(0, accuracy_improvement),
            "confidence_increase": max(0, confidence_improvement),
            "speed_improvement": max(0, speed_improvement)
        }
        
    def calculate_development_efficiency_impact(self) -> Dict[str, float]:
        """開発効率影響計算"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 測定期間の効率データ
            cursor.execute("""
                SELECT AVG(completion_time_minutes), AVG(error_resolution_time_minutes), 
                       AVG(code_quality_score), AVG(automation_level_percent)
                FROM efficiency_metrics 
                WHERE timestamp >= ?
            """, (self.measurement_start.isoformat(),))
            current_data = cursor.fetchone()
            
        if not current_data or current_data[0] is None:
            return {"task_completion_speedup": 0, "error_resolution_speedup": 0, "quality_improvement": 0}
            
        # V1ベースライン（仮定値）
        baseline_completion_time = 120.0  # 2時間
        baseline_error_resolution = 60.0   # 1時間
        baseline_quality = 70.0            # 70%
        
        completion_improvement = ((baseline_completion_time - current_data[0]) / baseline_completion_time) * 100
        resolution_improvement = ((baseline_error_resolution - current_data[1]) / baseline_error_resolution) * 100 if current_data[1] and current_data[1] > 0 else 100
        quality_improvement = ((current_data[2] - baseline_quality) / baseline_quality) * 100 if current_data[2] else 0
        
        return {
            "task_completion_speedup": max(0, completion_improvement),
            "error_resolution_speedup": max(0, resolution_improvement),
            "quality_improvement": max(0, quality_improvement)
        }
        
    def generate_impact_report(self) -> QualityImpactReport:
        """総合影響レポート生成"""
        # 各領域の影響計算
        stability_impact = self.calculate_system_stability_impact()
        accuracy_impact = self.calculate_evaluation_accuracy_impact()
        efficiency_impact = self.calculate_development_efficiency_impact()
        
        # 総合改善度計算
        all_improvements = []
        all_improvements.extend(stability_impact.values())
        all_improvements.extend(accuracy_impact.values())
        all_improvements.extend(efficiency_impact.values())
        
        overall_improvement = statistics.mean(all_improvements) if all_improvements else 0
        
        # 推奨事項生成
        recommendations = self._generate_recommendations(
            stability_impact, accuracy_impact, efficiency_impact
        )
        
        return QualityImpactReport(
            measurement_period=f"{self.measurement_start.isoformat()} - {datetime.now().isoformat()}",
            baseline_period=f"{self.baseline_start.isoformat()} - {self.baseline_end.isoformat()}",
            system_stability=stability_impact,
            evaluation_accuracy=accuracy_impact,
            development_efficiency=efficiency_impact,
            overall_improvement=overall_improvement,
            recommendations=recommendations
        )
        
    def _generate_recommendations(self, stability: Dict, accuracy: Dict, efficiency: Dict) -> List[str]:
        """推奨事項生成"""
        recommendations = []
        
        # 安定性の推奨
        if stability["error_rate_reduction"] < 50:
            recommendations.append("Consider implementing additional error prevention mechanisms")
            
        # 精度の推奨
        if accuracy["precision_improvement"] < 30:
            recommendations.append("Enhance PersonalityLearning training data quality")
            
        # 効率の推奨
        if efficiency["task_completion_speedup"] < 40:
            recommendations.append("Expand automation coverage for development tasks")
            
        if not recommendations:
            recommendations.append("Quality infrastructure is performing excellently")
            
        return recommendations
        
    def start_continuous_monitoring(self, interval_seconds: int = 300):
        """継続的監視開始"""
        logging.info(f"🔍 Starting continuous quality impact monitoring (interval: {interval_seconds}s)")
        
        try:
            while True:
                self.collect_system_stability_metrics()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logging.info("👋 Continuous monitoring stopped")
            
    def export_metrics_to_json(self, output_path: Optional[Path] = None) -> Path:
        """メトリクスのJSON出力"""
        if output_path is None:
            output_path = self.data_dir / f"quality_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        # 全メトリクス取得
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            metrics_data = {}
            
            # 安定性メトリクス
            cursor.execute("SELECT * FROM stability_metrics ORDER BY timestamp DESC LIMIT 100")
            metrics_data["stability"] = [dict(zip([col[0] for col in cursor.description], row)) 
                                       for row in cursor.fetchall()]
            
            # 精度メトリクス
            cursor.execute("SELECT * FROM accuracy_metrics ORDER BY timestamp DESC LIMIT 100")
            metrics_data["accuracy"] = [dict(zip([col[0] for col in cursor.description], row)) 
                                      for row in cursor.fetchall()]
            
            # 効率メトリクス
            cursor.execute("SELECT * FROM efficiency_metrics ORDER BY timestamp DESC LIMIT 100")
            metrics_data["efficiency"] = [dict(zip([col[0] for col in cursor.description], row)) 
                                        for row in cursor.fetchall()]
            
        # JSON出力
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False, default=str)
            
        logging.info(f"📁 Metrics exported to: {output_path}")
        return output_path


def main():
    """メイン実行"""
    measurement = QualityImpactMeasurement()
    
    # 現在のメトリクス収集
    measurement.collect_system_stability_metrics()
    
    # サンプル評価メトリクス
    measurement.collect_evaluation_accuracy_metrics(
        evaluation_id="test_001",
        predicted_score=4.2,
        actual_score=4.0,
        processing_time_ms=250
    )
    
    # サンプル開発効率メトリクス
    measurement.collect_development_efficiency_metrics(
        task_type="security_framework_implementation",
        completion_time_minutes=45,
        error_resolution_time_minutes=5,
        code_quality_score=95,
        automation_level=90
    )
    
    # 影響レポート生成
    report = measurement.generate_impact_report()
    
    print("🚀 MIRRALISM Quality Impact Report")
    print("=" * 50)
    print(f"📅 Measurement Period: {report.measurement_period}")
    print(f"📊 Overall Improvement: {report.overall_improvement:.1f}%")
    print()
    print("📈 System Stability:")
    for metric, value in report.system_stability.items():
        print(f"  {metric}: {value:.1f}%")
    print()
    print("🎯 Evaluation Accuracy:")
    for metric, value in report.evaluation_accuracy.items():
        print(f"  {metric}: {value:.1f}%")
    print()
    print("⚡ Development Efficiency:")
    for metric, value in report.development_efficiency.items():
        print(f"  {metric}: {value:.1f}%")
    print()
    print("💡 Recommendations:")
    for rec in report.recommendations:
        print(f"  • {rec}")
        
    # メトリクス出力
    output_file = measurement.export_metrics_to_json()
    print(f"\n📁 Detailed metrics saved to: {output_file}")


if __name__ == "__main__":
    main()