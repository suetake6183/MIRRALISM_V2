#!/usr/bin/env python3
"""
MIRRALISM Security Framework
Purpose: Centralized security management and API key protection
Design: Security-by-Design with V1 lessons learned

Created: 2025-06-07
Version: 1.0.0
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv


class MIRRALISMSecurityFramework:
    """統合セキュリティ管理システム"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.env_file = self.project_root / '.env.local'
        self.security_log = self.project_root / 'logs' / 'security_audit.log'
        
        # ログ設定
        self.security_log.parent.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=str(self.security_log),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # 環境変数ロード
        self._load_secure_environment()
        
    def _load_secure_environment(self):
        """セキュアな環境変数ロード"""
        if not self.env_file.exists():
            logging.error("🚨 .env.local not found - security breach risk!")
            raise SecurityError(".env.local file is required for secure operation")
            
        load_dotenv(self.env_file)
        logging.info("✅ Secure environment loaded successfully")
        
    def get_api_key(self, service: str) -> Optional[str]:
        """APIキーの安全な取得"""
        key_name = f"{service.upper()}_API_KEY"
        api_key = os.getenv(key_name)
        
        if api_key:
            # APIキーの一部をマスクしてログ記録
            masked_key = f"{api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "***"
            logging.info(f"API key retrieved for {service}: {masked_key}")
        else:
            logging.warning(f"API key not found for {service}")
            
        return api_key
        
    def security_audit(self) -> Dict[str, Any]:
        """セキュリティ監査実行"""
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # 1. 環境ファイル存在確認
        audit_results["checks"]["env_file_exists"] = self.env_file.exists()
        
        # 2. gitignore確認
        gitignore = self.project_root / '.gitignore'
        if gitignore.exists():
            with open(gitignore, 'r') as f:
                content = f.read()
                audit_results["checks"]["env_in_gitignore"] = '.env.local' in content
        else:
            audit_results["checks"]["env_in_gitignore"] = False
            
        # 3. MCP設定確認
        mcp_config = self.project_root / '.cursor' / 'mcp.json'
        if mcp_config.exists():
            with open(mcp_config, 'r') as f:
                config_content = f.read()
                # APIキーパターンの検出
                has_exposed_keys = any(
                    pattern in config_content 
                    for pattern in ['sk-ant-', 'sk-proj-', 'key-', 'token-']
                )
                audit_results["checks"]["mcp_no_exposed_keys"] = not has_exposed_keys
        
        # 4. 環境変数設定確認
        required_vars = ['ANTHROPIC_API_KEY', 'MIRRALISM_PROJECT_ROOT']
        for var in required_vars:
            audit_results["checks"][f"env_{var.lower()}"] = bool(os.getenv(var))
            
        # 総合判定
        all_passed = all(audit_results["checks"].values())
        audit_results["security_status"] = "SECURE" if all_passed else "VULNERABLE"
        
        # ログ記録
        logging.info(f"Security audit completed: {audit_results['security_status']}")
        
        return audit_results
        
    def protect_sensitive_file(self, file_path: Path) -> bool:
        """機密ファイルの保護設定"""
        try:
            # ファイル権限を600に設定（所有者のみ読み書き可能）
            os.chmod(file_path, 0o600)
            logging.info(f"Protected file: {file_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to protect file {file_path}: {e}")
            return False
            
    def generate_secure_mcp_config(self) -> Dict[str, Any]:
        """セキュアなMCP設定生成"""
        return {
            "_security": "MIRRALISM Secure Configuration",
            "_notice": "API keys loaded from environment at runtime",
            "mcpServers": {
                "task-master-ai": {
                    "command": "node",
                    "args": [os.getenv("MCP_TASK_MASTER_PATH", 
                            "/usr/local/lib/node_modules/task-master-ai/mcp-server/server.js")],
                    "env": {
                        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
                        "_secure": "true"
                    }
                },
                "filesystem": {
                    "command": "npx",
                    "args": [
                        "@modelcontextprotocol/server-filesystem",
                        *os.getenv("MCP_FILESYSTEM_PATHS", "").split(',')
                    ]
                }
            }
        }
        

class SecurityError(Exception):
    """セキュリティ関連エラー"""
    pass


# V1からの教訓を反映した設計原則
SECURITY_PRINCIPLES = {
    "never_expose_keys": "APIキーは絶対に設定ファイルに直接記載しない",
    "environment_only": "機密情報は環境変数からのみ読み込む",
    "audit_trail": "全てのセキュリティ操作をログに記録",
    "fail_secure": "セキュリティ問題がある場合は動作を停止",
    "defense_in_depth": "多層防御による保護"
}


if __name__ == "__main__":
    # セキュリティフレームワーク初期化
    security = MIRRALISMSecurityFramework()
    
    # セキュリティ監査実行
    audit_results = security.security_audit()
    print(json.dumps(audit_results, indent=2))
    
    # 環境ファイル保護
    security.protect_sensitive_file(security.env_file)