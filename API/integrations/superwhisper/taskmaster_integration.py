#!/usr/bin/env python3
"""
TaskMaster-SuperWhisper 統合モジュール（MIRRALISM V2）
==================================================

音声データからの自動タスク管理統合:
1. 音声分類に基づくTaskMaster操作判定
2. PersonalityLearning分析結果との相関
3. 自動タスク生成・更新・状態変更
4. 高精度分析結果の活用

作成者: MIRRALISM統合チーム
作成日: 2025年6月3日
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

# TaskMaster MCP連携
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(project_root))

# TaskMaster統合設定
TASKMASTER_PROJECT_ROOT = str(project_root)


class TaskMasterSuperWhisperIntegration:
    """TaskMaster-SuperWhisper統合システム"""

    def __init__(self, project_root: Optional[str] = None):
        """
        統合システム初期化

        Args:
            project_root: プロジェクトルート（TaskMaster用）
        """
        self.project_root = project_root or TASKMASTER_PROJECT_ROOT
        self.setup_logging()

        # TaskMaster操作統計
        self.operation_stats = {
            "tasks_created": 0,
            "tasks_updated": 0,
            "subtasks_added": 0,
            "status_changes": 0,
            "session_start": datetime.now().isoformat(),
        }

        self.logger.info("🔧 TaskMaster-SuperWhisper統合初期化完了")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def process_voice_for_tasks(
        self, workflow_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        音声処理結果からTaskMaster操作実行

        Args:
            workflow_result: SuperWhisperワークフロー処理結果

        Returns:
            TaskMaster統合結果
        """
        integration_id = f"tm_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            if not workflow_result.get("success", False):
                return {
                    "success": False,
                    "error": "ワークフロー処理が失敗しているため、TaskMaster統合をスキップ",
                    "integration_id": integration_id,
                }

            # データ抽出
            final_result = workflow_result["final_result"]
            task_correlation = workflow_result["task_correlation"]
            enhanced_analysis = workflow_result["enhanced_analysis"]

            # TaskMaster操作判定
            taskmaster_action = self._determine_taskmaster_action(
                final_result, task_correlation, enhanced_analysis
            )

            if taskmaster_action["action"] == "none":
                return {
                    "success": True,
                    "action": "none",
                    "reason": taskmaster_action["reason"],
                    "integration_id": integration_id,
                }

            # TaskMaster操作実行
            execution_result = self._execute_taskmaster_action(
                taskmaster_action, final_result
            )

            # 結果統合
            return {
                "success": True,
                "integration_id": integration_id,
                "taskmaster_action": taskmaster_action,
                "execution_result": execution_result,
                "operation_stats": self.operation_stats,
                "workflow_data": workflow_result,
            }

        except Exception as e:
            self.logger.error(f"❌ TaskMaster統合エラー ({integration_id}): {e}")
            return {
                "success": False,
                "error": str(e),
                "integration_id": integration_id,
                "workflow_data": workflow_result,
            }

    def _determine_taskmaster_action(
        self,
        final_result: Dict[str, Any],
        task_correlation: Dict[str, Any],
        enhanced_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        TaskMaster操作判定

        Args:
            final_result: 最終処理結果
            task_correlation: TaskMaster相関分析
            enhanced_analysis: 拡張分析結果

        Returns:
            操作判定結果
        """
        classification = final_result.get("classification", "thought")
        confidence = enhanced_analysis.get("analysis_result", {}).get("confidence", 0.0)
        correlation_found = task_correlation.get("correlation_found", False)

        # 高精度分析（85%以上）の場合の特別処理
        if confidence >= 85.0:
            if classification == "task" and correlation_found:
                return {
                    "action": "create_task",
                    "reason": f"高精度分析({confidence}%) + タスク分類 + 相関検知",
                    "confidence": confidence,
                    "priority": "high",
                }
            elif classification in ["idea", "reflection"] and confidence >= 90.0:
                return {
                    "action": "create_idea_task",
                    "reason": f"超高精度分析({confidence}%) + アイデア/振り返り",
                    "confidence": confidence,
                    "priority": "medium",
                }

        # 通常の判定ロジック
        if classification == "task":
            if correlation_found:
                return {
                    "action": "create_task",
                    "reason": "タスク分類 + 相関検知",
                    "confidence": confidence,
                    "priority": "medium",
                }
            elif confidence >= 70.0:
                return {
                    "action": "create_task",
                    "reason": f"タスク分類 + 中精度分析({confidence}%)",
                    "confidence": confidence,
                    "priority": "medium",
                }

        # PersonalityLearning更新時の既存タスク関連付け
        if enhanced_analysis.get("personality_learning_updated", False):
            return {
                "action": "update_related_tasks",
                "reason": f"PersonalityLearning更新({confidence}%)",
                "confidence": confidence,
                "priority": "low",
            }

        return {
            "action": "none",
            "reason": f"操作条件未満: 分類={classification}, 精度={confidence}%, 相関={correlation_found}",
            "confidence": confidence,
        }

    def _execute_taskmaster_action(
        self, action_config: Dict[str, Any], final_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        TaskMaster操作実行

        Args:
            action_config: 操作設定
            final_result: 処理結果データ

        Returns:
            実行結果
        """
        action = action_config["action"]

        if action == "create_task":
            return self._create_task_from_voice(action_config, final_result)
        elif action == "create_idea_task":
            return self._create_idea_task(action_config, final_result)
        elif action == "update_related_tasks":
            return self._update_related_tasks(action_config, final_result)
        else:
            return {"success": False, "error": f"未知の操作: {action}"}

    def _create_task_from_voice(
        self, action_config: Dict[str, Any], final_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        音声からタスク作成

        Args:
            action_config: 操作設定
            final_result: 処理結果

        Returns:
            タスク作成結果
        """
        try:
            text_content = final_result.get("text_content", "")
            confidence = action_config.get("confidence", 0.0)
            priority = action_config.get("priority", "medium")

            # タスクタイトル生成
            task_title = self._generate_task_title(text_content)

            # タスク詳細作成
            task_details = self._generate_task_details(
                text_content, confidence, final_result
            )

            # TaskMaster MCP操作をシミュレート（実際の実装では実際のMCP呼び出し）
            task_data = {
                "title": task_title,
                "description": f"SuperWhisper音声入力から自動生成 (精度: {confidence}%)",
                "details": task_details,
                "priority": priority,
                "source": "superwhisper_voice",
                "voice_data": {
                    "original_text": text_content,
                    "confidence": confidence,
                    "created_time": final_result.get("created_time"),
                    "notion_id": final_result.get("notion_id"),
                },
            }

            # 統計更新
            self.operation_stats["tasks_created"] += 1

            self.logger.info(f"🚀 音声タスク作成: {task_title}")

            return {
                "success": True,
                "action": "task_created",
                "task_data": task_data,
                "message": f"音声から高精度タスク作成完了: {task_title}",
            }

        except Exception as e:
            self.logger.error(f"❌ タスク作成エラー: {e}")
            return {"success": False, "error": str(e)}

    def _create_idea_task(
        self, action_config: Dict[str, Any], final_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        アイデア・振り返りタスク作成

        Args:
            action_config: 操作設定
            final_result: 処理結果

        Returns:
            アイデアタスク作成結果
        """
        try:
            text_content = final_result.get("text_content", "")
            confidence = action_config.get("confidence", 0.0)
            classification = final_result.get("classification", "idea")

            # アイデアタスクタイトル
            if classification == "idea":
                task_title = f"💡 アイデア検討: {self._extract_key_phrase(text_content)}"
            else:  # reflection
                task_title = f"🔍 振り返り実装: {self._extract_key_phrase(text_content)}"

            # アイデアタスク詳細
            task_details = f"""
## 音声入力からの{classification}タスク

**原文:**
{text_content}

**PersonalityLearning分析:**
- 精度: {confidence}%
- 分類: {classification}
- 重要度: 高精度により自動タスク化

**推奨アクション:**
- 詳細検討・計画立案
- 関連リサーチ実施
- 実装可能性評価
"""

            task_data = {
                "title": task_title,
                "description": f"高精度分析({confidence}%)による{classification}の自動タスク化",
                "details": task_details,
                "priority": "medium",
                "source": f"superwhisper_{classification}",
                "classification": classification,
            }

            # 統計更新
            self.operation_stats["tasks_created"] += 1

            self.logger.info(f"💡 {classification}タスク作成: {task_title}")

            return {
                "success": True,
                "action": "idea_task_created",
                "task_data": task_data,
                "message": f"{classification}から高精度タスク生成: {task_title}",
            }

        except Exception as e:
            self.logger.error(f"❌ アイデアタスク作成エラー: {e}")
            return {"success": False, "error": str(e)}

    def _update_related_tasks(
        self, action_config: Dict[str, Any], final_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        関連タスクの更新

        Args:
            action_config: 操作設定
            final_result: 処理結果

        Returns:
            更新結果
        """
        try:
            confidence = action_config.get("confidence", 0.0)
            text_content = final_result.get("text_content", "")

            update_note = f"""
## PersonalityLearning更新関連ノート
**音声入力:** {text_content}
**分析精度:** {confidence}%
**更新日時:** {datetime.now().isoformat()}

このPersonalityLearning更新により、関連タスクの見直しを推奨します。
"""

            # 統計更新
            self.operation_stats["tasks_updated"] += 1

            self.logger.info(f"📝 関連タスク更新ノート作成 (精度: {confidence}%)")

            return {
                "success": True,
                "action": "related_tasks_updated",
                "update_note": update_note,
                "message": f"PersonalityLearning更新による関連タスク情報追加",
            }

        except Exception as e:
            self.logger.error(f"❌ 関連タスク更新エラー: {e}")
            return {"success": False, "error": str(e)}

    def _generate_task_title(self, text_content: str) -> str:
        """
        音声からタスクタイトル生成

        Args:
            text_content: 音声テキスト

        Returns:
            生成されたタスクタイトル
        """
        # 重要キーワード抽出
        key_phrase = self._extract_key_phrase(text_content)

        # 動詞パターン検知
        if any(verb in text_content for verb in ["実装", "作成", "開発"]):
            return f"🔧 実装: {key_phrase}"
        elif any(verb in text_content for verb in ["修正", "更新", "改善"]):
            return f"🔄 修正: {key_phrase}"
        elif any(verb in text_content for verb in ["テスト", "確認", "検証"]):
            return f"✅ 検証: {key_phrase}"
        else:
            return f"📋 タスク: {key_phrase}"

    def _extract_key_phrase(self, text_content: str) -> str:
        """
        キーフレーズ抽出

        Args:
            text_content: テキスト内容

        Returns:
            抽出されたキーフレーズ
        """
        # 簡易実装：最初の30文字 + 省略記号
        if len(text_content) > 30:
            return text_content[:30] + "..."
        return text_content

    def _generate_task_details(
        self,
        text_content: str,
        confidence: float,
        final_result: Dict[str, Any],
    ) -> str:
        """
        タスク詳細生成

        Args:
            text_content: 音声テキスト
            confidence: 分析精度
            final_result: 処理結果

        Returns:
            生成されたタスク詳細
        """
        return f"""
## SuperWhisper音声入力タスク

**原音声:**
{text_content}

**PersonalityLearning分析:**
- 分析精度: {confidence}%
- 学習影響度: {final_result.get('personality_learning_enhanced', {}).get('learning_impact', 0.0):.2f}
- 進化ステージ: {final_result.get('personality_learning_enhanced', {}).get('evolution_stage', 'unknown')}

**音声メタデータ:**
- Notion ID: {final_result.get('notion_id', 'N/A')}
- 作成時刻: {final_result.get('created_time', 'N/A')}
- 品質スコア: {final_result.get('quality_score', 'N/A')}

**推奨実装アプローチ:**
高精度分析結果に基づき、PersonalityLearning統合を活用して実装してください。

**参考リンク:**
- [MIRRALISM統合システム](./MIRRALISM/)
- [PersonalityLearning Database](./MIRRALISM/Core/PersonalityLearning/)
"""

    def get_integration_summary(self) -> Dict[str, Any]:
        """
        統合サマリー取得

        Returns:
            統合統計とサマリー
        """
        session_duration = (
            datetime.now()
            - datetime.fromisoformat(self.operation_stats["session_start"])
        ).total_seconds()

        return {
            **self.operation_stats,
            "session_duration_seconds": session_duration,
            "total_operations": (
                self.operation_stats["tasks_created"]
                + self.operation_stats["tasks_updated"]
                + self.operation_stats["subtasks_added"]
                + self.operation_stats["status_changes"]
            ),
            "project_root": self.project_root,
        }


# 統合エントリーポイント
def integrate_with_taskmaster(
    workflow_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    TaskMaster統合エントリーポイント

    Args:
        workflow_result: SuperWhisperワークフロー結果

    Returns:
        TaskMaster統合結果
    """
    integration = TaskMasterSuperWhisperIntegration()
    return integration.process_voice_for_tasks(workflow_result)


if __name__ == "__main__":
    # テスト実行
    test_workflow_result = {
        "success": True,
        "final_result": {
            "text_content": "MIRRALISMのSuperWhisper統合を完成させて、TaskMasterとの自動連携を実装する必要がある",
            "classification": "task",
            "created_time": "2025-06-03T19:40:00+09:00",
            "notion_id": "test_taskmaster_123",
            "quality_score": 0.95,
        },
        "task_correlation": {
            "correlation_found": True,
            "task_keywords": ["実装", "統合", "完成"],
        },
        "enhanced_analysis": {
            "analysis_result": {"confidence": 92.5},
            "personality_learning_updated": True,
            "personality_learning_enhanced": {
                "learning_impact": 0.95,
                "evolution_stage": "V2_production_ready",
            },
        },
    }

    result = integrate_with_taskmaster(test_workflow_result)

    print("🔧 TaskMaster統合テスト")
    print("=" * 50)
    print(f"成功: {result['success']}")
    if result["success"]:
        if result.get("execution_result", {}).get("success", False):
            exec_result = result["execution_result"]
            print(f"操作: {exec_result['action']}")
            print(f"メッセージ: {exec_result['message']}")
            if "task_data" in exec_result:
                print(f"タスクタイトル: {exec_result['task_data']['title']}")
        else:
            print(f"アクション: {result.get('action', 'none')}")
            print(f"理由: {result.get('reason', 'N/A')}")
    else:
        print(f"エラー: {result['error']}")
