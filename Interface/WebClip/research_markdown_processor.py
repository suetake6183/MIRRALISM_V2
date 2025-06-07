#!/usr/bin/env python3
"""
ディープリサーチマークダウン処理システム
=====================================

MIRRALISM V2 WebClip拡張システム
目的: Gemini/Perplexityリサーチファイルの統合処理

作成者: 技術責任者
作成日: 2025年6月6日
設計思想: WebClipシステム拡張による統一体験
"""

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 既存WebClipシステムからのインポート
from .motivation_analyzer import WebClipMotivationAnalyzer
from .yaml_processor import YAMLFrontmatterProcessor


class ResearchMarkdownProcessor:
    """ディープリサーチマークダウン処理システム"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        リサーチ処理システム初期化
        
        Args:
            project_root: MIRRALISMプロジェクトルート
        """
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.setup_logging()
        
        # 既存WebClipシステム統合
        self.motivation_analyzer = WebClipMotivationAnalyzer(project_root)
        self.yaml_processor = YAMLFrontmatterProcessor(project_root)
        
        # リサーチ特化システム
        self.research_sources = self._initialize_research_sources()
        self.processing_stats = {
            "total_processed": 0,
            "successful_processing": 0,
            "source_detection_accuracy": 0.0,
            "research_files_by_source": {}
        }
        
        self.logger.info("✅ ディープリサーチマークダウン処理システム初期化完了")

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - RESEARCH_MARKDOWN - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def process_research_markdown(
        self,
        markdown_file_path: str,
        user_context: Optional[Dict] = None,
        save_to_file: bool = True
    ) -> Dict[str, Any]:
        """
        リサーチマークダウンファイル完全処理
        
        CTOの要求:
        - マークダウンファイルの自動解析
        - リサーチソース検出（Gemini/Perplexity/Claude）
        - 既存動機分析システム適用："なぜこのリサーチをしたのか？"
        - WebClipと同様の統一体験
        
        Args:
            markdown_file_path: マークダウンファイルパス
            user_context: ユーザーコンテキスト
            save_to_file: ファイル保存フラグ
            
        Returns:
            処理結果
        """
        try:
            self.processing_stats["total_processed"] += 1
            
            file_path = Path(markdown_file_path)
            self.logger.info(f"🔍 リサーチマークダウン処理開始: {file_path.name}")
            
            # 1. マークダウンファイル読み込み・解析
            markdown_analysis = self._analyze_markdown_file(file_path)
            
            # 2. リサーチソース検出・分類
            source_detection = self._detect_research_source(markdown_analysis)
            
            # 3. リサーチ内容の構造化分析
            content_analysis = self._analyze_research_content(markdown_analysis, source_detection)
            
            # 4. 既存動機分析システム適用（WebClipと同じエンジン）
            motivation_result = self.motivation_analyzer.analyze_clip_motivation(
                article_content=content_analysis["structured_content"],
                article_url=f"research_file://{file_path.name}",
                article_title=content_analysis["research_title"],
                user_context={
                    **(user_context or {}),
                    "input_type": "research_markdown",
                    "research_source": source_detection["detected_source"],
                    "research_depth": content_analysis["research_depth"]
                }
            )
            
            # 5. リサーチ特化の質問・洞察生成
            research_insights = self._generate_research_insights(
                content_analysis, source_detection, motivation_result
            )
            
            # 6. YAML frontmatter生成（既存システム利用）
            yaml_result = self.yaml_processor.process_webclip_frontmatter(
                article_title=f"[{source_detection['detected_source']}] {content_analysis['research_title']}",
                article_url=f"research_file://{file_path.name}",
                article_content=content_analysis["structured_content"],
                clip_metadata={
                    "input_type": "research_markdown",
                    "source_file": str(file_path),
                    "research_source": source_detection["detected_source"],
                    "research_depth": content_analysis["research_depth"],
                    "processed_at": datetime.now(timezone.utc).isoformat()
                },
                user_context=user_context
            )
            
            # 7. 統合結果構築
            integrated_result = self._build_research_result(
                markdown_analysis, source_detection, content_analysis,
                motivation_result, research_insights, yaml_result
            )
            
            # 8. ファイル保存（オプション）
            save_result = None
            if save_to_file:
                save_result = self._save_research_file(integrated_result, file_path)
            
            # 統計更新
            self.processing_stats["successful_processing"] += 1
            self._update_source_stats(source_detection["detected_source"])
            
            result = {
                "success": True,
                "file_path": str(file_path),
                "research_analysis": integrated_result,
                "save_result": save_result,
                "processing_stats": self.processing_stats.copy()
            }
            
            self.logger.info(
                f"✅ リサーチマークダウン処理完了: {file_path.name} "
                f"[{source_detection['detected_source']}]"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ リサーチマークダウン処理エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "file_path": markdown_file_path,
                "processing_stats": self.processing_stats.copy()
            }

    def _analyze_markdown_file(self, file_path: Path) -> Dict[str, Any]:
        """マークダウンファイル解析"""
        
        try:
            # ファイル読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 基本メタデータ
            file_stats = file_path.stat()
            
            # マークダウン構造解析
            structure = self._parse_markdown_structure(content)
            
            return {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "file_size": file_stats.st_size,
                "created_time": datetime.fromtimestamp(file_stats.st_ctime, timezone.utc).isoformat(),
                "modified_time": datetime.fromtimestamp(file_stats.st_mtime, timezone.utc).isoformat(),
                "raw_content": content,
                "content_length": len(content),
                "structure": structure,
                "encoding": "utf-8"
            }
            
        except Exception as e:
            self.logger.error(f"❌ マークダウンファイル解析エラー: {e}")
            raise

    def _parse_markdown_structure(self, content: str) -> Dict[str, Any]:
        """マークダウン構造解析"""
        
        # ヘッダー抽出
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        
        # リンク抽出
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        # コードブロック抽出
        code_blocks = re.findall(r'```(\w*)\n(.*?)\n```', content, re.DOTALL)
        
        # 箇条書き抽出
        bullet_points = re.findall(r'^[\*\-\+]\s+(.+)$', content, re.MULTILINE)
        
        # 番号付きリスト抽出
        numbered_lists = re.findall(r'^\d+\.\s+(.+)$', content, re.MULTILINE)
        
        return {
            "headers": [{"level": len(h[0]), "text": h[1]} for h in headers],
            "links": [{"text": l[0], "url": l[1]} for l in links],
            "code_blocks": [{"language": cb[0], "code": cb[1]} for cb in code_blocks],
            "bullet_points": bullet_points,
            "numbered_lists": numbered_lists,
            "total_headers": len(headers),
            "total_links": len(links),
            "total_code_blocks": len(code_blocks),
            "paragraph_count": len([p for p in content.split('\n\n') if p.strip()])
        }

    def _detect_research_source(self, markdown_analysis: Dict) -> Dict[str, Any]:
        """リサーチソース検出・分類"""
        
        content = markdown_analysis["raw_content"].lower()
        file_name = markdown_analysis["file_name"].lower()
        
        # ソース検出パターン
        source_patterns = {
            "gemini": [
                "google gemini", "gemini pro", "gemini advanced", "bard",
                "ai.google.com", "gemini.google", "generated by gemini"
            ],
            "perplexity": [
                "perplexity", "perplexity.ai", "pplx", "perplexity pro",
                "generated by perplexity", "perplexity search"
            ],
            "claude": [
                "claude", "anthropic", "claude.ai", "claude pro",
                "generated by claude", "claude sonnet", "claude opus"
            ],
            "chatgpt": [
                "chatgpt", "openai", "gpt-4", "gpt-3.5", "chat.openai.com",
                "generated by chatgpt"
            ],
            "copilot": [
                "copilot", "microsoft copilot", "bing chat", "edge copilot"
            ]
        }
        
        # 検出実行
        detected_sources = []
        confidence_scores = {}
        
        for source, patterns in source_patterns.items():
            matches = 0
            for pattern in patterns:
                if pattern in content or pattern in file_name:
                    matches += 1
            
            if matches > 0:
                confidence = min(matches / len(patterns), 1.0)
                detected_sources.append(source)
                confidence_scores[source] = confidence
        
        # 主要ソース決定
        if detected_sources:
            primary_source = max(confidence_scores.keys(), key=lambda x: confidence_scores[x])
            confidence = confidence_scores[primary_source]
        else:
            primary_source = "unknown"
            confidence = 0.0
        
        # ファイル名からの推測
        filename_hints = self._extract_filename_hints(markdown_analysis["file_name"])
        
        return {
            "detected_source": primary_source,
            "confidence": confidence,
            "all_detected_sources": detected_sources,
            "confidence_scores": confidence_scores,
            "filename_hints": filename_hints,
            "detection_method": "pattern_matching" if detected_sources else "fallback"
        }

    def _extract_filename_hints(self, filename: str) -> Dict[str, Any]:
        """ファイル名からのヒント抽出"""
        
        # 日付パターン抽出
        date_patterns = [
            r'(\d{4}[-_]\d{2}[-_]\d{2})',  # YYYY-MM-DD
            r'(\d{2}[-_]\d{2}[-_]\d{4})',  # MM-DD-YYYY
            r'(\d{8})',                    # YYYYMMDD
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, filename)
            dates.extend(matches)
        
        # キーワード抽出
        keywords = re.findall(r'[a-zA-Z]{3,}', filename.replace('.md', ''))
        
        return {
            "extracted_dates": dates,
            "keywords": keywords,
            "extension": Path(filename).suffix,
            "basename": Path(filename).stem
        }

    def _analyze_research_content(self, markdown_analysis: Dict, source_detection: Dict) -> Dict[str, Any]:
        """リサーチ内容の構造化分析"""
        
        content = markdown_analysis["raw_content"]
        structure = markdown_analysis["structure"]
        
        # タイトル推定
        research_title = self._extract_research_title(structure, markdown_analysis["file_name"])
        
        # 研究深度評価
        research_depth = self._assess_research_depth(structure, content)
        
        # 主要トピック抽出
        main_topics = self._extract_main_topics(structure, content)
        
        # 情報源・引用分析
        sources_analysis = self._analyze_information_sources(structure)
        
        # 構造化コンテンツ生成（動機分析用）
        structured_content = self._create_structured_content_for_analysis(
            content, research_title, main_topics
        )
        
        return {
            "research_title": research_title,
            "research_depth": research_depth,
            "main_topics": main_topics,
            "sources_analysis": sources_analysis,
            "structured_content": structured_content,
            "content_type": "research_markdown",
            "estimated_read_time": self._estimate_read_time(len(content)),
            "complexity_level": self._assess_complexity_level(structure, content)
        }

    def _extract_research_title(self, structure: Dict, filename: str) -> str:
        """リサーチタイトル抽出"""
        
        # 最初のH1ヘッダーを使用
        headers = structure.get("headers", [])
        for header in headers:
            if header["level"] == 1:
                return header["text"]
        
        # H1がない場合はH2を使用
        for header in headers:
            if header["level"] == 2:
                return header["text"]
        
        # ヘッダーがない場合はファイル名から生成
        basename = Path(filename).stem
        return f"Research: {basename.replace('_', ' ').replace('-', ' ')}"

    def _assess_research_depth(self, structure: Dict, content: str) -> str:
        """研究深度評価"""
        
        # 深度指標
        header_count = structure.get("total_headers", 0)
        link_count = structure.get("total_links", 0)
        code_count = structure.get("total_code_blocks", 0)
        paragraph_count = structure.get("paragraph_count", 0)
        
        # スコア計算
        depth_score = (
            header_count * 0.3 +
            link_count * 0.2 +
            code_count * 0.1 +
            paragraph_count * 0.4
        )
        
        if depth_score > 20:
            return "comprehensive"  # 包括的
        elif depth_score > 10:
            return "detailed"       # 詳細
        elif depth_score > 5:
            return "moderate"       # 中程度
        else:
            return "basic"          # 基本的

    def _extract_main_topics(self, structure: Dict, content: str) -> List[str]:
        """主要トピック抽出"""
        
        topics = []
        
        # ヘッダーからトピック抽出
        headers = structure.get("headers", [])
        for header in headers:
            if header["level"] <= 3:  # H1-H3のみ
                topics.append(header["text"])
        
        # 頻出キーワード抽出（簡易版）
        words = re.findall(r'\b[A-Za-z]{4,}\b', content.lower())
        word_freq = {}
        for word in words:
            if word not in ['this', 'that', 'with', 'from', 'they', 'have', 'were', 'been', 'their']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 頻出上位5単語を追加
        frequent_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        topics.extend([word for word, freq in frequent_words if freq > 2])
        
        return topics[:10]  # 最大10トピック

    def _analyze_information_sources(self, structure: Dict) -> Dict[str, Any]:
        """情報源・引用分析"""
        
        links = structure.get("links", [])
        
        # ドメイン分析
        domains = {}
        for link in links:
            url = link["url"]
            if url.startswith(('http://', 'https://')):
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                    domains[domain] = domains.get(domain, 0) + 1
                except:
                    pass
        
        # 信頼性評価
        trusted_domains = {
            'wikipedia.org', 'nature.com', 'sciencedirect.com', 'arxiv.org',
            'pubmed.ncbi.nlm.nih.gov', 'scholar.google.com', 'ieee.org'
        }
        
        credibility_score = 0.0
        if domains:
            trusted_count = sum(1 for domain in domains.keys() if domain in trusted_domains)
            credibility_score = trusted_count / len(domains)
        
        return {
            "total_links": len(links),
            "unique_domains": len(domains),
            "domain_distribution": domains,
            "credibility_score": credibility_score,
            "has_citations": len(links) > 3
        }

    def _create_structured_content_for_analysis(
        self, content: str, title: str, topics: List[str]
    ) -> str:
        """動機分析用の構造化コンテンツ生成"""
        
        # 既存の動機分析システムが処理しやすい形式に変換
        structured = f"""Research Title: {title}

Main Topics: {', '.join(topics[:5])}

Content Summary:
{content[:1000]}...

Research Context: This is a deep research document containing detailed analysis and insights.
"""
        
        return structured

    def _estimate_read_time(self, content_length: int) -> str:
        """読書時間推定"""
        
        # 平均読書速度: 250単語/分（英語）、400文字/分（日本語）
        words_estimate = content_length / 5  # 平均単語長5文字と仮定
        minutes = max(1, int(words_estimate / 250))
        
        if minutes < 5:
            return f"{minutes}分"
        elif minutes < 15:
            return f"{minutes}分（中程度）"
        else:
            return f"{minutes}分（長文研究）"

    def _assess_complexity_level(self, structure: Dict, content: str) -> str:
        """複雑度レベル評価"""
        
        # 複雑度指標
        technical_terms = len(re.findall(r'\b[A-Z]{2,}\b', content))  # 専門用語
        code_blocks = structure.get("total_code_blocks", 0)
        nested_headers = len([h for h in structure.get("headers", []) if h["level"] > 2])
        
        complexity_score = technical_terms * 0.4 + code_blocks * 0.3 + nested_headers * 0.3
        
        if complexity_score > 15:
            return "expert"
        elif complexity_score > 8:
            return "advanced"
        elif complexity_score > 3:
            return "intermediate"
        else:
            return "basic"

    def _generate_research_insights(
        self,
        content_analysis: Dict,
        source_detection: Dict,
        motivation_result: Dict
    ) -> Dict[str, Any]:
        """リサーチ特化洞察生成"""
        
        # リサーチ特化の質問生成
        research_questions = self._generate_research_questions(
            content_analysis, source_detection
        )
        
        # 活用提案（リサーチ特化）
        utilization_suggestions = self._generate_research_utilization_suggestions(
            content_analysis, motivation_result
        )
        
        # リサーチ品質評価
        quality_assessment = self._assess_research_quality(
            content_analysis, source_detection
        )
        
        return {
            "research_questions": research_questions,
            "utilization_suggestions": utilization_suggestions,
            "quality_assessment": quality_assessment,
            "research_type": self._classify_research_type(content_analysis),
            "follow_up_recommendations": self._generate_follow_up_recommendations(content_analysis)
        }

    def _generate_research_questions(
        self, content_analysis: Dict, source_detection: Dict
    ) -> List[str]:
        """リサーチ特化質問生成"""
        
        questions = []
        
        research_depth = content_analysis["research_depth"]
        detected_source = source_detection["detected_source"]
        main_topics = content_analysis.get("main_topics", [])
        
        # 深度に応じた質問
        if research_depth == "comprehensive":
            questions.append("この包括的なリサーチは、どのような大きな決定や戦略のためでしょうか？")
        elif research_depth == "detailed":
            questions.append("詳細な調査をされましたが、具体的にどの部分が最も重要でしたか？")
        else:
            questions.append("このリサーチのきっかけとなった課題や疑問は何でしたか？")
        
        # ソースに応じた質問
        if detected_source == "gemini":
            questions.append("Geminiを選択された理由は何でしょうか？他のAIとの比較検討はありましたか？")
        elif detected_source == "perplexity":
            questions.append("Perplexityの検索結果で、最も価値があった情報は何でしたか？")
        elif detected_source == "claude":
            questions.append("Claudeとの対話で、予期しない洞察や発見はありましたか？")
        
        # トピックに応じた質問
        if main_topics:
            primary_topic = main_topics[0]
            questions.append(f"「{primary_topic}」について、今後さらに深く調べたい側面はありますか？")
        
        return questions[:3]  # 最大3つの質問

    def _generate_research_utilization_suggestions(
        self, content_analysis: Dict, motivation_result: Dict
    ) -> List[Dict[str, str]]:
        """リサーチ活用提案生成"""
        
        suggestions = []
        
        research_depth = content_analysis["research_depth"]
        complexity = content_analysis["complexity_level"]
        
        # 深度別提案
        if research_depth == "comprehensive":
            suggestions.append({
                "type": "strategic",
                "suggestion": "戦略文書として整理し、意思決定の参考資料にする"
            })
            suggestions.append({
                "type": "sharing",
                "suggestion": "チームや関係者と共有し、集合知として活用する"
            })
        else:
            suggestions.append({
                "type": "immediate",
                "suggestion": "具体的なアクションプランに落とし込む"
            })
        
        # 複雑度別提案
        if complexity in ["expert", "advanced"]:
            suggestions.append({
                "type": "learning",
                "suggestion": "専門知識として体系的に整理し、学習資料化する"
            })
        else:
            suggestions.append({
                "type": "practical",
                "suggestion": "実践的なガイドラインとして活用する"
            })
        
        # 動機結果からの提案
        if motivation_result.get("success"):
            analysis = motivation_result.get("analysis", {})
            primary_motivation = analysis.get("motivation_estimation", {}).get("primary_motivation")
            
            if primary_motivation and primary_motivation.get("type") == "mirralism_application":
                suggestions.append({
                    "type": "mirralism",
                    "suggestion": "MIRRALISMの設計・開発に直接適用する"
                })
        
        return suggestions[:4]  # 最大4つの提案

    def _assess_research_quality(
        self, content_analysis: Dict, source_detection: Dict
    ) -> Dict[str, Any]:
        """リサーチ品質評価"""
        
        # 品質指標
        depth_score = {"basic": 1, "moderate": 2, "detailed": 3, "comprehensive": 4}[
            content_analysis["research_depth"]
        ]
        
        complexity_score = {"basic": 1, "intermediate": 2, "advanced": 3, "expert": 4}[
            content_analysis["complexity_level"]
        ]
        
        source_confidence = source_detection["confidence"]
        
        sources_analysis = content_analysis["sources_analysis"]
        credibility_score = sources_analysis["credibility_score"]
        
        # 総合品質スコア
        overall_quality = (
            depth_score * 0.3 +
            complexity_score * 0.2 +
            source_confidence * 0.2 +
            credibility_score * 0.3
        ) / 4.0
        
        # 品質ラベル
        if overall_quality > 0.8:
            quality_label = "excellent"
        elif overall_quality > 0.6:
            quality_label = "good"
        elif overall_quality > 0.4:
            quality_label = "acceptable"
        else:
            quality_label = "needs_improvement"
        
        return {
            "overall_quality": overall_quality,
            "quality_label": quality_label,
            "depth_score": depth_score,
            "complexity_score": complexity_score,
            "source_confidence": source_confidence,
            "credibility_score": credibility_score,
            "recommendations": self._generate_quality_recommendations(overall_quality)
        }

    def _generate_quality_recommendations(self, quality_score: float) -> List[str]:
        """品質改善推奨事項"""
        
        recommendations = []
        
        if quality_score < 0.6:
            recommendations.append("より多くの信頼できる情報源からの情報収集を推奨")
            recommendations.append("専門家の意見や学術論文の参照を検討")
        
        if quality_score < 0.8:
            recommendations.append("関連する最新の研究や動向も調査対象に含める")
            recommendations.append("複数の視点からの分析を追加する")
        
        recommendations.append("定期的な情報更新と見直しを計画する")
        
        return recommendations

    def _classify_research_type(self, content_analysis: Dict) -> str:
        """リサーチタイプ分類"""
        
        main_topics = content_analysis.get("main_topics", [])
        complexity = content_analysis["complexity_level"]
        depth = content_analysis["research_depth"]
        
        # キーワードベースの分類
        topic_text = " ".join(main_topics).lower()
        
        if any(word in topic_text for word in ["technology", "ai", "machine", "software", "system"]):
            return "technology_research"
        elif any(word in topic_text for word in ["business", "strategy", "market", "management"]):
            return "business_research"
        elif any(word in topic_text for word in ["science", "research", "study", "analysis"]):
            return "academic_research"
        elif any(word in topic_text for word in ["health", "medical", "healthcare"]):
            return "health_research"
        else:
            return "general_research"

    def _generate_follow_up_recommendations(self, content_analysis: Dict) -> List[str]:
        """フォローアップ推奨事項"""
        
        recommendations = []
        
        research_type = self._classify_research_type(content_analysis)
        main_topics = content_analysis.get("main_topics", [])
        
        if research_type == "technology_research":
            recommendations.append("最新の技術動向の継続監視")
            recommendations.append("実装可能性の技術検証")
        elif research_type == "business_research":
            recommendations.append("競合分析の実施")
            recommendations.append("市場データの定量分析")
        
        if main_topics:
            recommendations.append(f"「{main_topics[0]}」の関連分野での追加調査")
        
        recommendations.append("専門家やコミュニティとの意見交換")
        
        return recommendations[:3]

    def _build_research_result(
        self,
        markdown_analysis: Dict,
        source_detection: Dict,
        content_analysis: Dict,
        motivation_result: Dict,
        research_insights: Dict,
        yaml_result: Dict
    ) -> Dict[str, Any]:
        """統合リサーチ結果構築"""
        
        return {
            "processing_timestamp": datetime.now(timezone.utc).isoformat(),
            "input_type": "research_markdown",
            
            # ファイル情報
            "file_analysis": {
                "file_path": markdown_analysis["file_path"],
                "file_name": markdown_analysis["file_name"],
                "file_size": markdown_analysis["file_size"],
                "created_time": markdown_analysis["created_time"],
                "modified_time": markdown_analysis["modified_time"]
            },
            
            # ソース検出結果
            "source_detection": source_detection,
            
            # コンテンツ分析
            "content_analysis": content_analysis,
            
            # 動機分析（WebClipと同じエンジン）
            "motivation_analysis": motivation_result,
            
            # リサーチ特化洞察
            "research_insights": research_insights,
            
            # 構造化データ
            "structured_data": {
                "frontmatter": yaml_result.get("frontmatter", {}),
                "markdown_output": yaml_result.get("markdown_file", ""),
                "yaml_processing": yaml_result
            },
            
            # 統合メタデータ
            "metadata": {
                "system_version": "v2.0_webclip_extended",
                "processing_engine": "research_markdown_processor",
                "components_used": [
                    "motivation_analyzer", "yaml_processor", 
                    "research_content_analyzer", "source_detector"
                ]
            }
        }

    def _save_research_file(self, integrated_result: Dict, original_path: Path) -> Dict[str, Any]:
        """リサーチファイル保存"""
        
        try:
            # 保存先ディレクトリ
            save_dir = self.project_root / "Data" / "research_files"
            save_dir.mkdir(parents=True, exist_ok=True)
            
            # ファイル名生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            source = integrated_result["source_detection"]["detected_source"]
            title = integrated_result["content_analysis"]["research_title"]
            safe_title = "".join(c for c in title if c.isalnum() or c in " -_")[:50]
            
            # マークダウンファイル保存
            markdown_filename = f"{timestamp}_{source}_{safe_title}.md"
            markdown_path = save_dir / markdown_filename
            
            markdown_content = integrated_result["structured_data"]["markdown_output"]
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # JSON分析結果保存
            json_filename = f"{timestamp}_{source}_analysis.json"
            json_path = save_dir / json_filename
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(integrated_result, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "markdown_file": str(markdown_path),
                "analysis_file": str(json_path),
                "original_file": str(original_path),
                "save_directory": str(save_dir)
            }
            
        except Exception as e:
            self.logger.error(f"❌ リサーチファイル保存エラー: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _update_source_stats(self, detected_source: str):
        """ソース統計更新"""
        
        source_stats = self.processing_stats["research_files_by_source"]
        source_stats[detected_source] = source_stats.get(detected_source, 0) + 1

    def _initialize_research_sources(self) -> Dict[str, Dict]:
        """リサーチソース初期化"""
        
        return {
            "gemini": {
                "name": "Google Gemini",
                "capabilities": ["reasoning", "research", "analysis"],
                "typical_outputs": ["detailed_analysis", "multi_perspective"]
            },
            "perplexity": {
                "name": "Perplexity AI",
                "capabilities": ["search", "synthesis", "citation"],
                "typical_outputs": ["sourced_research", "current_information"]
            },
            "claude": {
                "name": "Anthropic Claude",
                "capabilities": ["analysis", "reasoning", "writing"],
                "typical_outputs": ["structured_analysis", "thoughtful_insights"]
            },
            "chatgpt": {
                "name": "OpenAI ChatGPT",
                "capabilities": ["conversation", "analysis", "generation"],
                "typical_outputs": ["conversational_research", "creative_analysis"]
            },
            "copilot": {
                "name": "Microsoft Copilot",
                "capabilities": ["search", "productivity", "integration"],
                "typical_outputs": ["integrated_research", "productivity_focused"]
            }
        }

    def get_processing_statistics(self) -> Dict[str, Any]:
        """処理統計取得"""
        
        stats = self.processing_stats.copy()
        
        if stats["total_processed"] > 0:
            stats["success_rate"] = stats["successful_processing"] / stats["total_processed"]
            
            # ソース検出精度計算
            total_detections = sum(stats["research_files_by_source"].values())
            if total_detections > 0:
                stats["source_detection_accuracy"] = total_detections / stats["total_processed"]
        
        return stats


if __name__ == "__main__":
    # テスト実行
    processor = ResearchMarkdownProcessor()
    
    # サンプルマークダウンファイル作成・テスト
    import tempfile
    
    sample_content = """# AI Personality Learning Research

## Overview
This is a comprehensive research on AI-driven personality learning systems using Google Gemini Advanced.

## Key Findings
- Machine learning algorithms can effectively analyze personality patterns
- Real-time processing achieves sub-2-second response times
- User engagement increases by 300% with personalized insights

## Implementation Strategies
1. **Data Collection**: Voice input integration
2. **Analysis Engine**: Multi-dimensional personality assessment
3. **User Interface**: Intuitive dialogue system

## Sources
- [Nature Journal](https://nature.com/ai-personality)
- [MIT Technology Review](https://technologyreview.com/personality-ai)
- [Google AI Blog](https://ai.googleblog.com/personality-learning)

Generated by Google Gemini Advanced on 2025-06-06
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(sample_content)
        temp_path = f.name
    
    try:
        print("🧪 リサーチマークダウン処理システム テスト開始")
        print("=" * 60)
        
        result = processor.process_research_markdown(
            temp_path,
            user_context={"user_type": "CTO", "current_focus": "MIRRALISM development"},
            save_to_file=False
        )
        
        if result["success"]:
            analysis = result["research_analysis"]
            
            print(f"✅ 処理成功")
            print(f"📄 ファイル: {analysis['file_analysis']['file_name']}")
            print(f"🔍 検出ソース: {analysis['source_detection']['detected_source']} "
                  f"(信頼度: {analysis['source_detection']['confidence']:.0%})")
            print(f"📊 リサーチ深度: {analysis['content_analysis']['research_depth']}")
            print(f"🎯 複雑度: {analysis['content_analysis']['complexity_level']}")
            print(f"⭐ 品質: {analysis['research_insights']['quality_assessment']['quality_label']}")
            
            # 動機分析結果
            if analysis["motivation_analysis"].get("success"):
                motivation = analysis["motivation_analysis"]["analysis"]
                print(f"\n💭 動機洞察: {motivation['dialogue']['interest_insight']}")
                print("❓ リサーチ質問:")
                for q in analysis["research_insights"]["research_questions"]:
                    print(f"   - {q}")
        else:
            print(f"❌ 処理失敗: {result['error']}")
    
    finally:
        # 一時ファイル削除
        Path(temp_path).unlink()
    
    # 統計表示
    stats = processor.get_processing_statistics()
    print(f"\n📊 処理統計")
    print(f"成功率: {stats.get('success_rate', 0):.0%}")
    print(f"ソース検出精度: {stats.get('source_detection_accuracy', 0):.0%}")