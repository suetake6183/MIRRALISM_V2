#!/usr/bin/env python3
"""
MIRRALISM 簡単評価記録システム
末武さんの評価を記録・管理

Author: MIRRALISM Technical Team  
Version: 1.0
Created: 2025-06-10
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


class SimpleTestRecorder:
    """末武さんの評価を簡単に記録するシステム"""

    def __init__(self):
        """初期化"""
        self.project_root = Path(__file__).parent.parent.parent
        self.results_file = self.project_root / "Data" / "suetake_evaluation_results.json"
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

    def record_score(self, score, comment=""):
        """スコアを記録"""
        evaluation = {
            "evaluation_number": len(self.results["evaluations"]) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "score": score,
            "comment": comment,
            "question": "黒澤工務店について教えて"
        }
        
        self.results["evaluations"].append(evaluation)
        self._save_results()
        
        print("✅ 評価{}記録完了: {}点".format(
            evaluation["evaluation_number"], score
        ))
        
        if comment:
            print("   コメント: {}".format(comment))

    def show_progress(self):
        """現在の進捗表示"""
        total_evaluations = len(self.results["evaluations"])
        
        if total_evaluations == 0:
            print("📊 まだ評価がありません")
            return
        
        scores = [e["score"] for e in self.results["evaluations"]]
        average = sum(scores) / len(scores)
        
        print("\n📊 現在の進捗:")
        print("評価回数: {}/10回".format(total_evaluations))
        print("現在の平均: {:.2f}点".format(average))
        print("理解精度: {:.1f}%".format((average / 5.0) * 100))
        
        print("\n詳細:")
        for evaluation in self.results["evaluations"]:
            comment_text = " - {}".format(evaluation["comment"]) if evaluation["comment"] else ""
            print("  評価{}: {}点{}".format(
                evaluation["evaluation_number"], 
                evaluation["score"],
                comment_text
            ))

    def calculate_final_result(self):
        """最終結果計算"""
        if len(self.results["evaluations"]) < 10:
            print("⚠️  まだ10回の評価が完了していません")
            return
        
        scores = [e["score"] for e in self.results["evaluations"]]
        average_score = sum(scores) / len(scores)
        accuracy_percentage = (average_score / 5.0) * 100
        
        # 最終結果保存
        final_result = {
            "test_id": "client_understanding_{}".format(
                datetime.now().strftime('%Y%m%d_%H%M%S')
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "test_type": "client_understanding",
            "target_client": "黒澤工務店",
            "total_evaluations": len(scores),
            "scores": scores,
            "average_score": average_score,
            "accuracy_percentage": accuracy_percentage,
            "evaluations": self.results["evaluations"]
        }
        
        # 最終結果ファイルに保存
        final_file = self.project_root / "Data" / "final_test_result.json"
        with open(final_file, 'w', encoding='utf-8') as f:
            json.dump(final_result, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*60)
        print("🎯 最終テスト結果")
        print("="*60)
        print("総評価回数: {}回".format(len(scores)))
        print("平均スコア: {:.2f}点 / 5点".format(average_score))
        print("理解精度: {:.1f}%".format(accuracy_percentage))
        print()
        
        # 判定
        if accuracy_percentage >= 90:
            print("🌟 優秀! MIRRALISMは黒澤工務店を非常によく理解しています")
        elif accuracy_percentage >= 75:
            print("👍 良好! もう少し改善の余地があります")
        elif accuracy_percentage >= 60:
            print("⚠️  普通: かなりの改善が必要です")
        else:
            print("🚨 要改善: 大幅な精度向上が必要です")
        
        print("\n✅ 最終結果保存: {}".format(final_file))
        
        return final_result


if __name__ == "__main__":
    recorder = SimpleTestRecorder()
    
    print("=== MIRRALISM 評価記録システム ===")
    print("使い方:")
    print("1. record_score(点数, コメント) で評価記録")
    print("2. show_progress() で進捗確認")
    print("3. calculate_final_result() で最終結果計算")
    print()
    
    # 現在の状況表示
    recorder.show_progress() 