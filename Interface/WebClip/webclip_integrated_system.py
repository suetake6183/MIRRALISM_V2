#!/usr/bin/env python3
"""
WebClip統合システム
==================

MIRRALISM V2 WebClip独立システム統合版
目的: 動機分析 + リアルタイム対話 + YAML処理の完全統合

作成者: 技術責任者
作成日: 2025年6月6日  
設計思想: Option B 分離最適化 + CTOリアルタイム体験最適化
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .motivation_analyzer import WebClipMotivationAnalyzer
from .realtime_dialogue import WebClipRealtimeDialogue  
from .yaml_processor import YAMLFrontmatterProcessor


class WebClipIntegratedSystem:
    """WebClip統合システム（Option B 完全版）"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        統合システム初期化
        
        Args:
            project_root: MIRRALISMプロジェクトルート
        """
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.setup_logging()
        
        # コンポーネント初期化
        self.motivation_analyzer = WebClipMotivationAnalyzer(project_root)
        self.dialogue_system = WebClipRealtimeDialogue(project_root)
        self.yaml_processor = YAMLFrontmatterProcessor(project_root)
        
        # 統合処理統計
        self.integration_stats = {
            "total_clips_processed": 0,
            "successful_integrations": 0,
            "average_processing_time": 0.0,
            "target_achievement_rate": 0.0,
            "v1_errors_prevented": 0
        }
        
        # パフォーマンス履歴
        self.performance_history = []
        
        self.logger.info("✅ WebClip統合システム初期化完了")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - WEBCLIP_INTEGRATED - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    async def process_webclip_complete(
        self,
        article_url: str,
        article_title: str,
        article_content: str,
        user_context: Optional[Dict] = None,
        save_to_file: bool = True
    ) -> Dict[str, Any]:
        """
        WebClip完全処理（統合システム）
        
        CTOの要求: 
        - <2秒以内での即座洞察
        - "あなたはこういうことに興味を持ったんですね"
        - "なぜこの記事をクリップしたのか？"
        - V1 25%エラー率の完全解決
        
        Args:
            article_url: 記事URL
            article_title: 記事タイトル  
            article_content: 記事内容
            user_context: ユーザーコンテキスト
            save_to_file: ファイル保存フラグ
            
        Returns:
            統合処理結果
        """
        start_time = time.time()
        processing_id = self._generate_processing_id()
        
        try:
            self.logger.info(f"🚀 WebClip統合処理開始 [{processing_id}]: {article_title[:50]}...")
            
            # Phase 1: 並列処理準備
            tasks = []
            
            # 1. リアルタイム対話処理（最優先）
            dialogue_task = asyncio.create_task(
                self._async_dialogue_processing(
                    article_content, article_url, article_title, user_context
                )
            )
            tasks.append(("dialogue", dialogue_task))
            
            # 2. YAML処理（並列実行）
            yaml_task = asyncio.create_task(
                self._async_yaml_processing(
                    article_title, article_url, article_content, user_context
                )
            )
            tasks.append(("yaml", yaml_task))
            
            # Phase 2: 並列実行
            phase2_start = time.time()
            completed_tasks = {}
            
            for task_name, task in tasks:
                try:
                    result = await task
                    completed_tasks[task_name] = {"success": True, "result": result}
                except Exception as e:
                    completed_tasks[task_name] = {"success": False, "error": str(e)}
                    self.logger.error(f"❌ {task_name}タスクエラー: {e}")
            
            phase2_time = time.time() - phase2_start
            
            # Phase 3: 結果統合
            integration_start = time.time()
            
            # 必須結果の確認
            if not completed_tasks.get("dialogue", {}).get("success"):
                raise Exception("リアルタイム対話処理が失敗しました")
            
            dialogue_result = completed_tasks["dialogue"]["result"]
            yaml_result = completed_tasks.get("yaml", {}).get("result", {})
            
            # 統合結果構築
            integrated_result = self._build_integrated_result(
                dialogue_result, yaml_result, user_context, processing_id
            )
            
            integration_time = time.time() - integration_start
            
            # Phase 4: ファイル保存（オプション）
            save_result = None
            if save_to_file:
                save_start = time.time()
                save_result = await self._save_webclip_file(integrated_result)
                save_time = time.time() - save_start
            else:
                save_time = 0.0
            
            # Phase 5: パフォーマンス記録
            total_time = time.time() - start_time
            performance = {
                "processing_id": processing_id,
                "total_time": total_time,
                "phase_times": {
                    "parallel_processing": phase2_time,
                    "integration": integration_time,
                    "file_save": save_time
                },
                "target_achieved": total_time < 2.0,
                "components_success": {
                    "dialogue": completed_tasks.get("dialogue", {}).get("success", False),
                    "yaml": completed_tasks.get("yaml", {}).get("success", False)
                }
            }
            
            self._record_integration_performance(performance)
            
            # 統計更新
            self.integration_stats["total_clips_processed"] += 1
            if all(performance["components_success"].values()):
                self.integration_stats["successful_integrations"] += 1
            
            self._update_integration_stats(performance)
            
            final_result = {
                "success": True,
                "processing_id": processing_id,
                "instant_display": integrated_result["instant_display"],
                "full_analysis": integrated_result,
                "performance": performance,
                "save_result": save_result,
                "integration_stats": self.integration_stats.copy()
            }
            
            self.logger.info(
                f"✅ WebClip統合処理完了 [{processing_id}] ({total_time:.2f}s) - "
                f"目標達成: {'○' if total_time < 2.0 else '×'}"
            )
            
            return final_result
            
        except Exception as e:
            error_time = time.time() - start_time
            self.logger.error(f"❌ WebClip統合処理エラー [{processing_id}] ({error_time:.2f}s): {e}")
            
            # エラー時でも基本的な応答
            return {
                "success": False,
                "processing_id": processing_id,
                "error": str(e),
                "instant_display": self._create_error_display(article_title, str(e)),
                "performance": {
                    "total_time": error_time,
                    "target_achieved": False,
                    "error": True
                }
            }

    async def _async_dialogue_processing(
        self, 
        article_content: str, 
        article_url: str, 
        article_title: str, 
        user_context: Optional[Dict]
    ) -> Dict[str, Any]:
        """非同期対話処理"""
        
        # リアルタイム対話システムの呼び出し
        dialogue_result = self.dialogue_system.process_webclip_realtime(
            article_content, article_url, article_title, user_context
        )
        
        return dialogue_result

    async def _async_yaml_processing(
        self,
        article_title: str,
        article_url: str, 
        article_content: str,
        user_context: Optional[Dict]
    ) -> Dict[str, Any]:
        """非同期YAML処理"""
        
        # YAML処理システムの呼び出し
        yaml_result = self.yaml_processor.process_webclip_frontmatter(
            article_title, article_url, article_content, 
            clip_metadata={"processed_at": datetime.now(timezone.utc).isoformat()},
            user_context=user_context
        )
        
        return yaml_result

    def _build_integrated_result(
        self,
        dialogue_result: Dict,
        yaml_result: Dict,
        user_context: Optional[Dict],
        processing_id: str
    ) -> Dict[str, Any]:
        """統合結果構築"""
        
        # 対話結果から即座表示データ取得
        instant_display = dialogue_result.get("instant_display", {})
        
        # YAML結果から構造化データ取得
        frontmatter = yaml_result.get("frontmatter", {})
        markdown_content = yaml_result.get("markdown_file", "")
        
        # V1エラー防止情報
        v1_prevention = yaml_result.get("v1_comparison", {})
        
        # 統合分析結果
        full_analysis = dialogue_result.get("full_analysis", {})
        
        integrated = {
            "processing_id": processing_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            
            # CTOの即座表示用（最重要）
            "instant_display": {
                **instant_display,
                "processing_id": processing_id,
                "yaml_valid": yaml_result.get("success", False),
                "v1_errors_prevented": len(v1_prevention.get("prevented_errors", []))
            },
            
            # 完全分析結果
            "analysis": full_analysis,
            
            # 構造化データ
            "structured_data": {
                "frontmatter": frontmatter,
                "markdown": markdown_content,
                "yaml_processing": yaml_result
            },
            
            # V1改善情報
            "v1_improvements": {
                "errors_prevented": v1_prevention.get("prevented_errors", []),
                "prevention_rate": v1_prevention.get("prevention_rate", 0.0),
                "yaml_validation": yaml_result.get("validation", {})
            },
            
            # メタデータ
            "metadata": {
                "user_context": user_context,
                "system_version": "v2.0_integrated",
                "components": ["motivation_analyzer", "dialogue_system", "yaml_processor"]
            }
        }
        
        return integrated

    async def _save_webclip_file(self, integrated_result: Dict) -> Dict[str, Any]:
        """WebClipファイル保存"""
        
        try:
            # 保存先ディレクトリ
            save_dir = self.project_root / "Data" / "webclips"
            save_dir.mkdir(parents=True, exist_ok=True)
            
            # ファイル名生成
            processing_id = integrated_result["processing_id"]
            article_title = integrated_result["instant_display"].get("article_summary", {}).get("title", "untitled")
            safe_title = "".join(c for c in article_title if c.isalnum() or c in " -_")[:50]
            
            filename = f"{processing_id}_{safe_title}.md"
            file_path = save_dir / filename
            
            # マークダウンファイル保存
            markdown_content = integrated_result["structured_data"].get("markdown", "")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # JSON保存（詳細分析結果）
            json_filename = f"{processing_id}_analysis.json"
            json_path = save_dir / json_filename
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(integrated_result, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "markdown_file": str(file_path),
                "analysis_file": str(json_path),
                "file_size": file_path.stat().st_size if file_path.exists() else 0
            }
            
        except Exception as e:
            self.logger.error(f"❌ ファイル保存エラー: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _create_error_display(self, title: str, error: str) -> Dict[str, Any]:
        """エラー時表示データ作成"""
        
        return {
            "primary_message": "クリップ処理中にエラーが発生しました",
            "question": "記事の内容について教えていただけますか？",
            "suggestion": "手動でクリップ内容を整理することをお勧めします",
            "article_summary": {
                "title": title,
                "estimated_read_time": "不明",
                "complexity": "分析中",
                "actionability": "分析中"
            },
            "interest_metrics": {
                "novelty": "分析中",
                "frequency": 0,
                "themes": []
            },
            "motivation_confidence": "分析中",
            "empathy_note": f"エラーが発生しましたが、記録は保持されます",
            "error_info": error,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _generate_processing_id(self) -> str:
        """処理ID生成"""
        
        timestamp = datetime.now()
        return f"webclip_{timestamp.strftime('%Y%m%d_%H%M%S')}_{timestamp.microsecond}"

    def _record_integration_performance(self, performance: Dict):
        """統合パフォーマンス記録"""
        
        performance["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.performance_history.append(performance)
        
        # 最新100件を保持
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]

    def _update_integration_stats(self, performance: Dict):
        """統合統計更新"""
        
        recent_performances = self.performance_history[-20:]  # 最新20件
        
        if recent_performances:
            total_times = [p["total_time"] for p in recent_performances]
            success_count = sum(1 for p in recent_performances if p["target_achieved"])
            
            self.integration_stats["average_processing_time"] = sum(total_times) / len(total_times)
            self.integration_stats["target_achievement_rate"] = success_count / len(recent_performances)

    def get_system_status(self) -> Dict[str, Any]:
        """システム状態取得"""
        
        # 各コンポーネントの状態
        motivation_stats = self.motivation_analyzer.processing_stats if hasattr(self.motivation_analyzer, 'processing_stats') else {}
        dialogue_performance = self.dialogue_system.get_performance_summary()
        yaml_stats = self.yaml_processor.get_processing_statistics()
        
        return {
            "system_info": {
                "version": "v2.0_integrated",
                "components": 3,
                "uptime": "active",
                "last_update": datetime.now(timezone.utc).isoformat()
            },
            "integration_stats": self.integration_stats,
            "component_stats": {
                "motivation_analyzer": motivation_stats,
                "dialogue_system": dialogue_performance,
                "yaml_processor": yaml_stats
            },
            "recent_performance": {
                "total_processes": len(self.performance_history),
                "recent_average_time": self.integration_stats["average_processing_time"],
                "target_achievement_rate": self.integration_stats["target_achievement_rate"]
            },
            "v1_improvements": {
                "total_errors_prevented": self.integration_stats["v1_errors_prevented"],
                "error_prevention_active": True,
                "yaml_processing": "standard_library"
            }
        }

    async def run_integration_test(self) -> Dict[str, Any]:
        """統合テスト実行"""
        
        test_articles = [
            {
                "title": "Advanced AI Personality Learning Systems Implementation Guide",
                "url": "https://example.com/ai-personality-learning",
                "content": """
                AI-driven personality learning systems are revolutionizing personal development and self-understanding. 
                This comprehensive guide explores how to implement advanced machine learning algorithms for personality analysis, 
                behavioral pattern recognition, and personalized insight generation.
                
                Key topics covered:
                - Machine learning models for personality analysis
                - Real-time processing optimization 
                - User experience design for personal insights
                - Integration with existing systems
                """,
                "user_context": {"user_type": "CTO", "current_focus": "MIRRALISM development"}
            },
            {
                "title": "Leadership Strategies for Technical Teams",
                "url": "https://example.com/tech-leadership",
                "content": """
                Effective leadership in technology teams requires balancing technical expertise with human understanding.
                This article outlines proven strategies for managing technical teams, fostering innovation, 
                and maintaining high performance while supporting team member growth.
                
                Strategies include:
                - Technical decision-making frameworks
                - Team communication optimization
                - Performance management approaches
                - Conflict resolution in technical contexts
                """,
                "user_context": {"user_type": "CTO", "current_focus": "team management"}
            }
        ]
        
        test_results = []
        
        self.logger.info("🧪 WebClip統合システム テスト開始")
        
        for i, article in enumerate(test_articles, 1):
            self.logger.info(f"📝 テストケース {i}: {article['title']}")
            
            result = await self.process_webclip_complete(
                article["url"],
                article["title"], 
                article["content"],
                article["user_context"],
                save_to_file=False  # テスト時はファイル保存なし
            )
            
            test_results.append({
                "test_case": i,
                "title": article["title"],
                "success": result["success"],
                "performance": result.get("performance", {}),
                "instant_display": result.get("instant_display", {}),
                "error": result.get("error")
            })
        
        # テスト結果サマリー
        successful_tests = sum(1 for r in test_results if r["success"])
        avg_time = sum(r["performance"].get("total_time", 0) for r in test_results) / len(test_results)
        target_achieved = sum(1 for r in test_results if r["performance"].get("target_achieved", False))
        
        test_summary = {
            "total_tests": len(test_results),
            "successful_tests": successful_tests,
            "success_rate": successful_tests / len(test_results),
            "average_processing_time": avg_time,
            "target_achievement_rate": target_achieved / len(test_results),
            "all_tests_passed": successful_tests == len(test_results),
            "performance_target_met": avg_time < 2.0,
            "detailed_results": test_results
        }
        
        self.logger.info(
            f"✅ 統合テスト完了 - 成功率: {test_summary['success_rate']:.0%}, "
            f"平均時間: {avg_time:.2f}s, 目標達成率: {test_summary['target_achievement_rate']:.0%}"
        )
        
        return test_summary


if __name__ == "__main__":
    async def main():
        # 統合システムテスト実行
        integrated_system = WebClipIntegratedSystem()
        
        print("🚀 WebClip統合システム 初期化・テスト")
        print("=" * 60)
        
        # システム状態確認
        status = integrated_system.get_system_status()
        print(f"システムバージョン: {status['system_info']['version']}")
        print(f"コンポーネント数: {status['system_info']['components']}")
        
        # 統合テスト実行
        test_results = await integrated_system.run_integration_test()
        
        print(f"\n📊 統合テスト結果")
        print(f"成功率: {test_results['success_rate']:.0%}")
        print(f"平均処理時間: {test_results['average_processing_time']:.2f}s")
        print(f"目標達成率: {test_results['target_achievement_rate']:.0%}")
        print(f"性能目標達成: {'✅' if test_results['performance_target_met'] else '❌'}")
        
        # 各テストケースの詳細
        for result in test_results["detailed_results"]:
            perf = result["performance"]
            print(f"\nテスト {result['test_case']}: {result['title'][:50]}...")
            print(f"  成功: {'✅' if result['success'] else '❌'}")
            print(f"  時間: {perf.get('total_time', 0):.2f}s ({'✅' if perf.get('target_achieved', False) else '❌'} <2s)")
            
            if result["success"] and "instant_display" in result:
                display = result["instant_display"]
                print(f"  洞察: {display.get('primary_message', '')[:60]}...")
                print(f"  質問: {display.get('question', '')[:60]}...")
    
    # 非同期テスト実行
    asyncio.run(main())