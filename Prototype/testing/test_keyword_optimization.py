#!/usr/bin/env python3
"""
MIRRALISM キーワード最適化テストシステム
=======================================

目的: PersonalityLearning キーワード重み最適化
作成日: 2025年6月3日
"""

import json
import sqlite3
from pathlib import Path


class KeywordOptimizationTester:
    """キーワード重み最適化テストシステム"""

    def __init__(self, db_path="Data/raw/personality_learning.db"):
        self.db_path = Path(db_path)
        self.current_tech_weight = 5
        self.current_integrity_weight = 3

    def test_weight_combinations(self):
        """異なる重み組み合わせをテスト"""
        test_combinations = [
            (3, 2),  # 控えめ
            (5, 3),  # 現在値
            (7, 4),  # 強化版
            (10, 5),  # 最大化
        ]

        results = []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # テストデータ取得
            cursor.execute(
                """
                SELECT suetake_likeness_index, tech_keywords, integrity_keywords
                FROM daily_analysis
                ORDER BY created_at DESC
                LIMIT 5
            """
            )

            test_data = cursor.fetchall()
            conn.close()

            if not test_data:
                return {"error": "テストデータが見つかりません"}

            for tech_weight, integrity_weight in test_combinations:
                scores = []

                for confidence, tech_count, integrity_count in test_data:
                    base_score = 91.5
                    tech_bonus = (tech_count or 0) * tech_weight
                    integrity_bonus = (integrity_count or 0) * integrity_weight

                    total_score = min(base_score + tech_bonus + integrity_bonus, 100.0)
                    scores.append(total_score)

                avg_score = sum(scores) / len(scores)
                score_variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)

                results.append(
                    {
                        "tech_weight": tech_weight,
                        "integrity_weight": integrity_weight,
                        "average_score": round(avg_score, 2),
                        "variance": round(score_variance, 2),
                        "score_range": f"{min(scores):.1f}% - {max(scores):.1f}%",
                        "is_current": (tech_weight == 5 and integrity_weight == 3),
                    }
                )

            return {
                "test_results": results,
                "recommendation": self._generate_recommendation(results),
            }

        except Exception as e:
            return {"error": f"テストエラー: {str(e)}"}

    def _generate_recommendation(self, results):
        """最適化推奨事項を生成"""
        current_result = next((r for r in results if r["is_current"]), None)

        if not current_result:
            return "現在設定のテスト結果が見つかりません"

        # 分散が最小でスコアが高い組み合わせを推奨
        best_result = min(results, key=lambda x: x["variance"])

        if best_result["tech_weight"] == 5 and best_result["integrity_weight"] == 3:
            return "現在の重み設定が最適です"
        else:
            return f"推奨重み: tech={best_result['tech_weight']}, integrity={best_result['integrity_weight']} (分散最小化)"

    def run_optimization_test(self):
        """最適化テスト実行"""
        print("🔬 キーワード重み最適化テスト開始")

        results = self.test_weight_combinations()

        if "error" in results:
            print(f"❌ エラー: {results['error']}")
            return results

        print("\n📊 テスト結果:")
        for result in results["test_results"]:
            status = " (現在値)" if result["is_current"] else ""
            print(
                f"Tech={result['tech_weight']}, Integrity={result['integrity_weight']}: "
                f"平均{result['average_score']}%, 分散{result['variance']}{status}"
            )

        print(f"\n💡 推奨事項: {results['recommendation']}")

        return results


if __name__ == "__main__":
    tester = KeywordOptimizationTester()
    results = tester.run_optimization_test()

    # JSON出力
    output_file = "Data/analytics/keyword_optimization_results.json"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 詳細結果: {output_file}")
