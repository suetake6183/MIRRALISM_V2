#!/usr/bin/env python3
"""
MIRRALISM MCP Health Monitor - Phase 1 Implementation
Purpose: Real-time MCP service health monitoring with immediate retry mechanisms
Design: Self-healing architecture with 4-layer resilience system

Created: 2025-06-07
Version: 1.0.0
MIRRALISM Principles: Constraint-First Design, Preventive Quality Assurance
"""

import asyncio
import json
import time
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import psutil


class HealthStatus(Enum):
    """健全性ステータス"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


class RetryStrategy(Enum):
    """リトライ戦略"""
    IMMEDIATE = "immediate"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    CIRCUIT_BREAKER = "circuit_breaker"


@dataclass
class HealthMetric:
    """健全性メトリクス"""
    timestamp: datetime
    service_name: str
    status: HealthStatus
    response_time_ms: float
    success_rate: float
    error_count: int
    last_error: Optional[str]


@dataclass
class RetryAttempt:
    """リトライ試行記録"""
    timestamp: datetime
    service_name: str
    strategy: RetryStrategy
    attempt_number: int
    success: bool
    response_time_ms: float
    error_message: Optional[str]


class MCPHealthMonitor:
    """MCP健全性監視システム"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "Data" / "mcp_resilience"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 健全性データ
        self.health_metrics: List[HealthMetric] = []
        self.retry_attempts: List[RetryAttempt] = []
        self.current_status: Dict[str, HealthStatus] = {}
        
        # 監視設定
        self.monitoring_interval = 30  # seconds
        self.health_check_timeout = 5  # seconds
        self.max_immediate_retries = 3
        self.exponential_base_delay = 1.0  # seconds
        self.max_exponential_delay = 30.0  # seconds
        
        # しきい値設定
        self.response_time_threshold = 2000  # ms
        self.success_rate_threshold = 0.95
        self.error_frequency_threshold = 5  # per hour
        
        # 監視対象サービス
        self.monitored_services = [
            "task-master-ai",
            "filesystem", 
            "notion"
        ]
        
        # 監視スレッド制御
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # ログ設定
        self.log_path = self.data_dir / "health_monitor.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler()
            ]
        )
        
        logging.info("🔍 MIRRALISM MCP Health Monitor initialized")
        
    def start_monitoring(self) -> bool:
        """健全性監視開始"""
        if self.monitoring_active:
            logging.warning("⚠️ Health monitoring already active")
            return False
            
        try:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True
            )
            self.monitoring_thread.start()
            
            logging.info("✅ Health monitoring started")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to start health monitoring: {e}")
            self.monitoring_active = False
            return False
            
    def stop_monitoring(self) -> bool:
        """健全性監視停止"""
        if not self.monitoring_active:
            logging.warning("⚠️ Health monitoring not active")
            return False
            
        try:
            self.monitoring_active = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=10)
                
            logging.info("🛑 Health monitoring stopped")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to stop health monitoring: {e}")
            return False
            
    def _monitoring_loop(self):
        """監視ループ（バックグラウンド実行）"""
        while self.monitoring_active:
            try:
                # 全サービスの健全性チェック
                for service in self.monitored_services:
                    metric = self._check_service_health(service)
                    self.health_metrics.append(metric)
                    self.current_status[service] = metric.status
                    
                    # 不健全な場合は即座にリトライ
                    if metric.status in [HealthStatus.UNHEALTHY, HealthStatus.CRITICAL]:
                        self._execute_immediate_retry(service, metric)
                        
                # 定期レポート保存
                self._save_health_report()
                
                # 次の監視まで待機
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logging.error(f"❌ Error in monitoring loop: {e}")
                time.sleep(5)  # エラー時は短縮間隔で再試行
                
    def _check_service_health(self, service_name: str) -> HealthMetric:
        """サービス健全性チェック"""
        start_time = time.time()
        
        try:
            if service_name == "task-master-ai":
                success, error = self._check_task_master_ai()
            elif service_name == "filesystem":
                success, error = self._check_filesystem()
            elif service_name == "notion":
                success, error = self._check_notion()
            else:
                success, error = False, f"Unknown service: {service_name}"
                
            response_time = (time.time() - start_time) * 1000
            
            # ステータス判定
            if success and response_time < self.response_time_threshold:
                status = HealthStatus.HEALTHY
            elif success and response_time < self.response_time_threshold * 2:
                status = HealthStatus.DEGRADED
            elif success:
                status = HealthStatus.UNHEALTHY
            else:
                status = HealthStatus.CRITICAL
                
            # 成功率計算（過去1時間のデータから）
            success_rate = self._calculate_success_rate(service_name)
            
            # エラー数計算（過去1時間）
            error_count = self._calculate_error_count(service_name)
            
            return HealthMetric(
                timestamp=datetime.now(),
                service_name=service_name,
                status=status,
                response_time_ms=response_time,
                success_rate=success_rate,
                error_count=error_count,
                last_error=error if not success else None
            )
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            return HealthMetric(
                timestamp=datetime.now(),
                service_name=service_name,
                status=HealthStatus.CRITICAL,
                response_time_ms=response_time,
                success_rate=0.0,
                error_count=1,
                last_error=str(e)
            )
            
    def _check_task_master_ai(self) -> tuple[bool, Optional[str]]:
        """TaskMaster AI健全性チェック"""
        try:
            # プロセス存在確認
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if (proc.info['name'] == 'node' and 
                        any('task-master-ai' in cmd for cmd in proc.info['cmdline'])):
                        return True, None
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return False, "TaskMaster AI process not found"
            
        except Exception as e:
            return False, f"TaskMaster AI check failed: {e}"
            
    def _check_filesystem(self) -> tuple[bool, Optional[str]]:
        """Filesystem MCP健全性チェック"""
        try:
            # プロセス存在確認
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if (proc.info['name'] == 'node' and 
                        any('server-filesystem' in cmd for cmd in proc.info['cmdline'])):
                        
                        # ファイルアクセステスト
                        test_path = self.project_root / "test_filesystem_health.tmp"
                        test_path.write_text("health_check")
                        test_path.unlink()
                        return True, None
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return False, "Filesystem MCP process not found"
            
        except Exception as e:
            return False, f"Filesystem check failed: {e}"
            
    def _check_notion(self) -> tuple[bool, Optional[str]]:
        """Notion MCP健全性チェック"""
        try:
            # プロセス存在確認
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if (proc.info['name'] == 'node' and 
                        any('notion-mcp-server' in cmd for cmd in proc.info['cmdline'])):
                        return True, None
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return False, "Notion MCP process not found"
            
        except Exception as e:
            return False, f"Notion check failed: {e}"
            
    def _calculate_success_rate(self, service_name: str) -> float:
        """過去1時間の成功率計算"""
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_metrics = [
            m for m in self.health_metrics
            if m.service_name == service_name and m.timestamp > one_hour_ago
        ]
        
        if not recent_metrics:
            return 1.0
            
        successful = sum(1 for m in recent_metrics if m.status == HealthStatus.HEALTHY)
        return successful / len(recent_metrics)
        
    def _calculate_error_count(self, service_name: str) -> int:
        """過去1時間のエラー数計算"""
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_metrics = [
            m for m in self.health_metrics
            if (m.service_name == service_name and 
                m.timestamp > one_hour_ago and 
                m.status in [HealthStatus.UNHEALTHY, HealthStatus.CRITICAL])
        ]
        
        return len(recent_metrics)
        
    def _execute_immediate_retry(self, service_name: str, failed_metric: HealthMetric):
        """即座リトライ実行"""
        logging.warning(f"⚠️ Service {service_name} unhealthy, executing immediate retry")
        
        for attempt in range(1, self.max_immediate_retries + 1):
            start_time = time.time()
            
            try:
                # サービス再起動試行
                restart_success = self._restart_service(service_name)
                
                # 短時間待機後に健全性再確認
                time.sleep(2)
                
                # 健全性再チェック
                new_metric = self._check_service_health(service_name)
                
                response_time = (time.time() - start_time) * 1000
                success = new_metric.status == HealthStatus.HEALTHY
                
                # リトライ記録
                retry_record = RetryAttempt(
                    timestamp=datetime.now(),
                    service_name=service_name,
                    strategy=RetryStrategy.IMMEDIATE,
                    attempt_number=attempt,
                    success=success,
                    response_time_ms=response_time,
                    error_message=None if success else new_metric.last_error
                )
                
                self.retry_attempts.append(retry_record)
                
                if success:
                    logging.info(f"✅ Service {service_name} recovered after {attempt} attempts")
                    return True
                    
                logging.warning(f"⚠️ Retry attempt {attempt} failed for {service_name}")
                
            except Exception as e:
                logging.error(f"❌ Retry attempt {attempt} error for {service_name}: {e}")
                
        logging.error(f"❌ All immediate retries failed for {service_name}")
        return False
        
    def _restart_service(self, service_name: str) -> bool:
        """サービス再起動"""
        try:
            if service_name == "task-master-ai":
                # TaskMaster AI 再起動
                subprocess.run(["pkill", "-f", "task-master-ai"], check=False)
                time.sleep(2)
                # 自動的にCursorが再起動する
                return True
                
            elif service_name == "filesystem":
                # Filesystem MCP 再起動
                subprocess.run(["pkill", "-f", "server-filesystem"], check=False)
                time.sleep(2)
                # 自動的にCursorが再起動する
                return True
                
            elif service_name == "notion":
                # Notion MCP 再起動
                subprocess.run(["pkill", "-f", "notion-mcp-server"], check=False)
                time.sleep(2)
                # 自動的にCursorが再起動する
                return True
                
            return False
            
        except Exception as e:
            logging.error(f"❌ Service restart failed for {service_name}: {e}")
            return False
            
    def _save_health_report(self):
        """健全性レポート保存"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "current_status": {k: v.value for k, v in self.current_status.items()},
                "recent_metrics": [
                    {
                        **asdict(m),
                        "timestamp": m.timestamp.isoformat(),
                        "status": m.status.value
                    }
                    for m in self.health_metrics[-100:]  # 最新100件
                ],
                "recent_retries": [
                    {
                        **asdict(r),
                        "timestamp": r.timestamp.isoformat(),
                        "strategy": r.strategy.value
                    }
                    for r in self.retry_attempts[-50:]  # 最新50件
                ]
            }
            
            report_path = self.data_dir / "current_health_status.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"❌ Failed to save health report: {e}")
            
    def get_current_status(self) -> Dict[str, Any]:
        """現在の健全性ステータス取得"""
        return {
            "timestamp": datetime.now().isoformat(),
            "monitoring_active": self.monitoring_active,
            "services": {
                service: {
                    "status": self.current_status.get(service, HealthStatus.UNHEALTHY).value,
                    "last_check": self._get_last_check_time(service)
                }
                for service in self.monitored_services
            },
            "overall_health": self._calculate_overall_health(),
            "metrics_count": len(self.health_metrics),
            "retry_count": len(self.retry_attempts)
        }
        
    def _get_last_check_time(self, service_name: str) -> Optional[str]:
        """最後のチェック時刻取得"""
        recent_metrics = [
            m for m in self.health_metrics
            if m.service_name == service_name
        ]
        
        if recent_metrics:
            return recent_metrics[-1].timestamp.isoformat()
        return None
        
    def _calculate_overall_health(self) -> str:
        """全体的健全性計算"""
        if not self.current_status:
            return "unknown"
            
        status_counts = {}
        for status in self.current_status.values():
            status_counts[status] = status_counts.get(status, 0) + 1
            
        total_services = len(self.current_status)
        
        if status_counts.get(HealthStatus.CRITICAL, 0) > 0:
            return "critical"
        elif status_counts.get(HealthStatus.UNHEALTHY, 0) > total_services * 0.5:
            return "unhealthy"
        elif status_counts.get(HealthStatus.DEGRADED, 0) > 0:
            return "degraded"
        else:
            return "healthy"


def main():
    """メイン実行"""
    monitor = MCPHealthMonitor()
    
    print("🔍 MIRRALISM MCP Health Monitor")
    print("=" * 40)
    
    # 健全性監視開始
    if monitor.start_monitoring():
        print("✅ Health monitoring started successfully")
        
        try:
            # 初期ステータス表示
            time.sleep(5)  # 初回チェック待機
            status = monitor.get_current_status()
            
            print(f"\n📊 Current Status: {status['overall_health'].upper()}")
            for service, info in status['services'].items():
                print(f"  • {service}: {info['status'].upper()}")
                
            print(f"\n📈 Monitoring active. Logs: {monitor.log_path}")
            print("Press Ctrl+C to stop monitoring...")
            
            # 継続監視（Ctrl+Cで停止）
            while True:
                time.sleep(30)
                current_status = monitor.get_current_status()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Overall Health: {current_status['overall_health'].upper()}")
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping health monitoring...")
            monitor.stop_monitoring()
            print("✅ Health monitoring stopped")
            
    else:
        print("❌ Failed to start health monitoring")


if __name__ == "__main__":
    main()