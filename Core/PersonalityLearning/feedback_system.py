#!/usr/bin/env python3
"""
MIRRALISM フィードバック→自己採点システム
末武さんフィードバック + AI客観的自己採点

Author: MIRRALISM Technical Team
Version: 3.0 (フィードバック分離版)
Created: 2025-06-10
"""

import json
from datetime import datetime, timezone
from pathlib import Path


class FeedbackSystem:
    """フィードバック→自己採点システム"""

    def __init__(self):
        """初期化"""
        self.project_root = Path(__file__).parent.parent.parent
        self.results_file = (
            self.project_root / "Data" / "feedback_evaluation_results.json"
        )
        self.results_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 既存結果読み込み
        self.results = self._load_results()

    def _load_results(self):
        """既存の評価結果読み込み"""
        if self.results_file.exists():
            try:
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {"evaluations": []}
        return {"evaluations": []}

    def _save_results(self):
        """評価結果保存"""
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

    def record_feedback_and_score(self, feedback, self_score, self_reasoning):
        """フィードバックと自己採点を記録"""
        evaluation_number = len(self.results["evaluations"]) + 1
        
        evaluation = {
            "evaluation_number": evaluation_number,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "suetake_feedback": feedback,
            "ai_self_score": self_score,
            "ai_reasoning": self_reasoning,
            "question": "黒澤工務店について教えて"
        }
        
        self.results["evaluations"].append(evaluation)
        self._save_results()
        
        print("✅ 評価{}記録完了".format(evaluation_number))
        print("   末武さんフィードバック: {}".format(feedback))
        print("   AI自己採点: {}点".format(self_score))
        print("   採点理由: {}".format(self_reasoning))
        
        return evaluation

    def show_progress(self):
        """現在の進捗表示"""
        total_evaluations = len(self.results["evaluations"])
        
        if total_evaluations == 0:
            print("📊 まだ評価がありません")
            return
        
        scores = [e["ai_self_score"] for e in self.results["evaluations"]]
        average = sum(scores) / len(scores)
        
        print("\n📊 現在の進捗:")
        print("評価回数: {}/10回".format(total_evaluations))
        print("AI自己採点平均: {:.2f}点".format(average))
        print("推定理解精度: {:.1f}%".format((average / 5.0) * 100))
        
        print("\n詳細:")
        for evaluation in self.results["evaluations"]:
            print("  評価{}: {}点".format(
                evaluation["evaluation_number"], 
                evaluation["ai_self_score"]
            ))
            print("    フィードバック: {}".format(
                evaluation["suetake_feedback"][:50] + "..." 
                if len(evaluation["suetake_feedback"]) > 50 
                else evaluation["suetake_feedback"]
            ))
            print("    採点理由: {}".format(
                evaluation["ai_reasoning"][:50] + "..."
                if len(evaluation["ai_reasoning"]) > 50
                else evaluation["ai_reasoning"]
            ))
            print()

    def calculate_final_result(self):
        """最終結果計算"""
        if len(self.results["evaluations"]) < 10:
            print("⚠️  まだ10回の評価が完了していません")
            return
        
        scores = [e["ai_self_score"] for e in self.results["evaluations"]]
        average_score = sum(scores) / len(scores)
        accuracy_percentage = (average_score / 5.0) * 100
        
        print("\n" + "="*60)
        print("🎯 最終テスト結果（AI自己評価）")
        print("="*60)
        print("総評価回数: {}回".format(len(scores)))
        print("AI自己採点平均: {:.2f}点 / 5点".format(average_score))
        print("推定理解精度: {:.1f}%".format(accuracy_percentage))
        print()
        
        # 改善傾向分析
        if len(scores) >= 5:
            recent_scores = scores[-5:]
            recent_average = sum(recent_scores) / len(recent_scores)
            early_scores = scores[:5]
            early_average = sum(early_scores) / len(early_scores)
            
            improvement = recent_average - early_average
            print("改善傾向分析:")
            print("  初期5回平均: {:.2f}点".format(early_average))
            print("  最新5回平均: {:.2f}点".format(recent_average))
            print("  改善度: {:.2f}点".format(improvement))
            
            if improvement > 0.5:
                print("  → 🌟 大幅改善！学習効果が見られます")
            elif improvement > 0:
                print("  → 👍 改善傾向！継続的な向上が見られます")
            elif improvement > -0.5:
                print("  → ⚖️  安定状態：一定レベルを維持")
            else:
                print("  → ⚠️  要注意：精度低下傾向")
        
        # 判定
        if accuracy_percentage >= 90:
            print("\n🌟 優秀! AI自己評価で高い理解精度を達成")
        elif accuracy_percentage >= 75:
            print("\n👍 良好! 改善の余地ありますが良好な精度")
        elif accuracy_percentage >= 60:
            print("\n⚠️  普通: かなりの改善が必要")
        else:
            print("\n🚨 要改善: 大幅な精度向上が必要")
        
        return accuracy_percentage


def record_new_evaluation():
    """新しい評価を記録する関数"""
    system = FeedbackSystem()
    
    print("=== フィードバック→自己採点記録 ===")
    print()
    
    # 末武さんのフィードバック入力
    print("1. 末武さんのフィードバックを入力:")
    feedback = input("フィードバック: ")
    
    print()
    print("2. AI自己採点:")
    
    while True:
        try:
            score_input = input("客観的自己評価 (1-5点): ")
            score = int(score_input)
            if 1 <= score <= 5:
                break
            else:
                print("❌ 1から5の数字を入力してください")
        except ValueError:
            print("❌ 数字を入力してください")
    
    print()
    reasoning = input("採点理由: ")
    
    # 記録
    evaluation = system.record_feedback_and_score(feedback, score, reasoning)
    
    print("\n--- 更新後の状況 ---")
    system.show_progress()
    
    return evaluation


if __name__ == "__main__":
    system = FeedbackSystem()
    
    print("=== MIRRALISM フィードバック→自己採点システム ===")
    print("使い方:")
    print("1. record_new_evaluation() で新しい評価記録")
    print("2. show_progress() で進捗確認")
    print()
    
    # 現在の状況表示
    system.show_progress() 