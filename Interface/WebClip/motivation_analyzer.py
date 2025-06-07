#!/usr/bin/env python3
"""
WebClip動機分析エンジン
====================

MIRRALISM V2 WebClip独立システム
目的: クリップ動機の深い理解とリアルタイム洞察生成

作成者: 技術責任者
作成日: 2025年6月6日
設計思想: Option B 分離最適化アプローチ
"""

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


class WebClipMotivationAnalyzer:
    """WebClipクリップ動機分析エンジン"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        動機分析エンジン初期化
        
        Args:
            project_root: MIRRALISMプロジェクトルート
        """
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.setup_logging()
        
        # 動機パターンDB
        self.motivation_patterns = self._load_motivation_patterns()
        
        # 興味追跡システム
        self.interest_history = self._load_interest_history()
        
        self.logger.info("✅ WebClip動機分析エンジン初期化完了")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - WEBCLIP_MOTIVATION - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def analyze_clip_motivation(
        self, 
        article_content: str, 
        article_url: str, 
        article_title: str,
        user_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        クリップ動機分析
        
        CTOの要求: 「あなたはこういうことに興味を持ったんですね」
        「なぜこの記事をクリップしたのか？」
        
        Args:
            article_content: 記事内容
            article_url: 記事URL
            article_title: 記事タイトル
            user_context: ユーザーコンテキスト
            
        Returns:
            動機分析結果
        """
        try:
            # 1. 内容分析
            content_analysis = self._analyze_content_themes(article_content, article_title)
            
            # 2. 興味パターン分析
            interest_analysis = self._analyze_interest_patterns(content_analysis)
            
            # 3. 動機推定
            motivation_estimation = self._estimate_motivation(
                content_analysis, interest_analysis, user_context
            )
            
            # 4. 質問生成
            questions = self._generate_motivation_questions(motivation_estimation)
            
            # 5. 活用提案
            utilization_suggestions = self._suggest_utilization(motivation_estimation)
            
            analysis_result = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "article_info": {
                    "title": article_title,
                    "url": article_url,
                    "content_length": len(article_content)
                },
                "content_analysis": content_analysis,
                "interest_analysis": interest_analysis,
                "motivation_estimation": motivation_estimation,
                "dialogue": {
                    "interest_insight": self._generate_interest_insight(interest_analysis),
                    "motivation_questions": questions,
                    "follow_up_questions": self._generate_follow_up_questions(motivation_estimation)
                },
                "utilization_suggestions": utilization_suggestions,
                "confidence_score": self._calculate_confidence(motivation_estimation)
            }
            
            # 6. 興味履歴更新
            self._update_interest_history(interest_analysis)
            
            self.logger.info(f"✅ クリップ動機分析完了: {article_title[:50]}...")
            
            return {
                "success": True,
                "analysis": analysis_result
            }
            
        except Exception as e:
            import traceback
            self.logger.error(f"❌ クリップ動機分析エラー: {e}")
            self.logger.error(f"詳細エラー: {traceback.format_exc()}")
            return {
                "success": False,
                "error": str(e),
                "article_title": article_title
            }

    def _analyze_content_themes(self, content: str, title: str) -> Dict[str, Any]:
        """記事内容のテーマ分析"""
        
        # キーワード抽出
        keywords = self._extract_keywords(content + " " + title)
        
        # テーマ分類
        themes = self._classify_themes(keywords, content)
        
        # 内容タイプ判定
        content_type = self._determine_content_type(content, title)
        
        return {
            "keywords": keywords,
            "themes": themes,
            "content_type": content_type,
            "complexity_level": self._assess_complexity(content),
            "actionability": self._assess_actionability(content)
        }

    def _analyze_interest_patterns(self, content_analysis: Dict) -> Dict[str, Any]:
        """興味パターン分析"""
        
        current_themes = content_analysis["themes"]
        
        # 過去の興味履歴と比較
        recent_interests = self._get_recent_interests(days=30)
        theme_frequency = self._calculate_theme_frequency(current_themes, recent_interests)
        
        # 興味の変化分析
        interest_trend = self._analyze_interest_trend(current_themes, recent_interests)
        
        # 新規性評価
        novelty_score = self._calculate_novelty(current_themes, recent_interests)
        
        return {
            "current_themes": current_themes,
            "theme_frequency": theme_frequency,
            "interest_trend": interest_trend,
            "novelty_score": novelty_score,
            "interest_intensity": self._calculate_interest_intensity(theme_frequency),
            "related_past_clips": self._find_related_clips(current_themes)
        }

    def _estimate_motivation(
        self, 
        content_analysis: Dict, 
        interest_analysis: Dict,
        user_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """動機推定"""
        
        motivations = []
        
        # 学習動機
        if content_analysis["content_type"] in ["educational", "tutorial", "guide"]:
            motivations.append({
                "type": "learning",
                "reason": "新しいスキルや知識を習得したい",
                "confidence": 0.8,
                "evidence": content_analysis["content_type"]
            })
        
        # 実践動機  
        if content_analysis["actionability"] > 0.7:
            motivations.append({
                "type": "practical",
                "reason": "実際の業務や活動に活用したい", 
                "confidence": content_analysis["actionability"],
                "evidence": "高い実行可能性"
            })
        
        # 探究動機
        if interest_analysis["novelty_score"] > 0.6:
            motivations.append({
                "type": "exploration", 
                "reason": "新しい分野への関心から",
                "confidence": interest_analysis["novelty_score"],
                "evidence": "新規性の高いテーマ"
            })
        
        # 継続動機
        if interest_analysis["theme_frequency"].get("max_frequency", 0) > 3:
            motivations.append({
                "type": "continuation",
                "reason": "継続的に関心を持っている分野の深掘り",
                "confidence": 0.7,
                "evidence": "過去の関心履歴"
            })
        
        # MIRRALISM関連動機
        mirralism_relevance = self._assess_mirralism_relevance(content_analysis)
        if mirralism_relevance > 0.5:
            motivations.append({
                "type": "mirralism_application",
                "reason": "MIRRALISMプロジェクトに応用できそう",
                "confidence": mirralism_relevance,
                "evidence": "MIRRALISM関連キーワード"
            })
        
        # 最も可能性の高い動機を特定
        primary_motivation = max(motivations, key=lambda x: x["confidence"]) if motivations else None
        
        return {
            "all_motivations": motivations,
            "primary_motivation": primary_motivation,
            "motivation_diversity": len(motivations),
            "overall_confidence": max([m["confidence"] for m in motivations]) if motivations else 0.3
        }

    def _generate_interest_insight(self, interest_analysis: Dict) -> str:
        """興味洞察メッセージ生成"""
        
        current_themes = interest_analysis["current_themes"]
        interest_trend = interest_analysis["interest_trend"]
        
        if not current_themes:
            return "この記事に興味を持たれたんですね"
        
        # 最も顕著なテーマ
        primary_theme = current_themes[0] if current_themes else "このテーマ"
        
        # トレンド情報
        if interest_trend.get("trending_up"):
            trend_info = f"最近「{primary_theme}」への関心が高まっていますね"
        elif interest_trend.get("consistent"):
            trend_info = f"継続的に「{primary_theme}」に興味をお持ちですね"
        else:
            trend_info = f"「{primary_theme}」に興味を持たれたんですね"
        
        # 頻度情報
        frequency = interest_analysis["theme_frequency"].get("max_frequency", 0)
        if frequency > 5:
            frequency_info = f"（今月{frequency}回目のクリップです）"
        elif frequency > 2:
            frequency_info = f"（今月{frequency}回目ですね）"
        else:
            frequency_info = ""
        
        return f"{trend_info}{frequency_info}"

    def _generate_motivation_questions(self, motivation_estimation: Dict) -> List[str]:
        """動機確認質問生成"""
        
        questions = []
        primary = motivation_estimation.get("primary_motivation")
        
        if not primary:
            return ["この記事をクリップされたのはどのような理由からでしょうか？"]
        
        motivation_type = primary["type"]
        
        question_templates = {
            "learning": [
                "新しい知識やスキルを習得するためでしょうか？",
                "学習目的でクリップされましたか？"
            ],
            "practical": [
                "実際の業務や活動に活用する予定ですか？",
                "具体的な実践を想定してクリップされましたか？"
            ],
            "exploration": [
                "新しい分野への興味からクリップされましたか？",
                "この分野をもっと探求したいと思われましたか？"
            ],
            "continuation": [
                "継続的に関心をお持ちの分野ですが、今回は何か新しい観点がありましたか？",
                "この分野の理解をさらに深めたいとお考えですか？"
            ],
            "mirralism_application": [
                "MIRRALISMプロジェクトに応用できそうだと感じられましたか？",
                "MIRRALISM の設計や戦略に参考になりそうでしょうか？"
            ]
        }
        
        questions.extend(question_templates.get(motivation_type, ["この記事をクリップされた理由を教えてください"]))
        
        return questions[:2]  # 最大2つの質問

    def _generate_follow_up_questions(self, motivation_estimation: Dict) -> List[str]:
        """フォローアップ質問生成"""
        
        return [
            "この記事をどのように活用する予定ですか？",
            "読み返すタイミングはいつ頃を想定していますか？",
            "類似のテーマで他に知りたいことはありますか？"
        ]

    def _suggest_utilization(self, motivation_estimation: Dict) -> List[Dict[str, str]]:
        """活用提案生成"""
        
        suggestions = []
        primary = motivation_estimation.get("primary_motivation")
        
        if not primary:
            return [{"type": "general", "suggestion": "後日じっくり読み返すことをお勧めします"}]
        
        motivation_type = primary["type"]
        
        suggestion_templates = {
            "learning": [
                {"type": "action", "suggestion": "重要ポイントをメモしながら読み返す"},
                {"type": "schedule", "suggestion": "学習時間を確保して集中的に読む"},
                {"type": "practice", "suggestion": "学んだ内容を実際に試してみる"}
            ],
            "practical": [
                {"type": "action", "suggestion": "具体的な実行計画を立てる"},
                {"type": "integration", "suggestion": "現在の業務プロセスへの組み込みを検討"},
                {"type": "test", "suggestion": "小規模なテスト実行を試してみる"}
            ],
            "exploration": [
                {"type": "research", "suggestion": "関連記事や書籍をさらに探す"},
                {"type": "connection", "suggestion": "既存の知識との関連性を考える"},
                {"type": "discussion", "suggestion": "専門家や同僚と議論してみる"}
            ],
            "mirralism_application": [
                {"type": "analysis", "suggestion": "MIRRALISM設計への適用可能性を分析"},
                {"type": "documentation", "suggestion": "プロジェクト資料として整理・保存"},
                {"type": "team_share", "suggestion": "チームメンバーと知見を共有"}
            ]
        }
        
        suggestions.extend(suggestion_templates.get(motivation_type, []))
        
        return suggestions[:3]  # 最大3つの提案

    def _extract_keywords(self, text: str) -> List[str]:
        """キーワード抽出"""
        
        # 簡易的なキーワード抽出（実際はより高度なNLP使用予定）
        words = re.findall(r'\b[a-zA-Zあ-ん一-龯]{3,}\b', text.lower())
        
        # 重要キーワードの特定（頻度と位置ベース）
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 頻度順でソート
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:10]]

    def _classify_themes(self, keywords: List[str], content: str) -> List[str]:
        """テーマ分類"""
        
        theme_keywords = {
            "technology": ["ai", "machine learning", "programming", "software", "tech", "digital"],
            "management": ["management", "leadership", "strategy", "team", "organization"],
            "business": ["business", "startup", "marketing", "sales", "revenue", "growth"],
            "design": ["design", "ui", "ux", "interface", "user experience"],
            "productivity": ["productivity", "efficiency", "workflow", "process", "automation"],
            "learning": ["learning", "education", "skill", "knowledge", "training"],
            "health": ["health", "wellness", "fitness", "mental", "physical"],
            "finance": ["finance", "investment", "money", "financial", "economics"]
        }
        
        themes = []
        content_lower = content.lower()
        
        for theme, theme_words in theme_keywords.items():
            if any(word in content_lower or word in keywords for word in theme_words):
                themes.append(theme)
        
        return themes

    def _determine_content_type(self, content: str, title: str) -> str:
        """内容タイプ判定"""
        
        combined_text = (content + " " + title).lower()
        
        if any(word in combined_text for word in ["how to", "tutorial", "guide", "step by step"]):
            return "tutorial"
        elif any(word in combined_text for word in ["news", "announcement", "breaking", "update"]):
            return "news"
        elif any(word in combined_text for word in ["analysis", "research", "study", "report"]):
            return "analysis"
        elif any(word in combined_text for word in ["opinion", "thought", "perspective", "view"]):
            return "opinion"
        elif any(word in combined_text for word in ["case study", "example", "implementation"]):
            return "case_study"
        else:
            return "informational"

    def _assess_complexity(self, content: str) -> float:
        """複雑度評価"""
        
        # 簡易的な複雑度評価
        technical_terms = len(re.findall(r'\b[A-Z]{2,}\b', content))  # 専門用語（大文字）
        long_sentences = len([s for s in content.split('.') if len(s) > 100])
        
        complexity_score = (technical_terms * 0.3 + long_sentences * 0.7) / 10
        return min(complexity_score, 1.0)

    def _assess_actionability(self, content: str) -> float:
        """実行可能性評価"""
        
        action_words = ["implement", "create", "build", "try", "test", "use", "apply", "practice"]
        action_count = sum(1 for word in action_words if word in content.lower())
        
        return min(action_count / len(action_words), 1.0)

    def _assess_mirralism_relevance(self, content_analysis: Dict) -> float:
        """MIRRALISM関連性評価"""
        
        mirralism_keywords = [
            "personality", "learning", "analysis", "intelligence", "insight",
            "personal", "growth", "development", "system", "platform",
            "automation", "ai", "data", "pattern", "behavior"
        ]
        
        themes = content_analysis.get("themes", [])
        keywords = content_analysis.get("keywords", [])
        
        relevance_count = 0
        for keyword in mirralism_keywords:
            if any(keyword in theme for theme in themes) or keyword in keywords:
                relevance_count += 1
        
        return min(relevance_count / len(mirralism_keywords), 1.0)

    def _get_recent_interests(self, days: int = 30) -> List[Dict]:
        """最近の興味履歴取得"""
        
        cutoff_date = datetime.now(timezone.utc).timestamp() - (days * 24 * 3600)
        
        return [
            entry for entry in self.interest_history 
            if entry.get("timestamp", 0) > cutoff_date
        ]

    def _calculate_theme_frequency(self, current_themes: List[str], recent_interests: List[Dict]) -> Dict:
        """テーマ頻度計算"""
        
        theme_count = {}
        
        for entry in recent_interests:
            for theme in entry.get("themes", []):
                theme_count[theme] = theme_count.get(theme, 0) + 1
        
        current_theme_frequencies = {
            theme: theme_count.get(theme, 0) for theme in current_themes
        }
        
        return {
            "frequencies": current_theme_frequencies,
            "max_frequency": max(current_theme_frequencies.values()) if current_theme_frequencies else 0,
            "total_clips": len(recent_interests)
        }

    def _analyze_interest_trend(self, current_themes: List[str], recent_interests: List[Dict]) -> Dict:
        """興味トレンド分析"""
        
        # 簡易的なトレンド分析
        recent_themes = []
        for entry in recent_interests[-10:]:  # 最新10件
            recent_themes.extend(entry.get("themes", []))
        
        trending_up = any(theme in recent_themes[-5:] for theme in current_themes)
        consistent = any(recent_themes.count(theme) >= 3 for theme in current_themes)
        
        return {
            "trending_up": trending_up,
            "consistent": consistent,
            "recent_themes": recent_themes
        }

    def _calculate_novelty(self, current_themes: List[str], recent_interests: List[Dict]) -> float:
        """新規性スコア計算"""
        
        past_themes = set()
        for entry in recent_interests:
            past_themes.update(entry.get("themes", []))
        
        new_themes = [theme for theme in current_themes if theme not in past_themes]
        
        if not current_themes:
            return 0.0
            
        return len(new_themes) / len(current_themes)

    def _calculate_interest_intensity(self, theme_frequency: Dict) -> float:
        """興味強度計算"""
        
        max_freq = theme_frequency.get("max_frequency", 0)
        total_clips = theme_frequency.get("total_clips", 0)
        
        # ゼロ除算回避
        if total_clips == 0:
            return 0.0
        
        return min(max_freq / total_clips, 1.0)

    def _find_related_clips(self, current_themes: List[str]) -> List[Dict]:
        """関連クリップ検索"""
        
        related = []
        
        for entry in self.interest_history:
            entry_themes = entry.get("themes", [])
            if any(theme in entry_themes for theme in current_themes):
                # 類似度計算（ゼロ除算回避）
                intersection = len(set(current_themes) & set(entry_themes))
                union = len(set(current_themes) | set(entry_themes))
                similarity = intersection / union if union > 0 else 0.0
                
                related.append({
                    "timestamp": entry.get("timestamp"),
                    "themes": entry_themes,
                    "title": entry.get("title", ""),
                    "similarity": similarity
                })
        
        return sorted(related, key=lambda x: x["similarity"], reverse=True)[:5]

    def _calculate_confidence(self, motivation_estimation: Dict) -> float:
        """総合信頼度計算"""
        
        primary = motivation_estimation.get("primary_motivation")
        diversity = motivation_estimation.get("motivation_diversity", 0)
        
        if not primary:
            return 0.3
        
        base_confidence = primary["confidence"]
        diversity_bonus = min(diversity * 0.1, 0.2)
        
        return min(base_confidence + diversity_bonus, 1.0)

    def _update_interest_history(self, interest_analysis: Dict):
        """興味履歴更新"""
        
        new_entry = {
            "timestamp": datetime.now(timezone.utc).timestamp(),
            "themes": interest_analysis["current_themes"],
            "analysis": interest_analysis
        }
        
        self.interest_history.append(new_entry)
        
        # 古いエントリーを削除（最新1000件を保持）
        if len(self.interest_history) > 1000:
            self.interest_history = self.interest_history[-1000:]
        
        # 保存
        self._save_interest_history()

    def _load_motivation_patterns(self) -> Dict:
        """動機パターンDB読み込み"""
        
        patterns_file = self.project_root / "Data" / "webclip_motivation_patterns.json"
        
        try:
            if patterns_file.exists():
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"動機パターン読み込み失敗: {e}")
        
        return {}

    def _load_interest_history(self) -> List[Dict]:
        """興味履歴読み込み"""
        
        history_file = self.project_root / "Data" / "webclip_interest_history.json"
        
        try:
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"興味履歴読み込み失敗: {e}")
        
        return []

    def _save_interest_history(self):
        """興味履歴保存"""
        
        history_file = self.project_root / "Data" / "webclip_interest_history.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.interest_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"興味履歴保存失敗: {e}")


if __name__ == "__main__":
    # テスト実行
    analyzer = WebClipMotivationAnalyzer()
    
    # サンプル分析
    test_result = analyzer.analyze_clip_motivation(
        article_content="AI-driven personality learning systems are revolutionizing personal development. This comprehensive guide explains how to implement advanced machine learning algorithms for personality analysis and behavioral insights.",
        article_url="https://example.com/ai-personality-learning",
        article_title="Advanced AI Personality Learning: Implementation Guide",
        user_context={"recent_activity": "MIRRALISM development"}
    )
    
    if test_result["success"]:
        analysis = test_result["analysis"]
        print("🎯 WebClip動機分析テスト結果")
        print("=" * 50)
        print(f"記事: {analysis['article_info']['title']}")
        print(f"興味洞察: {analysis['dialogue']['interest_insight']}")
        print("動機質問:")
        for q in analysis['dialogue']['motivation_questions']:
            print(f"  - {q}")
        print("活用提案:")
        for s in analysis['utilization_suggestions']:
            print(f"  - {s['suggestion']}")
        print(f"信頼度: {analysis['confidence_score']:.2f}")
    else:
        print(f"❌ テスト失敗: {test_result['error']}")