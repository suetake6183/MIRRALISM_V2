#!/usr/bin/env python3
"""
MIRRALISM 正しい評価システム
末武さんの指摘を受けた修正版

Author: MIRRALISM Technical Team
Version: 2.0 (修正版)
Created: 2025-06-10
"""

import json
from datetime import datetime, timezone
from pathlib import Path


class CorrectTestSystem:
    """正しい評価収集システム"""

    def __init__(self):
        """初期化"""
        self.project_root = Path(__file__).parent.parent.parent
        self.results_file = self.project_root / "Data" / "correct_evaluation_results.json"
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

    def record_evaluation(self, score, comment=None):
        """評価を正しく記録"""
        evaluation_number = len(self.results["evaluations"]) + 1
        
        evaluation = {
            "evaluation_number": evaluation_number,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "score": score,
            "comment": comment if comment else None,
            "question": "黒澤工務店について教えて"
        }
        
        self.results["evaluations"].append(evaluation)
        self._save_results()
        
        print("✅ 評価{}記録完了: {}点".format(evaluation_number, score))
        
        if comment:
            print("   コメント: {}".format(comment))
        else:
            print("   コメント: なし")
        
        return evaluation

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
            if evaluation["comment"]:
                comment_text = " - {}".format(evaluation["comment"])
            else:
                comment_text = ""
            
            print("  評価{}: {}点{}".format(
                evaluation["evaluation_number"], 
                evaluation["score"],
                comment_text
            ))

    def interactive_evaluation(self):
        """インタラクティブな評価収集"""
        current_count = len(self.results["evaluations"]) + 1
        
        print("\n--- 評価 {}/10 ---".format(current_count))
        print("質問: 「黒澤工務店について教えて」")
        print("(この質問への私の回答を評価してください)")
        print()
        
        # 評価点数入力
        while True:
            try:
                score_input = input("評価{}: 何点ですか？ (1-5): ".format(current_count))
                score = int(score_input)
                if 1 <= score <= 5:
                    break
                else:
                    print("❌ 1から5の数字を入力してください")
            except ValueError:
                print("❌ 数字を入力してください")
        
        # コメント入力（任意）
        print()
        comment = input("コメント（任意、なければEnter）: ").strip()
        
        # コメントが空の場合はNoneにする
        if not comment:
            comment = None
        
        # 記録
        evaluation = self.record_evaluation(score, comment)
        
        return evaluation

    def run_full_test(self):
        """完全なテスト実行"""
        print("🎯 MIRRALISM クライアント理解精度テスト")
        print("="*50)
        print()
        print("【テスト手順】")
        print("1. 私に「黒澤工務店について教えて」と質問")
        print("2. 私の回答を読んで評価")
        print("3. 点数とコメント（任意）を入力")
        print("4. これを10回繰り返し")
        print()
        
        while len(self.results["evaluations"]) < 10:
            current_count = len(self.results["evaluations"]) + 1
            
            print("=" * 30)
            print("テスト {}/10回目".format(current_count))
            print("=" * 30)
            print()
            print("末武さん、私に質問してください:")
            print("→ 「黒澤工務店について教えて」")
            print()
            
            input("質問して回答を受け取ったらEnterキーを押してください...")
            
            # 評価収集
            self.interactive_evaluation()
            
            # 進捗表示
            self.show_progress()
            
            if len(self.results["evaluations"]) < 10:
                print("\n次のテストに進みます...")
            else:
                print("\n🎉 10回のテストが完了しました！")
                self.calculate_final_result()

    def calculate_final_result(self):
        """最終結果計算"""
        if len(self.results["evaluations"]) < 10:
            print("⚠️  まだ10回の評価が完了していません")
            return
        
        scores = [e["score"] for e in self.results["evaluations"]]
        average_score = sum(scores) / len(scores)
        accuracy_percentage = (average_score / 5.0) * 100
        
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
        
        return accuracy_percentage


def manual_record():
    """手動記録用の関数"""
    system = CorrectTestSystem()
    
    print("現在の状況:")
    system.show_progress()
    print()
    
    print("新しい評価を記録します:")
    evaluation = system.interactive_evaluation()
    
    print("\n更新後の状況:")
    system.show_progress()
    
    return evaluation


if __name__ == "__main__":
    system = CorrectTestSystem()
    
    print("=== MIRRALISM 正しい評価システム ===")
    print("使い方:")
    print("1. manual_record() で手動評価記録")
    print("2. run_full_test() で完全テスト実行")
    print()
    
    # 現在の状況表示
    system.show_progress() 