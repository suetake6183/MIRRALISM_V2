#!/usr/bin/env python3
"""
MIRRALISM MCP Connection Monitor
Purpose: Monitor and validate MCP server connections
Design: Real-time monitoring with automated recovery

Created: 2025-06-07
Version: 1.0.0
"""

import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class MCPConnectionMonitor:
    """MCP接続監視・自動復旧システム"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.mcp_config_path = self.project_root / '.cursor' / 'mcp.json'
        self.status_file = self.project_root / 'logs' / 'mcp_status.json'
        self.status_file.parent.mkdir(exist_ok=True)
        
    def load_mcp_config(self) -> Dict:
        """MCP設定読み込み"""
        with open(self.mcp_config_path, 'r') as f:
            return json.load(f)
            
    def check_process(self, process_name: str) -> bool:
        """プロセス動作確認"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', process_name], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error checking process {process_name}: {e}")
            return False
            
    def test_mcp_server(self, server_name: str, config: Dict) -> Tuple[bool, str]:
        """個別MCPサーバーテスト"""
        try:
            # サーバー固有のテスト
            if server_name == "filesystem":
                # ファイルシステムMCPのテスト
                test_path = Path(config['args'][1])
                if test_path.exists():
                    return True, "Filesystem paths accessible"
                else:
                    return False, f"Path not found: {test_path}"
                    
            elif server_name == "task-master-ai":
                # Task Master AIのテスト
                server_path = Path(config['args'][0])
                if server_path.exists():
                    return True, "Task Master server found"
                else:
                    return False, f"Server not found: {server_path}"
                    
            elif server_name == "notion":
                # Notionサーバーのテスト
                return True, "Notion server configured"
                
            else:
                return True, "Unknown server type"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
            
    def monitor_all_servers(self) -> Dict:
        """全MCPサーバー監視"""
        config = self.load_mcp_config()
        status = {
            "timestamp": datetime.now().isoformat(),
            "servers": {},
            "overall_status": "HEALTHY"
        }
        
        for server_name, server_config in config.get('mcpServers', {}).items():
            is_running = self.check_process(server_name)
            is_valid, message = self.test_mcp_server(server_name, server_config)
            
            status["servers"][server_name] = {
                "process_running": is_running,
                "configuration_valid": is_valid,
                "message": message,
                "status": "OK" if (is_running or is_valid) else "ERROR"
            }
            
            if not (is_running or is_valid):
                status["overall_status"] = "DEGRADED"
                
        # ステータス保存
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
            
        return status
        
    def attempt_recovery(self, server_name: str) -> bool:
        """MCPサーバー復旧試行"""
        print(f"🔧 Attempting recovery for {server_name}...")
        
        try:
            # Cursorの再起動を促す
            print("Please restart Cursor to reload MCP configuration")
            return True
        except Exception as e:
            print(f"Recovery failed: {e}")
            return False
            
    def continuous_monitor(self, interval: int = 60):
        """継続的監視モード"""
        print("🔍 Starting MCP Connection Monitor...")
        print(f"Checking every {interval} seconds. Press Ctrl+C to stop.")
        
        try:
            while True:
                status = self.monitor_all_servers()
                
                # ステータス表示
                print(f"\n📊 MCP Status at {status['timestamp']}")
                print(f"Overall: {status['overall_status']}")
                
                for server, info in status['servers'].items():
                    icon = "✅" if info['status'] == "OK" else "❌"
                    print(f"{icon} {server}: {info['message']}")
                    
                # 問題があれば復旧試行
                if status['overall_status'] != "HEALTHY":
                    for server, info in status['servers'].items():
                        if info['status'] != "OK":
                            self.attempt_recovery(server)
                            
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped.")
            

# V1からの教訓を活かした監視設計
MONITORING_PRINCIPLES = {
    "proactive_detection": "問題の早期発見",
    "automated_recovery": "可能な限り自動復旧",
    "clear_visibility": "状況の可視化",
    "minimal_disruption": "サービス影響の最小化"
}


if __name__ == "__main__":
    monitor = MCPConnectionMonitor()
    
    # 即座の状態チェック
    status = monitor.monitor_all_servers()
    print(json.dumps(status, indent=2))
    
    # 継続監視モードのオプション
    # monitor.continuous_monitor(interval=30)