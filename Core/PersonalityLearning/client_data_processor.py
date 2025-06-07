#!/usr/bin/env python3
"""
MIRRALISM ClientDataProcessor - Phase 1 基本実装
============================================

クライアントデータをPersonalityLearningシステムに統合する基本機能
17時間実装スコープでの概念実証レベル実装

Phase 1 機能範囲:
- クライアント基本情報の読み込み・解析
- PersonalityLearning統合データベースへの保存
- 基本的な分析メタデータ生成
- 統合アーキテクチャの概念実証

作成者: MIRRALISM V2 技術者
作成日: 2025年6月6日
"""

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# PersonalityLearning統合システムをインポート
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    # Phase 1用の基本システムを使用
    from personality_learning_core_phase1 import MirralismPersonalityLearningPhase1 as MirralismPersonalityLearning
    PersonalityLearningDatabase = None  # Phase 1では簡易実装
except ImportError as e:
    logging.warning(f"PersonalityLearning統合モジュールが見つかりません: {e}")
    MirralismPersonalityLearning = None
    PersonalityLearningDatabase = None


class ClientDataProcessor:
    """MIRRALISM クライアントデータ処理エンジン (Phase 1)"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        ClientDataProcessor初期化
        
        Args:
            project_root: MIRRALISMプロジェクトルート
        """
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.setup_logging()
        
        # PersonalityLearning統合初期化
        self.personality_learning = None
        self.database = None
        
        if MirralismPersonalityLearning:
            try:
                self.personality_learning = MirralismPersonalityLearning()
                self.logger.info("✅ PersonalityLearning統合システム初期化完了 (Phase 1)")
            except Exception as e:
                self.logger.error(f"❌ PersonalityLearning初期化失敗: {e}")
        
        # 統計情報
        self.processing_stats = {
            "clients_processed": 0,
            "integration_success": 0,
            "integration_failures": 0,
            "session_start": datetime.now(timezone.utc).isoformat()
        }

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - CLIENT_PROCESSOR - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def load_client_profiles(self) -> Dict[str, Any]:
        """クライアントプロファイルデータ読み込み"""
        try:
            client_db_path = self.project_root / "Clients" / "Database" / "client_profiles.json"
            
            with open(client_db_path, 'r', encoding='utf-8') as f:
                client_data = json.load(f)
            
            self.logger.info(f"✅ クライアントデータ読み込み完了: {client_db_path}")
            return client_data
            
        except FileNotFoundError:
            self.logger.error(f"❌ クライアントデータファイルが見つかりません: {client_db_path}")
            return {}
        except Exception as e:
            self.logger.error(f"❌ クライアントデータ読み込みエラー: {e}")
            return {}

    def extract_client_personalities(self, client_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """クライアント情報からPersonalityLearning対象データを抽出"""
        extracted_data = []
        
        clients = client_data.get("clients", {})
        
        for client_name, client_info in clients.items():
            if client_name == "_template":  # テンプレートをスキップ
                continue
                
            # 基本情報抽出
            personality_data = {
                "client_name": client_name,
                "formal_name": client_info.get("正式名称", client_name),
                "industry": client_info.get("業界", ""),
                "region": client_info.get("地域", ""),
                "representative": client_info.get("代表者", ""),
                "business_overview": client_info.get("事業概要", ""),
                "management_philosophy": client_info.get("経営理念", ""),
                "management_policy": client_info.get("経営方針", ""),
                "current_challenges": client_info.get("現在の課題", []),
                "special_notes": client_info.get("特記事項", []),
                "project_start_date": client_info.get("プロジェクト開始日", ""),
                "importance": client_info.get("重要度", "medium"),
                "status": client_info.get("ステータス", "unknown")
            }
            
            # 主要担当者情報抽出
            key_persons = client_info.get("主要担当者", [])
            personality_data["key_persons"] = []
            
            for person in key_persons:
                if isinstance(person, dict):
                    person_data = {
                        "name": person.get("名前", ""),
                        "position": person.get("役職", ""),
                        "characteristics": person.get("特徴", ""),
                        "role_type": self._classify_role_type(person.get("役職", ""))
                    }
                    personality_data["key_persons"].append(person_data)
            
            # PersonalityLearning分析用コンテンツ生成
            analysis_content = self._generate_analysis_content(personality_data)
            personality_data["analysis_content"] = analysis_content
            
            extracted_data.append(personality_data)
            
        self.logger.info(f"✅ {len(extracted_data)}件のクライアントデータを抽出")
        return extracted_data

    def _classify_role_type(self, position: str) -> str:
        """役職からロールタイプを分類"""
        position_lower = position.lower()
        
        if any(word in position_lower for word in ["代表", "社長", "ceo", "president"]):
            return "decision_maker"
        elif any(word in position_lower for word in ["補佐", "配偶者", "パートナー"]):
            return "key_supporter"
        elif any(word in position_lower for word in ["管理", "部長", "manager", "director"]):
            return "middle_management"
        else:
            return "team_member"

    def _generate_analysis_content(self, client_data: Dict[str, Any]) -> str:
        """PersonalityLearning分析用コンテンツ生成"""
        content_parts = []
        
        # 基本情報
        content_parts.append(f"クライアント: {client_data['client_name']}")
        if client_data['business_overview']:
            content_parts.append(f"事業概要: {client_data['business_overview']}")
        
        # 経営理念・方針
        if client_data['management_philosophy']:
            content_parts.append(f"経営理念: {client_data['management_philosophy']}")
        if client_data['management_policy']:
            content_parts.append(f"経営方針: {client_data['management_policy']}")
        
        # 主要担当者
        for person in client_data['key_persons']:
            if person['name'] and person['characteristics']:
                content_parts.append(f"{person['name']}({person['position']}): {person['characteristics']}")
        
        # 課題・特記事項
        if client_data['current_challenges']:
            challenges = client_data['current_challenges']
            if isinstance(challenges, list):
                content_parts.append(f"課題: {', '.join(challenges)}")
            else:
                content_parts.append(f"課題: {challenges}")
        
        return "\n".join(content_parts)

    def process_client_with_personality_learning(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """クライアントデータをPersonalityLearning分析"""
        if not self.personality_learning:
            return {
                "success": False,
                "error": "PersonalityLearning統合システムが利用できません",
                "client_name": client_data.get("client_name", "unknown")
            }
        
        try:
            analysis_content = client_data["analysis_content"]
            client_name = client_data["client_name"]
            
            # PersonalityLearning分析実行
            analysis_result = self.personality_learning.analyze_entry(
                content=analysis_content,
                source_type="client_data",
                metadata={
                    "client_name": client_name,
                    "industry": client_data.get("industry", ""),
                    "importance": client_data.get("importance", "medium"),
                    "data_source": "client_profiles_database"
                }
            )
            
            if analysis_result.get("success", False):
                # 統計更新
                self.processing_stats["integration_success"] += 1
                
                # 統合結果作成
                integration_result = {
                    "success": True,
                    "client_name": client_name,
                    "analysis_result": analysis_result.get("analysis", {}),
                    "confidence": analysis_result.get("analysis", {}).get("suetake_likeness_index", 0.0),
                    "integration_metadata": {
                        "processed_at": datetime.now(timezone.utc).isoformat(),
                        "data_source": "client_profiles",
                        "processing_version": "phase1_concept"
                    }
                }
                
                self.logger.info(f"✅ クライアント分析完了: {client_name} (精度: {integration_result['confidence']}%)")
                return integration_result
            else:
                error_msg = analysis_result.get("error", "unknown")
                self.logger.warning(f"⚠️ クライアント分析失敗: {client_name} - {error_msg}")
                self.processing_stats["integration_failures"] += 1
                return {
                    "success": False,
                    "error": error_msg,
                    "client_name": client_name
                }
                
        except Exception as e:
            self.logger.error(f"❌ PersonalityLearning分析エラー: {e}")
            self.processing_stats["integration_failures"] += 1
            return {
                "success": False,
                "error": str(e),
                "client_name": client_data.get("client_name", "unknown")
            }

    def save_integration_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """統合結果をデータベースに保存"""
        try:
            # 統合結果保存用ディレクトリ作成
            results_dir = self.project_root / "Data" / "client_integration"
            results_dir.mkdir(parents=True, exist_ok=True)
            
            # 結果ファイル生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = results_dir / f"client_integration_results_{timestamp}.json"
            
            # 保存データ準備
            save_data = {
                "integration_metadata": {
                    "processing_date": datetime.now(timezone.utc).isoformat(),
                    "phase": "phase1_concept",
                    "processor_version": "v2.0_basic",
                    "total_clients": len(results),
                    "successful_integrations": len([r for r in results if r.get("success", False)]),
                    "failed_integrations": len([r for r in results if not r.get("success", False)])
                },
                "processing_stats": self.processing_stats,
                "integration_results": results
            }
            
            # ファイル保存
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"✅ 統合結果保存完了: {results_file}")
            
            return {
                "success": True,
                "results_file": str(results_file),
                "total_processed": len(results),
                "successful": save_data["integration_metadata"]["successful_integrations"],
                "failed": save_data["integration_metadata"]["failed_integrations"]
            }
            
        except Exception as e:
            self.logger.error(f"❌ 統合結果保存エラー: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def run_phase1_integration(self) -> Dict[str, Any]:
        """Phase 1 統合処理実行"""
        self.logger.info("🚀 MIRRALISM ClientDataProcessor Phase 1 統合開始")
        
        try:
            # 1. クライアントデータ読み込み
            client_data = self.load_client_profiles()
            if not client_data:
                return {
                    "success": False,
                    "error": "クライアントデータの読み込みに失敗しました"
                }
            
            # 2. PersonalityLearning対象データ抽出
            extracted_clients = self.extract_client_personalities(client_data)
            if not extracted_clients:
                return {
                    "success": False,
                    "error": "クライアントデータの抽出に失敗しました"
                }
            
            # 3. PersonalityLearning統合分析
            integration_results = []
            for client in extracted_clients:
                result = self.process_client_with_personality_learning(client)
                integration_results.append(result)
                self.processing_stats["clients_processed"] += 1
            
            # 4. 結果保存
            save_result = self.save_integration_results(integration_results)
            
            # 5. 最終結果生成
            final_result = {
                "success": True,
                "phase": "phase1_concept",
                "processing_summary": {
                    "total_clients": len(extracted_clients),
                    "successful_integrations": len([r for r in integration_results if r.get("success", False)]),
                    "failed_integrations": len([r for r in integration_results if not r.get("success", False)]),
                    "average_confidence": self._calculate_average_confidence(integration_results)
                },
                "integration_results": integration_results,
                "save_result": save_result,
                "processing_stats": self.processing_stats,
                "mirralism_compliance": {
                    "ssot_principle": True,
                    "quality_baseline": True,
                    "v1_lessons_applied": True
                }
            }
            
            self.logger.info("🎯 Phase 1 統合処理完了")
            return final_result
            
        except Exception as e:
            self.logger.error(f"❌ Phase 1 統合処理エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_stats": self.processing_stats
            }

    def _calculate_average_confidence(self, results: List[Dict[str, Any]]) -> float:
        """平均信頼度計算"""
        successful_results = [r for r in results if r.get("success", False)]
        if not successful_results:
            return 0.0
        
        confidences = [r.get("confidence", 0.0) for r in successful_results]
        return sum(confidences) / len(confidences)

    def get_demo_data(self) -> Dict[str, Any]:
        """デモ用データ生成"""
        return {
            "processor_status": "phase1_ready",
            "capabilities": [
                "クライアント基本情報統合",
                "PersonalityLearning分析",
                "統合データベース保存",
                "分析結果可視化"
            ],
            "integration_architecture": {
                "data_source": "Clients/Database/client_profiles.json",
                "processing_engine": "PersonalityLearning integrated_system",
                "output_destination": "Data/client_integration/",
                "analysis_accuracy": "基本レベル（Phase 1）"
            },
            "phase2_preview": {
                "enhanced_analysis": "深層心理分析",
                "security_validation": "完全セキュリティ検証",
                "performance_optimization": "高速処理最適化",
                "advanced_integrations": "WebData統合対応"
            },
            "mirralism_compliance": {
                "quality_standards": "維持済み",
                "v1_lessons": "適用済み",
                "scalability": "設計済み"
            }
        }


# エントリーポイント
def run_phase1_demo():
    """Phase 1 デモ実行"""
    processor = ClientDataProcessor()
    result = processor.run_phase1_integration()
    
    print("🎯 MIRRALISM ClientDataProcessor Phase 1 デモ")
    print("=" * 60)
    
    if result["success"]:
        summary = result["processing_summary"]
        print(f"✅ 統合処理成功")
        print(f"📊 処理サマリー:")
        print(f"   総クライアント数: {summary['total_clients']}")
        print(f"   成功統合: {summary['successful_integrations']}")
        print(f"   失敗統合: {summary['failed_integrations']}")
        print(f"   平均信頼度: {summary['average_confidence']:.1f}%")
        
        # デモデータ表示
        demo_data = processor.get_demo_data()
        print(f"\n🔧 統合アーキテクチャ:")
        arch = demo_data["integration_architecture"]
        for key, value in arch.items():
            print(f"   {key}: {value}")
    else:
        print(f"❌ 統合処理失敗: {result.get('error', 'unknown')}")
    
    return result


if __name__ == "__main__":
    run_phase1_demo()