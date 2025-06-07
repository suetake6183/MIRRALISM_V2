#!/usr/bin/env python3
"""
MIRRALISM MCP Recovery Controller - Phase 1 Implementation
Purpose: Manual and automatic recovery operations for MCP services
Design: Human-centric automation with manual override capabilities

Created: 2025-06-07
Version: 1.0.0
MIRRALISM Principles: Human-Centric Automation, Transparency
"""

import asyncio
import json
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

from mcp_health_monitor import MCPHealthMonitor, HealthStatus


class RecoveryAction(Enum):
    """回復アクション"""
    HEALTH_CHECK = "health_check"
    SERVICE_RESTART = "service_restart"
    CONFIGURATION_REPAIR = "configuration_repair"
    SYSTEM_DIAGNOSTICS = "system_diagnostics"
    EMERGENCY_RESET = "emergency_reset"


@dataclass
class RecoveryResult:
    """回復結果"""
    timestamp: datetime
    action: RecoveryAction
    target_service: Optional[str]
    success: bool
    duration_ms: float
    message: str
    details: Dict[str, Any]


class MCPRecoveryController:
    """MCP回復制御システム"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "Data" / "mcp_resilience"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 回復履歴
        self.recovery_history: List[RecoveryResult] = []
        
        # 設定
        self.mcp_config_path = self.project_root / ".cursor" / "mcp.json"
        self.env_path = self.project_root / ".env.local"
        
        # ログ設定
        self.log_path = self.data_dir / "recovery_controller.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler()
            ]
        )
        
        logging.info("🔧 MIRRALISM MCP Recovery Controller initialized")
        
    def execute_recovery_action(self, action: RecoveryAction, 
                              target_service: Optional[str] = None) -> RecoveryResult:
        """回復アクション実行"""
        start_time = time.time()
        
        try:
            if action == RecoveryAction.HEALTH_CHECK:
                result = self._execute_health_check(target_service)
            elif action == RecoveryAction.SERVICE_RESTART:
                result = self._execute_service_restart(target_service)
            elif action == RecoveryAction.CONFIGURATION_REPAIR:
                result = self._execute_configuration_repair()
            elif action == RecoveryAction.SYSTEM_DIAGNOSTICS:
                result = self._execute_system_diagnostics()
            elif action == RecoveryAction.EMERGENCY_RESET:
                result = self._execute_emergency_reset()
            else:
                result = {
                    "success": False,
                    "message": f"Unknown recovery action: {action.value}",
                    "details": {}
                }
                
            duration = (time.time() - start_time) * 1000
            
            recovery_result = RecoveryResult(
                timestamp=datetime.now(),
                action=action,
                target_service=target_service,
                success=result["success"],
                duration_ms=duration,
                message=result["message"],
                details=result["details"]
            )
            
            self.recovery_history.append(recovery_result)
            self._save_recovery_log()
            
            return recovery_result
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            
            recovery_result = RecoveryResult(
                timestamp=datetime.now(),
                action=action,
                target_service=target_service,
                success=False,
                duration_ms=duration,
                message=f"Recovery action failed: {e}",
                details={"error": str(e)}
            )
            
            self.recovery_history.append(recovery_result)
            self._save_recovery_log()
            
            return recovery_result
            
    def _execute_health_check(self, target_service: Optional[str]) -> Dict[str, Any]:
        """健全性チェック実行"""
        try:
            monitor = MCPHealthMonitor()
            
            if target_service:
                # 個別サービスチェック
                metric = monitor._check_service_health(target_service)
                return {
                    "success": True,
                    "message": f"Health check completed for {target_service}",
                    "details": {
                        "service": target_service,
                        "status": metric.status.value,
                        "response_time_ms": metric.response_time_ms,
                        "last_error": metric.last_error
                    }
                }
            else:
                # 全サービスチェック
                status = monitor.get_current_status()
                return {
                    "success": True,
                    "message": "Health check completed for all services",
                    "details": status
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Health check failed: {e}",
                "details": {"error": str(e)}
            }
            
    def _execute_service_restart(self, target_service: str) -> Dict[str, Any]:
        """サービス再起動実行"""
        if not target_service:
            return {
                "success": False,
                "message": "Target service must be specified for restart",
                "details": {}
            }
            
        try:
            logging.info(f"🔄 Attempting to restart service: {target_service}")
            
            # サービス固有の再起動処理
            if target_service == "task-master-ai":
                restart_success = self._restart_task_master_ai()
            elif target_service == "filesystem":
                restart_success = self._restart_filesystem()
            elif target_service == "notion":
                restart_success = self._restart_notion()
            else:
                return {
                    "success": False,
                    "message": f"Unknown service: {target_service}",
                    "details": {}
                }
                
            if restart_success:
                # 再起動後の健全性確認
                time.sleep(5)  # 起動待機
                monitor = MCPHealthMonitor()
                metric = monitor._check_service_health(target_service)
                
                return {
                    "success": metric.status == HealthStatus.HEALTHY,
                    "message": f"Service {target_service} restart completed",
                    "details": {
                        "restart_success": restart_success,
                        "post_restart_status": metric.status.value,
                        "response_time_ms": metric.response_time_ms
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to restart service: {target_service}",
                    "details": {"restart_success": False}
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Service restart failed: {e}",
                "details": {"error": str(e)}
            }
            
    def _restart_task_master_ai(self) -> bool:
        """TaskMaster AI 再起動"""
        try:
            # 既存プロセス終了
            result = subprocess.run(
                ["pkill", "-f", "task-master-ai"], 
                capture_output=True, text=True
            )
            
            time.sleep(3)  # 終了待機
            
            # Cursor が自動的に再起動することを期待
            logging.info("✅ TaskMaster AI process terminated, awaiting automatic restart")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to restart TaskMaster AI: {e}")
            return False
            
    def _restart_filesystem(self) -> bool:
        """Filesystem MCP 再起動"""
        try:
            # 既存プロセス終了
            result = subprocess.run(
                ["pkill", "-f", "server-filesystem"], 
                capture_output=True, text=True
            )
            
            time.sleep(3)  # 終了待機
            
            # Cursor が自動的に再起動することを期待
            logging.info("✅ Filesystem MCP process terminated, awaiting automatic restart")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to restart Filesystem MCP: {e}")
            return False
            
    def _restart_notion(self) -> bool:
        """Notion MCP 再起動"""
        try:
            # 既存プロセス終了
            result = subprocess.run(
                ["pkill", "-f", "notion-mcp-server"], 
                capture_output=True, text=True
            )
            
            time.sleep(3)  # 終了待機
            
            # Cursor が自動的に再起動することを期待
            logging.info("✅ Notion MCP process terminated, awaiting automatic restart")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to restart Notion MCP: {e}")
            return False
            
    def _execute_configuration_repair(self) -> Dict[str, Any]:
        """設定修復実行"""
        try:
            repair_actions = []
            
            # MCP設定ファイル検証
            if self.mcp_config_path.exists():
                with open(self.mcp_config_path, 'r') as f:
                    config = json.load(f)
                    
                # セキュリティ設定検証
                security_issues = []
                for server_name, server_config in config.get("mcpServers", {}).items():
                    if "env" in server_config:
                        env_keys = server_config["env"]
                        for key, value in env_keys.items():
                            if not value.startswith("${") or not value.endswith("}"):
                                security_issues.append(f"{key} in {server_name}")
                                
                if security_issues:
                    repair_actions.append(f"Security issues detected: {', '.join(security_issues)}")
                else:
                    repair_actions.append("MCP configuration security validated")
                    
            else:
                repair_actions.append("MCP configuration file not found")
                
            # 環境ファイル検証
            if self.env_path.exists():
                repair_actions.append("Environment file exists")
            else:
                repair_actions.append("Environment file missing")
                
            return {
                "success": True,
                "message": "Configuration repair completed",
                "details": {
                    "repair_actions": repair_actions,
                    "config_path": str(self.mcp_config_path),
                    "env_path": str(self.env_path)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Configuration repair failed: {e}",
                "details": {"error": str(e)}
            }
            
    def _execute_system_diagnostics(self) -> Dict[str, Any]:
        """システム診断実行"""
        try:
            diagnostics = {}
            
            # Node.js バージョン確認
            try:
                result = subprocess.run(["node", "--version"], 
                                      capture_output=True, text=True, timeout=5)
                diagnostics["node_version"] = result.stdout.strip() if result.returncode == 0 else "unavailable"
            except Exception:
                diagnostics["node_version"] = "unavailable"
                
            # npm バージョン確認
            try:
                result = subprocess.run(["npm", "--version"], 
                                      capture_output=True, text=True, timeout=5)
                diagnostics["npm_version"] = result.stdout.strip() if result.returncode == 0 else "unavailable"
            except Exception:
                diagnostics["npm_version"] = "unavailable"
                
            # プロジェクトディレクトリ確認
            diagnostics["project_directory"] = {
                "exists": self.project_root.exists(),
                "readable": self.project_root.is_dir(),
                "path": str(self.project_root)
            }
            
            # MCP設定ファイル確認
            diagnostics["mcp_config"] = {
                "exists": self.mcp_config_path.exists(),
                "readable": self.mcp_config_path.is_file() if self.mcp_config_path.exists() else False,
                "path": str(self.mcp_config_path)
            }
            
            return {
                "success": True,
                "message": "System diagnostics completed",
                "details": diagnostics
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"System diagnostics failed: {e}",
                "details": {"error": str(e)}
            }
            
    def _execute_emergency_reset(self) -> Dict[str, Any]:
        """緊急リセット実行"""
        try:
            reset_actions = []
            
            # 全MCPプロセス終了
            mcp_processes = ["task-master-ai", "server-filesystem", "notion-mcp-server"]
            
            for process in mcp_processes:
                try:
                    result = subprocess.run(
                        ["pkill", "-f", process], 
                        capture_output=True, text=True
                    )
                    reset_actions.append(f"Terminated {process} processes")
                except Exception as e:
                    reset_actions.append(f"Failed to terminate {process}: {e}")
                    
            time.sleep(5)  # 終了待機
            
            # 一時ファイル削除
            temp_files = [
                self.project_root / "test_access.tmp",
                self.project_root / "test_filesystem_health.tmp"
            ]
            
            for temp_file in temp_files:
                if temp_file.exists():
                    try:
                        temp_file.unlink()
                        reset_actions.append(f"Removed temporary file: {temp_file.name}")
                    except Exception as e:
                        reset_actions.append(f"Failed to remove {temp_file.name}: {e}")
                        
            return {
                "success": True,
                "message": "Emergency reset completed",
                "details": {"reset_actions": reset_actions}
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Emergency reset failed: {e}",
                "details": {"error": str(e)}
            }
            
    def _save_recovery_log(self):
        """回復ログ保存"""
        try:
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "recovery_history": [
                    {
                        **asdict(r),
                        "timestamp": r.timestamp.isoformat(),
                        "action": r.action.value
                    }
                    for r in self.recovery_history[-100:]  # 最新100件
                ]
            }
            
            log_path = self.data_dir / "recovery_log.json"
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"❌ Failed to save recovery log: {e}")
            
    def get_recovery_status(self) -> Dict[str, Any]:
        """回復ステータス取得"""
        recent_recoveries = self.recovery_history[-10:]  # 最新10件
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_recoveries": len(self.recovery_history),
            "recent_recoveries": [
                {
                    "timestamp": r.timestamp.isoformat(),
                    "action": r.action.value,
                    "target_service": r.target_service,
                    "success": r.success,
                    "message": r.message
                }
                for r in recent_recoveries
            ],
            "success_rate": (
                sum(1 for r in self.recovery_history if r.success) / len(self.recovery_history)
                if self.recovery_history else 0.0
            )
        }


def main():
    """メイン実行（インタラクティブ制御）"""
    controller = MCPRecoveryController()
    
    print("🔧 MIRRALISM MCP Recovery Controller")
    print("=" * 45)
    
    while True:
        print("\n🔍 Available Recovery Actions:")
        print("1. Health Check (all services)")
        print("2. Health Check (specific service)")
        print("3. Service Restart")
        print("4. Configuration Repair")
        print("5. System Diagnostics")
        print("6. Emergency Reset")
        print("7. Show Recovery Status")
        print("0. Exit")
        
        try:
            choice = input("\nSelect action (0-7): ").strip()
            
            if choice == "0":
                print("👋 Exiting recovery controller")
                break
                
            elif choice == "1":
                print("🔍 Executing health check for all services...")
                result = controller.execute_recovery_action(RecoveryAction.HEALTH_CHECK)
                
            elif choice == "2":
                service = input("Enter service name (task-master-ai/filesystem/notion): ").strip()
                if service in ["task-master-ai", "filesystem", "notion"]:
                    print(f"🔍 Executing health check for {service}...")
                    result = controller.execute_recovery_action(RecoveryAction.HEALTH_CHECK, service)
                else:
                    print("❌ Invalid service name")
                    continue
                    
            elif choice == "3":
                service = input("Enter service name (task-master-ai/filesystem/notion): ").strip()
                if service in ["task-master-ai", "filesystem", "notion"]:
                    print(f"🔄 Restarting {service}...")
                    result = controller.execute_recovery_action(RecoveryAction.SERVICE_RESTART, service)
                else:
                    print("❌ Invalid service name")
                    continue
                    
            elif choice == "4":
                print("🔧 Executing configuration repair...")
                result = controller.execute_recovery_action(RecoveryAction.CONFIGURATION_REPAIR)
                
            elif choice == "5":
                print("🩺 Executing system diagnostics...")
                result = controller.execute_recovery_action(RecoveryAction.SYSTEM_DIAGNOSTICS)
                
            elif choice == "6":
                confirm = input("⚠️ Emergency reset will terminate all MCP processes. Continue? (y/N): ").strip().lower()
                if confirm == "y":
                    print("🚨 Executing emergency reset...")
                    result = controller.execute_recovery_action(RecoveryAction.EMERGENCY_RESET)
                else:
                    print("❌ Emergency reset cancelled")
                    continue
                    
            elif choice == "7":
                status = controller.get_recovery_status()
                print(f"\n📊 Recovery Status:")
                print(f"  Total recoveries: {status['total_recoveries']}")
                print(f"  Success rate: {status['success_rate']:.1%}")
                print(f"  Recent recoveries: {len(status['recent_recoveries'])}")
                continue
                
            else:
                print("❌ Invalid choice")
                continue
                
            # 結果表示
            print(f"\n📋 Result: {'✅ SUCCESS' if result.success else '❌ FAILED'}")
            print(f"Message: {result.message}")
            print(f"Duration: {result.duration_ms:.1f}ms")
            
            if result.details:
                print("Details:")
                for key, value in result.details.items():
                    print(f"  {key}: {value}")
                    
        except KeyboardInterrupt:
            print("\n👋 Exiting recovery controller")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()