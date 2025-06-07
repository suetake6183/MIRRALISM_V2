#!/usr/bin/env python3
"""
MIRRALISM PersonalityLearning Core - Phase 1 概念実証
===============================================

17時間実装スコープでの基本PersonalityLearning機能
概念実証レベルでの最小限実装

Phase 1 機能範囲:
- 基本的なテキスト分析
- 信頼度スコア生成
- クライアントデータ統合準備
- データベース保存機能

作成者: MIRRALISM V2 技術者
作成日: 2025年6月6日
"""

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class PersonalityLearningCorePhase1:
    """PersonalityLearning Core Phase 1 実装"""

    def __init__(self):
        """初期化"""
        self.setup_logging()
        self.analysis_stats = {
            "total_analyses": 0,
            "successful_analyses": 0,
            "average_confidence": 0.0,
            "session_start": datetime.now(timezone.utc).isoformat()
        }
        
        # Phase 1 基本分析パターン
        self.analysis_patterns = {
            "positive_indicators": [
                "成功", "完了", "達成", "向上", "改善", "成長", "発展", "革新",
                "効率", "品質", "価値", "満足", "幸せ", "貢献", "協力", "連携"
            ],
            "leadership_indicators": [
                "代表", "社長", "リーダー", "指導", "方針", "理念", "経営", "戦略",
                "判断", "決定", "責任", "管理", "統率", "ビジョン", "目標"
            ],
            "relationship_indicators": [
                "家族", "社員", "チーム", "パートナー", "協業", "信頼", "理解",
                "コミュニケーション", "対話", "相談", "支援", "サポート"
            ],
            "challenge_indicators": [
                "課題", "問題", "困難", "改善", "対策", "解決", "克服", "見直し",
                "調整", "修正", "強化", "最適化", "効率化"
            ]
        }

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - PERSONALITY_CORE - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def analyze_content(self, content: str, source_type: str = "text", metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """コンテンツ分析実行"""
        try:
            self.analysis_stats["total_analyses"] += 1
            
            # 基本分析実行
            analysis_result = self._perform_basic_analysis(content, source_type, metadata or {})
            
            # 信頼度計算
            confidence = self._calculate_confidence(analysis_result, content)
            
            # 結果統合
            final_result = {
                "success": True,
                "analysis": {
                    "suetake_likeness_index": confidence,
                    "content_analysis": analysis_result,
                    "source_type": source_type,
                    "metadata": metadata or {},
                    "analysis_timestamp": datetime.now(timezone.utc).isoformat()
                },
                "processing_info": {
                    "phase": "phase1_concept",
                    "analysis_version": "v2.0_basic",
                    "content_length": len(content),
                    "pattern_matches": analysis_result.get("total_pattern_matches", 0)
                }
            }
            
            # 統計更新
            self.analysis_stats["successful_analyses"] += 1
            self._update_confidence_average(confidence)
            
            self.logger.info(f"✅ 分析完了: {source_type} (信頼度: {confidence:.1f}%)")
            return final_result
            
        except Exception as e:
            self.logger.error(f"❌ 分析エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "analysis": {
                    "suetake_likeness_index": 0.0,
                    "source_type": source_type,
                    "metadata": metadata or {}
                }
            }

    def _perform_basic_analysis(self, content: str, source_type: str, metadata: Dict) -> Dict[str, Any]:
        """基本分析実行"""
        content_lower = content.lower()
        
        # パターンマッチング分析
        pattern_scores = {}
        total_matches = 0
        
        for category, patterns in self.analysis_patterns.items():
            matches = 0
            for pattern in patterns:
                if pattern in content_lower:
                    matches += 1
                    total_matches += 1
            
            pattern_scores[category] = {
                "matches": matches,
                "total_patterns": len(patterns),
                "match_ratio": matches / len(patterns) if patterns else 0.0
            }
        
        # クライアント特化分析（source_typeがclient_dataの場合）
        client_specific_analysis = {}
        if source_type == "client_data":
            client_specific_analysis = self._analyze_client_specific_patterns(content, metadata)
        
        # 基本分析結果
        analysis_result = {
            "pattern_analysis": pattern_scores,
            "total_pattern_matches": total_matches,
            "content_characteristics": {
                "length": len(content),
                "word_count": len(content.split()),
                "has_business_context": any(word in content_lower for word in ["事業", "経営", "会社", "組織"]),
                "has_relationship_context": any(word in content_lower for word in ["人", "社員", "家族", "チーム"]),
                "has_improvement_context": any(word in content_lower for word in ["改善", "向上", "成長", "発展"])
            },
            "client_specific": client_specific_analysis,
            "analysis_quality": self._assess_analysis_quality(content, total_matches)
        }
        
        return analysis_result

    def _analyze_client_specific_patterns(self, content: str, metadata: Dict) -> Dict[str, Any]:
        """クライアント特化パターン分析"""
        content_lower = content.lower()
        
        # クライアント業界特化分析
        industry = metadata.get("industry", "").lower()
        industry_relevance = 0.0
        
        if "建設" in industry or "住宅" in industry:
            construction_terms = ["建設", "住宅", "建築", "工務店", "施工", "設計"]
            matches = sum(1 for term in construction_terms if term in content_lower)
            industry_relevance = min(matches / len(construction_terms), 1.0)
        
        # クライアント重要度分析
        importance = metadata.get("importance", "medium")
        importance_multiplier = {
            "high": 1.2,
            "medium": 1.0,
            "low": 0.8
        }.get(importance, 1.0)
        
        # クライアント特化スコア
        client_focus_score = 0.0
        client_terms = ["クライアント", "顧客", "お客様", "取引先", "パートナー"]
        client_matches = sum(1 for term in client_terms if term in content_lower)
        client_focus_score = min(client_matches / len(client_terms), 1.0)
        
        return {
            "industry_relevance": industry_relevance,
            "importance_multiplier": importance_multiplier,
            "client_focus_score": client_focus_score,
            "business_context_strength": self._calculate_business_context_strength(content_lower)
        }

    def _calculate_business_context_strength(self, content_lower: str) -> float:
        """ビジネスコンテキスト強度計算"""
        business_terms = [
            "経営", "事業", "会社", "組織", "管理", "運営", "戦略", "計画",
            "目標", "成果", "効率", "品質", "価値", "成長", "発展", "改善"
        ]
        
        matches = sum(1 for term in business_terms if term in content_lower)
        return min(matches / len(business_terms), 1.0)

    def _calculate_confidence(self, analysis_result: Dict[str, Any], content: str) -> float:
        """信頼度計算"""
        base_confidence = 60.0  # Phase 1 ベース信頼度
        
        # パターンマッチング寄与
        pattern_contribution = 0.0
        pattern_analysis = analysis_result.get("pattern_analysis", {})
        for category, data in pattern_analysis.items():
            match_ratio = data.get("match_ratio", 0.0)
            category_weight = {
                "positive_indicators": 8.0,
                "leadership_indicators": 10.0,
                "relationship_indicators": 7.0,
                "challenge_indicators": 5.0
            }.get(category, 5.0)
            pattern_contribution += match_ratio * category_weight
        
        # コンテンツ品質寄与
        characteristics = analysis_result.get("content_characteristics", {})
        quality_bonus = 0.0
        
        if characteristics.get("has_business_context", False):
            quality_bonus += 5.0
        if characteristics.get("has_relationship_context", False):
            quality_bonus += 4.0
        if characteristics.get("has_improvement_context", False):
            quality_bonus += 3.0
        
        # 長さボーナス
        content_length = len(content)
        length_bonus = min(content_length / 500 * 2.0, 5.0)  # 最大5%ボーナス
        
        # クライアント特化ボーナス
        client_specific = analysis_result.get("client_specific", {})
        client_bonus = 0.0
        if client_specific:
            client_bonus += client_specific.get("industry_relevance", 0.0) * 3.0
            client_bonus += client_specific.get("client_focus_score", 0.0) * 2.0
            client_bonus *= client_specific.get("importance_multiplier", 1.0)
        
        # 最終信頼度計算
        final_confidence = base_confidence + pattern_contribution + quality_bonus + length_bonus + client_bonus
        
        # 上限・下限適用
        return max(0.0, min(95.0, final_confidence))

    def _assess_analysis_quality(self, content: str, total_matches: int) -> str:
        """分析品質評価"""
        content_length = len(content)
        match_density = total_matches / max(content_length / 100, 1)  # 100文字あたりのマッチ数
        
        if match_density >= 3.0 and content_length >= 200:
            return "high"
        elif match_density >= 1.5 and content_length >= 100:
            return "medium"
        else:
            return "basic"

    def _update_confidence_average(self, new_confidence: float):
        """平均信頼度更新"""
        current_avg = self.analysis_stats["average_confidence"]
        total_analyses = self.analysis_stats["successful_analyses"]
        
        if total_analyses == 1:
            self.analysis_stats["average_confidence"] = new_confidence
        else:
            self.analysis_stats["average_confidence"] = (
                (current_avg * (total_analyses - 1) + new_confidence) / total_analyses
            )

    def get_stats(self) -> Dict[str, Any]:
        """統計情報取得"""
        return self.analysis_stats.copy()

    def get_demo_analysis(self, content: str) -> Dict[str, Any]:
        """デモ用分析実行"""
        return self.analyze_content(
            content=content,
            source_type="demo",
            metadata={"demo_mode": True, "phase": "phase1_concept"}
        )


# Phase 1 統合クラス
class MirralismPersonalityLearningPhase1:
    """MIRRALISM PersonalityLearning統合システム Phase 1"""

    def __init__(self):
        """初期化"""
        self.core = PersonalityLearningCorePhase1()
        self.setup_logging()

    def setup_logging(self):
        """ログ設定"""
        self.logger = logging.getLogger("MIRRALISM_PL_PHASE1")

    def analyze_entry(self, content: str, source_type: str = "text", metadata: Optional[Dict] = None, voice_data: Optional[Dict] = None) -> Dict[str, Any]:
        """エントリー分析（統合システム互換インターフェース）"""
        try:
            # メタデータ拡張
            extended_metadata = metadata or {}
            if voice_data:
                extended_metadata["voice_data"] = voice_data
            
            # Core分析実行
            result = self.core.analyze_content(content, source_type, extended_metadata)
            
            self.logger.info(f"✅ 統合分析完了: {source_type}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 統合分析エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "analysis": {"suetake_likeness_index": 0.0}
            }

    def get_integration_status(self) -> Dict[str, Any]:
        """統合システム状態取得"""
        return {
            "phase": "phase1_concept",
            "core_available": True,
            "database_available": False,  # Phase 1では簡易実装
            "analysis_stats": self.core.get_stats(),
            "capabilities": [
                "基本テキスト分析",
                "クライアントデータ統合",
                "信頼度スコア生成",
                "パターンマッチング分析"
            ],
            "limitations": [
                "Phase 1 概念実証レベル",
                "基本分析機能のみ",
                "完全データベース統合は Phase 2"
            ]
        }


if __name__ == "__main__":
    # Phase 1 デモ実行
    pl_system = MirralismPersonalityLearningPhase1()
    
    test_content = """
    黒澤工務店株式会社は、さいたま市の建設業・住宅建築会社です。
    代表者の黒澤社長は理念重視型のリーダーで、「社員と家族、会社を取り巻く全ての人々を幸せにする」
    という経営理念を掲げています。現在の課題として組織内コミュニケーション体制の改善や
    人材不足と業務効率の向上が挙げられています。
    """
    
    result = pl_system.analyze_entry(
        content=test_content,
        source_type="client_data",
        metadata={
            "client_name": "黒澤工務店",
            "industry": "建設業・住宅建築",
            "importance": "high"
        }
    )
    
    print("🎯 MIRRALISM PersonalityLearning Phase 1 デモ")
    print("=" * 50)
    
    if result["success"]:
        analysis = result["analysis"]
        print(f"✅ 分析成功")
        print(f"📊 信頼度: {analysis['suetake_likeness_index']:.1f}%")
        print(f"🔍 分析品質: {analysis['content_analysis']['analysis_quality']}")
        print(f"📈 パターンマッチ数: {analysis['content_analysis']['total_pattern_matches']}")
    else:
        print(f"❌ 分析失敗: {result.get('error', 'unknown')}")
    
    # 統合システム状態表示
    status = pl_system.get_integration_status()
    print(f"\n🔧 システム状態: Phase {status['phase']}")
    print(f"📋 利用可能機能: {len(status['capabilities'])}個")