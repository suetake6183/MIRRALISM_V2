#!/usr/bin/env python3
"""
WebClipリアルタイム対話システム
===============================

MIRRALISM V2 WebClip独立システム
目的: クリップ時の即座対話・洞察提供

作成者: 技術責任者  
作成日: 2025年6月6日
設計思想: Option B 分離最適化アプローチ + CTOリアルタイム体験最適化
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .motivation_analyzer import WebClipMotivationAnalyzer


class WebClipRealtimeDialogue:
    """WebClipリアルタイム対話システム"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        リアルタイム対話システム初期化
        
        Args:
            project_root: MIRRALISMプロジェクトルート
        """
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.setup_logging()
        
        # 動機分析エンジン
        self.motivation_analyzer = WebClipMotivationAnalyzer(project_root)
        
        # 対話履歴
        self.dialogue_history = self._load_dialogue_history()
        
        # パフォーマンス測定
        self.performance_metrics = []
        
        self.logger.info("✅ WebClipリアルタイム対話システム初期化完了")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - WEBCLIP_DIALOGUE - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def process_webclip_realtime(
        self,
        article_content: str,
        article_url: str, 
        article_title: str,
        user_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        WebClipリアルタイム処理
        
        CTOの要求: <2秒以内での即座洞察提供
        
        Args:
            article_content: 記事内容
            article_url: 記事URL  
            article_title: 記事タイトル
            user_context: ユーザーコンテキスト
            
        Returns:
            リアルタイム対話結果
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"🚀 WebClipリアルタイム処理開始: {article_title[:50]}...")
            
            # 1. 動機分析（高速化）
            analysis_start = time.time()
            motivation_result = self.motivation_analyzer.analyze_clip_motivation(
                article_content, article_url, article_title, user_context
            )
            analysis_time = time.time() - analysis_start
            
            if not motivation_result["success"]:
                raise Exception(f"動機分析失敗: {motivation_result.get('error')}")
            
            analysis = motivation_result["analysis"]
            
            # 2. リアルタイム対話生成
            dialogue_start = time.time()
            realtime_dialogue = self._generate_realtime_dialogue(analysis)
            dialogue_time = time.time() - dialogue_start
            
            # 3. 即座表示用データ構築
            display_start = time.time()
            instant_display = self._create_instant_display(analysis, realtime_dialogue)
            display_time = time.time() - display_start
            
            # 4. パフォーマンス記録
            total_time = time.time() - start_time
            performance = {
                "total_time": total_time,
                "analysis_time": analysis_time,
                "dialogue_time": dialogue_time,
                "display_time": display_time,
                "target_achieved": total_time < 2.0
            }
            
            self._record_performance(performance)
            
            # 5. 対話履歴更新
            self._update_dialogue_history(analysis, realtime_dialogue, performance)
            
            result = {
                "success": True,
                "instant_display": instant_display,
                "full_analysis": analysis,
                "performance": performance,
                "dialogue_id": self._generate_dialogue_id()
            }
            
            self.logger.info(
                f"✅ WebClipリアルタイム処理完了 ({total_time:.2f}s) - "
                f"目標達成: {'○' if total_time < 2.0 else '×'}"
            )
            
            return result
            
        except Exception as e:
            error_time = time.time() - start_time
            self.logger.error(f"❌ WebClipリアルタイム処理エラー ({error_time:.2f}s): {e}")
            
            # エラー時でも基本的な応答を返す
            return {
                "success": False,
                "error": str(e),
                "instant_display": self._create_fallback_display(article_title),
                "performance": {"total_time": error_time, "target_achieved": False}
            }

    def _generate_realtime_dialogue(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """リアルタイム対話生成"""
        
        dialogue = analysis.get("dialogue", {})
        motivation = analysis.get("motivation_estimation", {})
        
        # 1. 即座洞察（第一印象）
        instant_insight = dialogue.get("interest_insight", "この記事に興味を持たれたんですね")
        
        # 2. 重要動機質問（1つに絞る）
        primary_question = self._select_primary_question(dialogue.get("motivation_questions", []))
        
        # 3. 簡潔な活用提案（最重要1つ）
        key_suggestion = self._select_key_suggestion(analysis.get("utilization_suggestions", []))
        
        # 4. フォローアップ（必要に応じて）
        follow_up = self._generate_contextual_follow_up(analysis)
        
        # 5. 感情的共感要素
        empathy_message = self._generate_empathy_message(analysis)
        
        return {
            "instant_insight": instant_insight,
            "primary_question": primary_question,
            "key_suggestion": key_suggestion,
            "follow_up": follow_up,
            "empathy_message": empathy_message,
            "dialogue_tone": self._determine_dialogue_tone(analysis),
            "confidence_level": analysis.get("confidence_score", 0.5)
        }

    def _create_instant_display(self, analysis: Dict, dialogue: Dict) -> Dict[str, Any]:
        """即座表示用データ作成"""
        
        article_info = analysis.get("article_info", {})
        
        # CTOが即座に見る情報
        instant_display = {
            "primary_message": dialogue["instant_insight"],
            "question": dialogue["primary_question"],
            "suggestion": dialogue["key_suggestion"]["suggestion"] if dialogue["key_suggestion"] else "",
            "article_summary": {
                "title": article_info.get("title", ""),
                "estimated_read_time": self._estimate_read_time(article_info.get("content_length", 0)),
                "complexity": self._get_complexity_label(analysis.get("content_analysis", {}).get("complexity_level", 0)),
                "actionability": self._get_actionability_label(analysis.get("content_analysis", {}).get("actionability", 0))
            },
            "interest_metrics": {
                "novelty": self._get_novelty_label(analysis.get("interest_analysis", {}).get("novelty_score", 0)),
                "frequency": analysis.get("interest_analysis", {}).get("theme_frequency", {}).get("max_frequency", 0),
                "themes": analysis.get("interest_analysis", {}).get("current_themes", [])[:3]  # 最大3つ
            },
            "motivation_confidence": f"{dialogue['confidence_level']:.0%}",
            "empathy_note": dialogue.get("empathy_message", ""),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return instant_display

    def _create_fallback_display(self, article_title: str) -> Dict[str, Any]:
        """エラー時フォールバック表示"""
        
        return {
            "primary_message": "この記事に興味を持たれたんですね",
            "question": "どのような点に魅力を感じられましたか？",
            "suggestion": "後でじっくり読み返すことをお勧めします",
            "article_summary": {
                "title": article_title,
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
            "empathy_note": "クリップありがとうございます",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _select_primary_question(self, questions: List[str]) -> str:
        """主要質問選択"""
        
        if not questions:
            return "この記事をクリップされた理由を教えてください"
        
        # 最も具体的で答えやすい質問を選択
        priority_keywords = ["実際", "具体的", "どのように", "なぜ"]
        
        for keyword in priority_keywords:
            for question in questions:
                if keyword in question:
                    return question
        
        return questions[0]

    def _select_key_suggestion(self, suggestions: List[Dict]) -> Optional[Dict]:
        """重要提案選択"""
        
        if not suggestions:
            return None
        
        # 実行可能性の高い提案を優先
        action_priorities = ["action", "integration", "analysis", "schedule"]
        
        for priority in action_priorities:
            for suggestion in suggestions:
                if suggestion.get("type") == priority:
                    return suggestion
        
        return suggestions[0]

    def _generate_contextual_follow_up(self, analysis: Dict) -> Optional[str]:
        """文脈的フォローアップ生成"""
        
        themes = analysis.get("interest_analysis", {}).get("current_themes", [])
        motivation = analysis.get("motivation_estimation", {}).get("primary_motivation")
        
        if not motivation:
            return None
        
        motivation_type = motivation.get("type")
        
        follow_up_templates = {
            "mirralism_application": "MIRRALISM開発への具体的な活用イメージはありますか？",
            "practical": "実装のタイムラインはお考えですか？", 
            "learning": "この分野でさらに深く学びたい側面はありますか？",
            "exploration": "関連する他のリソースもお探しですか？"
        }
        
        return follow_up_templates.get(motivation_type)

    def _generate_empathy_message(self, analysis: Dict) -> str:
        """共感メッセージ生成"""
        
        themes = analysis.get("interest_analysis", {}).get("current_themes", [])
        frequency = analysis.get("interest_analysis", {}).get("theme_frequency", {}).get("max_frequency", 0)
        
        if frequency > 5:
            return "継続的な関心をお持ちですね。深い探求心を感じます。"
        elif frequency > 2:
            return "この分野への興味が一貫していますね。"
        elif themes:
            return f"「{themes[0]}」への新しい視点ですね。"
        else:
            return "新しい発見がありそうですね。"

    def _determine_dialogue_tone(self, analysis: Dict) -> str:
        """対話トーン決定"""
        
        confidence = analysis.get("confidence_score", 0.5)
        
        if confidence > 0.8:
            return "confident"  # 確信的
        elif confidence > 0.6:
            return "engaged"    # 積極的
        elif confidence > 0.4:
            return "curious"    # 探求的
        else:
            return "supportive" # 支援的

    def _estimate_read_time(self, content_length: int) -> str:
        """読書時間推定"""
        
        if content_length == 0:
            return "不明"
        
        # 平均読書速度: 400文字/分（日本語）
        minutes = max(1, content_length // 400)
        
        if minutes < 5:
            return f"{minutes}分"
        elif minutes < 15:
            return f"{minutes}分（中程度）"
        else:
            return f"{minutes}分（長文）"

    def _get_complexity_label(self, complexity: float) -> str:
        """複雑度ラベル"""
        
        if complexity > 0.7:
            return "高度"
        elif complexity > 0.4:
            return "中程度"
        else:
            return "基礎的"

    def _get_actionability_label(self, actionability: float) -> str:
        """実行可能性ラベル"""
        
        if actionability > 0.7:
            return "すぐ実践可能"
        elif actionability > 0.4:
            return "実践検討可能"
        else:
            return "知識・理論中心"

    def _get_novelty_label(self, novelty: float) -> str:
        """新規性ラベル"""
        
        if novelty > 0.7:
            return "新分野"
        elif novelty > 0.3:
            return "新しい視点"
        else:
            return "継続分野"

    def _generate_dialogue_id(self) -> str:
        """対話ID生成"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"webclip_dialogue_{timestamp}"

    def _record_performance(self, performance: Dict):
        """パフォーマンス記録"""
        
        performance["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.performance_metrics.append(performance)
        
        # 最新100件を保持
        if len(self.performance_metrics) > 100:
            self.performance_metrics = self.performance_metrics[-100:]
        
        # 統計計算
        recent_times = [p["total_time"] for p in self.performance_metrics[-10:]]
        avg_time = sum(recent_times) / len(recent_times) if recent_times else 0
        success_rate = sum(1 for p in self.performance_metrics[-10:] if p["target_achieved"]) / len(recent_times) if recent_times else 0
        
        self.logger.info(f"📊 パフォーマンス - 平均: {avg_time:.2f}s, 成功率: {success_rate:.0%}")

    def _update_dialogue_history(self, analysis: Dict, dialogue: Dict, performance: Dict):
        """対話履歴更新"""
        
        history_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "article_title": analysis.get("article_info", {}).get("title", ""),
            "dialogue_summary": {
                "insight": dialogue["instant_insight"],
                "question": dialogue["primary_question"],
                "suggestion": dialogue.get("key_suggestion", {}).get("suggestion", "")
            },
            "performance": performance,
            "themes": analysis.get("interest_analysis", {}).get("current_themes", []),
            "confidence": analysis.get("confidence_score", 0)
        }
        
        self.dialogue_history.append(history_entry)
        
        # 最新500件を保持
        if len(self.dialogue_history) > 500:
            self.dialogue_history = self.dialogue_history[-500:]
        
        # 保存
        self._save_dialogue_history()

    def get_performance_summary(self) -> Dict[str, Any]:
        """パフォーマンス要約取得"""
        
        if not self.performance_metrics:
            return {"status": "no_data"}
        
        recent_metrics = self.performance_metrics[-20:]  # 最新20件
        
        total_times = [m["total_time"] for m in recent_metrics]
        success_count = sum(1 for m in recent_metrics if m["target_achieved"])
        
        return {
            "total_dialogues": len(self.performance_metrics),
            "recent_average_time": sum(total_times) / len(total_times),
            "recent_success_rate": success_count / len(recent_metrics),
            "target_achievement": f"{success_count}/{len(recent_metrics)}",
            "fastest_time": min(total_times),
            "slowest_time": max(total_times),
            "performance_trend": "improving" if success_count > len(recent_metrics) * 0.8 else "needs_optimization"
        }

    def _load_dialogue_history(self) -> List[Dict]:
        """対話履歴読み込み"""
        
        history_file = self.project_root / "Data" / "webclip_dialogue_history.json"
        
        try:
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"対話履歴読み込み失敗: {e}")
        
        return []

    def _save_dialogue_history(self):
        """対話履歴保存"""
        
        history_file = self.project_root / "Data" / "webclip_dialogue_history.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.dialogue_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"対話履歴保存失敗: {e}")


if __name__ == "__main__":
    # テスト実行
    dialogue_system = WebClipRealtimeDialogue()
    
    # パフォーマンステスト
    test_articles = [
        {
            "title": "Advanced AI Personality Learning Systems",
            "content": "This comprehensive guide covers the implementation of machine learning algorithms for personality analysis...",
            "url": "https://example.com/ai-personality"
        },
        {
            "title": "Leadership Management Strategies for Tech Teams", 
            "content": "Effective leadership in technology teams requires understanding both technical and human aspects...",
            "url": "https://example.com/tech-leadership"
        }
    ]
    
    print("🚀 WebClipリアルタイム対話システム テスト開始")
    print("=" * 60)
    
    for i, article in enumerate(test_articles, 1):
        print(f"\n📝 テスト {i}: {article['title']}")
        
        result = dialogue_system.process_webclip_realtime(
            article["content"], 
            article["url"], 
            article["title"],
            {"user_type": "CTO", "current_focus": "MIRRALISM development"}
        )
        
        if result["success"]:
            display = result["instant_display"]
            perf = result["performance"]
            
            print(f"⏱️  処理時間: {perf['total_time']:.2f}s ({'✅' if perf['target_achieved'] else '❌'} <2s目標)")
            print(f"💭 洞察: {display['primary_message']}")
            print(f"❓ 質問: {display['question']}")
            print(f"💡 提案: {display['suggestion']}")
            print(f"📊 信頼度: {display['motivation_confidence']}")
        else:
            print(f"❌ エラー: {result['error']}")
    
    # パフォーマンス要約
    summary = dialogue_system.get_performance_summary()
    print(f"\n📊 パフォーマンス要約")
    print(f"平均処理時間: {summary.get('recent_average_time', 0):.2f}s")
    print(f"目標達成率: {summary.get('recent_success_rate', 0):.0%}")
    print(f"パフォーマンス傾向: {summary.get('performance_trend', 'unknown')}")