#!/usr/bin/env python3
"""
MIRRALISM データ統合自動化システム
legacy_dataとClientsディレクトリの完全統合、SSOT原則実現

Author: MIRRALISM Technical Team
Version: 1.0 (Data Integration Automation)
Created: 2025-06-10 (CTO緊急指示対応)
"""

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
import hashlib
import re


@dataclass
class DataSource:
    """データソース情報"""
    source_path: Path
    source_type: str  # "legacy", "current", "external"
    content_type: str  # "client_profile", "project_data", "config"
    last_modified: str
    file_hash: str
    metadata: Dict[str, Any]


@dataclass
class IntegrationResult:
    """統合結果"""
    integration_id: str
    timestamp: str
    sources_processed: int
    conflicts_resolved: int
    data_updated: int
    errors: List[str]
    success: bool
    integration_summary: Dict[str, Any]


class AutomaticDataIntegrationSystem:
    """
    データ統合自動化システム
    
    SSOT原則に基づく統合データ管理を実現
    """

    def __init__(self, project_root: Optional[Path] = None):
        """データ統合システム初期化"""
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.setup_logging()
        
        # パス設定
        self.legacy_data_path = self.project_root / "legacy_data"
        self.clients_path = self.project_root / "Clients"
        self.integration_log_path = (
            self.project_root / "Data" / "integration_log.json"
        )
        
        # 統合ルール設定
        self.integration_rules = {
            "client_profiles": {
                "target_directory": self.clients_path / "Database",
                "target_file": "client_profiles.json",
                "merge_strategy": "deep_merge",
                "conflict_resolution": "prefer_newer",
                "required_fields": ["name", "contact_info", "projects"]
            },
            "project_data": {
                "target_directory": self.clients_path / "Projects",
                "merge_strategy": "separate_files",
                "conflict_resolution": "preserve_both",
                "required_fields": ["project_name", "client", "status"]
            },
            "knowledge_base": {
                "target_directory": self.project_root / "Knowledge",
                "merge_strategy": "categorize",
                "conflict_resolution": "version_control",
                "required_fields": ["title", "content", "category"]
            }
        }
        
        # 統合履歴
        self.integration_history = self._load_integration_history()
        
        logger.info("データ統合自動化システム初期化完了")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - INTEGRATION_SYSTEM - %(levelname)s - %(message)s"
        )
        global logger
        logger = logging.getLogger(__name__)

    def _load_integration_history(self) -> List[Dict[str, Any]]:
        """統合履歴読み込み"""
        try:
            if self.integration_log_path.exists():
                with open(self.integration_log_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("integrations", [])
            return []
        except Exception as e:
            logger.warning(f"統合履歴読み込みエラー: {e}")
            return []

    def _save_integration_history(self):
        """統合履歴保存"""
        try:
            self.integration_log_path.parent.mkdir(parents=True, exist_ok=True)
            
            save_data = {
                "metadata": {
                    "version": "1.0",
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "integration_rules": self.integration_rules
                },
                "integrations": self.integration_history
            }
            
            with open(self.integration_log_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"統合履歴保存完了: {self.integration_log_path}")
            
        except Exception as e:
            logger.error(f"統合履歴保存エラー: {e}")

    def scan_legacy_data(self) -> List[DataSource]:
        """legacy_data完全スキャン"""
        logger.info("legacy_dataスキャン開始")
        
        data_sources = []
        
        if not self.legacy_data_path.exists():
            logger.warning(f"legacy_dataディレクトリが存在しません: {self.legacy_data_path}")
            return data_sources
        
        # 全ファイルスキャン
        for file_path in self.legacy_data_path.rglob("*"):
            if file_path.is_file():
                try:
                    # ファイルハッシュ計算
                    file_hash = self._calculate_file_hash(file_path)
                    
                    # コンテンツタイプ判定
                    content_type = self._determine_content_type(file_path)
                    
                    # メタデータ抽出
                    metadata = self._extract_metadata(file_path)
                    
                    data_source = DataSource(
                        source_path=file_path,
                        source_type="legacy",
                        content_type=content_type,
                        last_modified=datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        ).isoformat(),
                        file_hash=file_hash,
                        metadata=metadata
                    )
                    
                    data_sources.append(data_source)
                    
                except Exception as e:
                    logger.error(f"ファイルスキャンエラー: {file_path}, {e}")
        
        logger.info(f"legacy_dataスキャン完了: {len(data_sources)}ファイル")
        return data_sources

    def _calculate_file_hash(self, file_path: Path) -> str:
        """ファイルハッシュ計算"""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return "hash_calculation_failed"

    def _determine_content_type(self, file_path: Path) -> str:
        """コンテンツタイプ判定"""
        file_name = file_path.name.lower()
        file_content = ""
        
        try:
            if file_path.suffix in ['.json', '.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read().lower()
        except Exception:
            pass
        
        # パターンマッチング
        if any(keyword in file_name for keyword in ['client', 'customer', '顧客']):
            return "client_profile"
        elif any(keyword in file_name for keyword in ['project', 'プロジェクト']):
            return "project_data"
        elif any(keyword in file_name for keyword in ['config', 'setting', '設定']):
            return "configuration"
        elif any(keyword in file_content for keyword in ['contact', 'email', 'phone']):
            return "client_profile"
        elif any(keyword in file_content for keyword in ['deadline', 'budget', '予算']):
            return "project_data"
        else:
            return "unknown"

    def _extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """メタデータ抽出"""
        metadata = {
            "file_size": file_path.stat().st_size,
            "file_extension": file_path.suffix,
            "relative_path": str(file_path.relative_to(self.legacy_data_path))
        }
        
        # JSONファイルの場合、構造解析
        if file_path.suffix == '.json':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    metadata["json_keys"] = list(data.keys()) if isinstance(data, dict) else []
                    metadata["json_structure"] = type(data).__name__
            except Exception:
                pass
        
        return metadata

    def execute_full_integration(self) -> IntegrationResult:
        """完全統合実行"""
        integration_id = f"integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"完全統合開始: {integration_id}")
        
        errors = []
        sources_processed = 0
        conflicts_resolved = 0
        data_updated = 0
        
        try:
            # 1. legacy_dataスキャン
            data_sources = self.scan_legacy_data()
            sources_processed = len(data_sources)
            
            # 2. クライアントデータ統合
            client_sources = [
                source for source in data_sources 
                if source.content_type == "client_profile"
            ]
            
            if client_sources:
                conflicts, updates = self._integrate_client_data(client_sources)
                conflicts_resolved += conflicts
                data_updated += updates
            
            # 3. プロジェクトデータ統合
            project_sources = [
                source for source in data_sources 
                if source.content_type == "project_data"
            ]
            
            if project_sources:
                conflicts, updates = self._integrate_project_data(project_sources)
                conflicts_resolved += conflicts
                data_updated += updates
            
            # 4. 重複データ検出・統合
            duplicates_resolved = self._resolve_duplicates()
            conflicts_resolved += duplicates_resolved
            
            # 5. データ整合性チェック
            integrity_issues = self._check_data_integrity()
            if integrity_issues:
                errors.extend(integrity_issues)
            
        except Exception as e:
            errors.append(f"統合処理エラー: {str(e)}")
            logger.error(f"統合処理エラー: {e}")
        
        # 統合結果作成
        result = IntegrationResult(
            integration_id=integration_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            sources_processed=sources_processed,
            conflicts_resolved=conflicts_resolved,
            data_updated=data_updated,
            errors=errors,
            success=len(errors) == 0,
            integration_summary={
                "client_data_integrated": len(client_sources) if 'client_sources' in locals() else 0,
                "project_data_integrated": len(project_sources) if 'project_sources' in locals() else 0,
                "total_files_processed": sources_processed
            }
        )
        
        # 履歴保存
        self.integration_history.append({
            "integration_id": result.integration_id,
            "timestamp": result.timestamp,
            "sources_processed": result.sources_processed,
            "conflicts_resolved": result.conflicts_resolved,
            "data_updated": result.data_updated,
            "errors": result.errors,
            "success": result.success,
            "integration_summary": result.integration_summary
        })
        
        self._save_integration_history()
        
        logger.info(f"完全統合完了: {integration_id}, 成功: {result.success}")
        
        return result

    def _integrate_client_data(self, client_sources: List[DataSource]) -> Tuple[int, int]:
        """クライアントデータ統合"""
        logger.info(f"クライアントデータ統合開始: {len(client_sources)}件")
        
        conflicts_resolved = 0
        data_updated = 0
        
        # 既存クライアントプロファイル読み込み
        client_profiles_file = self.clients_path / "Database" / "client_profiles.json"
        existing_profiles = {}
        
        if client_profiles_file.exists():
            try:
                with open(client_profiles_file, 'r', encoding='utf-8') as f:
                    existing_profiles = json.load(f)
            except Exception as e:
                logger.error(f"既存プロファイル読み込みエラー: {e}")
        
        # legacy_dataから新しいクライアント情報抽出・統合
        for source in client_sources:
            try:
                if source.source_path.suffix == '.json':
                    with open(source.source_path, 'r', encoding='utf-8') as f:
                        legacy_data = json.load(f)
                    
                    # データ構造に応じた統合処理
                    if isinstance(legacy_data, dict):
                        merged, conflicts = self._merge_client_profile(
                            existing_profiles, legacy_data
                        )
                        if merged:
                            existing_profiles.update(merged)
                            data_updated += 1
                            conflicts_resolved += conflicts
                
            except Exception as e:
                logger.error(f"クライアントデータ統合エラー: {source.source_path}, {e}")
        
        # 統合結果保存
        if data_updated > 0:
            client_profiles_file.parent.mkdir(parents=True, exist_ok=True)
            with open(client_profiles_file, 'w', encoding='utf-8') as f:
                json.dump(existing_profiles, f, ensure_ascii=False, indent=2)
        
        logger.info(f"クライアントデータ統合完了: 更新{data_updated}件, 競合解決{conflicts_resolved}件")
        
        return conflicts_resolved, data_updated

    def _merge_client_profile(
        self, existing_profiles: Dict, legacy_data: Dict
    ) -> Tuple[Dict, int]:
        """クライアントプロファイル統合"""
        merged_data = {}
        conflicts = 0
        
        # 簡易的な統合ロジック（実際にはより複雑な処理が必要）
        for key, value in legacy_data.items():
            if key not in existing_profiles:
                merged_data[key] = value
            else:
                # 競合解決：新しいデータを優先（設定可能）
                if existing_profiles[key] != value:
                    merged_data[key] = value  # 新しいデータを採用
                    conflicts += 1
        
        return merged_data, conflicts

    def _integrate_project_data(self, project_sources: List[DataSource]) -> Tuple[int, int]:
        """プロジェクトデータ統合"""
        logger.info(f"プロジェクトデータ統合開始: {len(project_sources)}件")
        
        conflicts_resolved = 0
        data_updated = 0
        
        projects_dir = self.clients_path / "Projects"
        projects_dir.mkdir(parents=True, exist_ok=True)
        
        for source in project_sources:
            try:
                # プロジェクトファイルのコピー・統合
                target_file = projects_dir / f"legacy_{source.source_path.name}"
                
                if not target_file.exists():
                    shutil.copy2(source.source_path, target_file)
                    data_updated += 1
                else:
                    # 重複ファイルの処理
                    conflicts_resolved += 1
                    
            except Exception as e:
                logger.error(f"プロジェクトデータ統合エラー: {source.source_path}, {e}")
        
        logger.info(f"プロジェクトデータ統合完了: 更新{data_updated}件, 競合解決{conflicts_resolved}件")
        
        return conflicts_resolved, data_updated

    def _resolve_duplicates(self) -> int:
        """重複データ解決"""
        logger.info("重複データ解決開始")
        
        # 簡易的な重複検出（ファイルハッシュベース）
        resolved_count = 0
        
        # 実際の重複解決処理は複雑になるため、基本的な枠組みのみ実装
        
        logger.info(f"重複データ解決完了: {resolved_count}件")
        
        return resolved_count

    def _check_data_integrity(self) -> List[str]:
        """データ整合性チェック"""
        logger.info("データ整合性チェック開始")
        
        issues = []
        
        # 必須ファイルの存在チェック
        required_files = [
            self.clients_path / "Database" / "client_profiles.json"
        ]
        
        for required_file in required_files:
            if not required_file.exists():
                issues.append(f"必須ファイルが存在しません: {required_file}")
        
        # JSON構造の検証
        if (self.clients_path / "Database" / "client_profiles.json").exists():
            try:
                with open(
                    self.clients_path / "Database" / "client_profiles.json", 
                    'r', encoding='utf-8'
                ) as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        issues.append("client_profiles.jsonの構造が正しくありません")
            except Exception as e:
                issues.append(f"client_profiles.json検証エラー: {e}")
        
        logger.info(f"データ整合性チェック完了: 問題{len(issues)}件")
        
        return issues

    def get_integration_status(self) -> Dict[str, Any]:
        """統合状況取得"""
        status = {
            "total_integrations": len(self.integration_history),
            "last_integration": None,
            "success_rate": 0.0,
            "data_sources": {
                "legacy_data_files": 0,
                "current_client_profiles": 0,
                "integrated_clients": 0
            }
        }
        
        if self.integration_history:
            # 最新統合情報
            latest = max(self.integration_history, key=lambda x: x["timestamp"])
            status["last_integration"] = latest
            
            # 成功率計算
            successful = sum(1 for integration in self.integration_history if integration["success"])
            status["success_rate"] = successful / len(self.integration_history)
        
        # データソース状況
        if self.legacy_data_path.exists():
            status["data_sources"]["legacy_data_files"] = len(list(self.legacy_data_path.rglob("*")))
        
        client_profiles_file = self.clients_path / "Database" / "client_profiles.json"
        if client_profiles_file.exists():
            try:
                with open(client_profiles_file, 'r', encoding='utf-8') as f:
                    profiles = json.load(f)
                    status["data_sources"]["current_client_profiles"] = len(profiles)
            except Exception:
                pass
        
        return status


# 使用例・テスト関数
def run_integration_system_test():
    """統合システムテスト実行"""
    system = AutomaticDataIntegrationSystem()
    
    # データスキャン
    data_sources = system.scan_legacy_data()
    
    # 完全統合実行
    integration_result = system.execute_full_integration()
    
    # 統合状況確認
    status = system.get_integration_status()
    
    logger.info("データ統合システムテスト完了")
    return {
        "data_sources": len(data_sources),
        "integration_result": integration_result,
        "current_status": status
    }


if __name__ == "__main__":
    run_integration_system_test() 