#!/usr/bin/env python3
"""
MIRRALISM インタラクティブ精度測定システム
末武さんが実際に評価を入力して精度を測定

Author: MIRRALISM Technical Team
Version: 1.0 (Interactive Measurement)
Created: 2025-06-10 (末武さん指摘対応)
"""

import json
from datetime import datetime, timezone
from pathlib import Path


class InteractivePrecisionTest:
    """末武さんが使う実際の精度測定システム"""

    def __init__(self):
        """初期化"""
        self.project_root = Path(__file__).parent.parent.parent
        self.results_file = (
            self.project_root / "Data" / "suetake_evaluation_results.json"
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

    def run_client_understanding_test(self):
        """クライアント理解精度テスト実行"""
        print("\n" + "="*60)
        print("🎯 MIRRALISM クライアント理解精度テスト")
        print("="*60)
        print()
        
        print("【テスト手順】")
        print("1. MIRRALISMに「黒澤工務店について教えて」と質問してください")
        print("2. 回答を読んで、理解度を1-5で評価してください")
        print("3. この作業を10回繰り返します")
        print()
        
        print("【評価基準】")
        print("1点: 全然理解できていない")
        print("2点: あまり理解できていない") 
        print("3点: 普通")
        print("4点: よく理解できている")
        print("5点: 完璧に理解できている")
        print()
        
        input("準備ができたらEnterキーを押してください...")
        
        # 10回の評価を収集
        scores = []
        comments = []
        
        for i in range(1, 11):
            print("\n--- 評価 {}/10 ---".format(i))
            print("MIRRALISMに質問: 「黒澤工務店について教えて」")
            print()
            
            # 評価入力
            while True:
                try:
                    score = input("評価{}: MIRRALISMの回答は何点？ (1-5): ".format(i))
                    score = int(score)
                    if 1 <= score <= 5:
                        break
                    else:
                        print("❌ 1から5の数字を入力してください")
                except ValueError:
                    print("❌ 数字を入力してください")
            
            scores.append(score)
            
            # コメント入力（任意）
            comment = input("コメント{} (任意): ".format(i))
            comments.append(comment)
            
            print("✅ 評価{}完了: {}点".format(i, score))
        
        # 結果計算
        average_score = sum(scores) / len(scores)
        accuracy_percentage = (average_score / 5.0) * 100
        
        # 結果表示
        print("\n" + "="*60)
        print("📊 テスト結果")
        print("="*60)
        print("総評価回数: {}回".format(len(scores)))
        print("平均スコア: {:.2f}点 / 5点".format(average_score))
        print("理解精度: {:.1f}%".format(accuracy_percentage))
        print()
        
        print("詳細スコア:")
        for i, (score, comment) in enumerate(zip(scores, comments), 1):
            comment_text = " ({})".format(comment) if comment else ""
            print("  評価{}: {}点{}".format(i, score, comment_text))
        
        # 結果保存
        evaluation_result = {
            "test_id": "client_understanding_{}".format(
                datetime.now().strftime('%Y%m%d_%H%M%S')
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "test_type": "client_understanding",
            "target_client": "黒澤工務店",
            "scores": scores,
            "comments": comments,
            "average_score": average_score,
            "accuracy_percentage": accuracy_percentage,
            "total_evaluations": len(scores)
        }
        
        self.results["evaluations"].append(evaluation_result)
        self._save_results()
        
        print("\n✅ 結果が保存されました: {}".format(self.results_file))
        
        # 判定とアドバイス
        print("\n📈 評価:")
        if accuracy_percentage >= 90:
            print("🌟 優秀! MIRRALISMは黒澤工務店を非常によく理解しています")
        elif accuracy_percentage >= 75:
            print("👍 良好! もう少し改善の余地があります")
        elif accuracy_percentage >= 60:
            print("⚠️  普通: かなりの改善が必要です")
        else:
            print("🚨 要改善: 大幅な精度向上が必要です")
        
        return evaluation_result

    def run_data_integration_check(self):
        """データ統合確認テスト"""
        print("\n" + "="*60)
        print("📁 統合データ確認テスト")
        print("="*60)
        print()
        
        projects_dir = self.project_root / "Clients" / "Projects"
        
        if not projects_dir.exists():
            print("❌ Clients/Projectsディレクトリが存在しません")
            return
        
        # legacy_ファイルを検索
        legacy_files = list(projects_dir.glob("legacy_*"))
        
        print("📊 統合結果:")
        print("統合されたファイル数: {}個".format(len(legacy_files)))
        print()
        
        if legacy_files:
            print("統合されたファイル一覧:")
            for i, file_path in enumerate(legacy_files[:10], 1):  # 最初の10個を表示
                print("  {}. {}".format(i, file_path.name))
            
            if len(legacy_files) > 10:
                print("  ... 他{}個".format(len(legacy_files) - 10))
        
        print()
        print("【確認作業】")
        print("1. 上記ファイルを実際に開いて内容を確認してください")
        print("2. 価値のありそうなクライアント情報を3つ選んでください")
        print("3. 黒澤工務店以外で使えそうなデータがあるか確認してください")
        print()
        
        # ユーザーからの価値判定入力
        valuable_data = []
        print("価値ある情報を3つ入力してください:")
        
        for i in range(1, 4):
            data_info = input("価値あるデータ{} (ファイル名または内容): ".format(i))
            if data_info.strip():
                valuable_data.append(data_info.strip())
        
        # 結果保存
        integration_result = {
            "test_id": "data_integration_{}".format(
                datetime.now().strftime('%Y%m%d_%H%M%S')
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "test_type": "data_integration_check",
            "total_legacy_files": len(legacy_files),
            "valuable_data_identified": valuable_data,
            "integration_status": "completed" if legacy_files else "failed"
        }
        
        self.results["evaluations"].append(integration_result)
        self._save_results()
        
        print("\n✅ データ統合確認完了")
        print("結果保存先: {}".format(self.results_file))
        
        return integration_result

    def run_consistency_test(self):
        """システム一貫性テスト"""
        print("\n" + "="*60)
        print("🔄 システム一貫性テスト")
        print("="*60)
        print()
        
        print("【テスト手順】")
        print("1. 同じ質問をMIRRALISMに2回投げる")
        print("2. 回答の一貫性を評価する")
        print("3. 3つの質問でテストします")
        print()
        
        test_questions = [
            "黒澤工務店の特徴を教えて",
            "黒澤工務店に最適な提案は何か？",
            "黒澤工務店の今後の反応を予測して"
        ]
        
        consistency_results = []
        
        for i, question in enumerate(test_questions, 1):
            print("\n--- 質問{}/3 ---".format(i))
            print("質問: 「{}」".format(question))
            print()
            
            print("この質問をMIRRALISMに2回投げて、回答を比較してください")
            print()
            
            # 一貫性評価
            while True:
                consistency = input(
                    "一貫性評価 (○: 同じ回答 / △: 似ている / ×: 違う回答): "
                )
                if consistency in ['○', '△', '×']:
                    break
                else:
                    print("❌ ○、△、×のいずれかを入力してください")
            
            # コメント
            comment = input("コメント (任意): ")
            
            consistency_results.append({
                "question": question,
                "consistency": consistency,
                "comment": comment
            })
            
            print("✅ 質問{}評価完了: {}".format(i, consistency))
        
        # 結果集計
        consistent_count = sum(
            1 for r in consistency_results if r["consistency"] == "○"
        )
        similar_count = sum(
            1 for r in consistency_results if r["consistency"] == "△"
        )
        inconsistent_count = sum(
            1 for r in consistency_results if r["consistency"] == "×"
        )
        
        print("\n" + "="*60)
        print("📊 一貫性テスト結果")
        print("="*60)
        print("一貫している: {}個 (○)".format(consistent_count))
        print("似ている: {}個 (△)".format(similar_count))
        print("一貫していない: {}個 (×)".format(inconsistent_count))
        print()
        
        # 結果保存
        consistency_test_result = {
            "test_id": "consistency_{}".format(
                datetime.now().strftime('%Y%m%d_%H%M%S')
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "test_type": "system_consistency",
            "questions_tested": len(test_questions),
            "consistent_responses": consistent_count,
            "similar_responses": similar_count,
            "inconsistent_responses": inconsistent_count,
            "details": consistency_results
        }
        
        self.results["evaluations"].append(consistency_test_result)
        self._save_results()
        
        # 総合評価
        if consistent_count == 3:
            print("🌟 優秀! システムは完全に一貫しています")
        elif consistent_count >= 2:
            print("👍 良好! 概ね一貫しています")
        else:
            print("⚠️  要改善: 一貫性に問題があります")
        
        return consistency_test_result

    def show_all_results(self):
        """全ての評価結果表示"""
        print("\n" + "="*60)
        print("📊 これまでの評価結果")
        print("="*60)
        
        if not self.results["evaluations"]:
            print("まだ評価結果がありません")
            return
        
        for i, evaluation in enumerate(self.results["evaluations"], 1):
            print("{}. {} - {}".format(
                i, 
                evaluation.get('test_type', 'unknown'),
                evaluation.get('timestamp', '')[:10]
            ))
            
            if evaluation["test_type"] == "client_understanding":
                print("   クライアント理解精度: {:.1f}%".format(
                    evaluation.get('accuracy_percentage', 0)
                ))
            elif evaluation["test_type"] == "data_integration_check":
                print("   統合ファイル数: {}個".format(
                    evaluation.get('total_legacy_files', 0)
                ))
            elif evaluation["test_type"] == "system_consistency":
                print("   一貫性: {}/3".format(
                    evaluation.get('consistent_responses', 0)
                ))

    def main_menu(self):
        """メインメニュー"""
        while True:
            print("\n" + "="*60)
            print("🎯 MIRRALISM 精度測定システム")
            print("="*60)
            print()
            print("1. クライアント理解精度テスト (24時間以内)")
            print("2. データ統合確認テスト (48時間以内)")
            print("3. システム一貫性テスト (72時間以内)")
            print("4. これまでの結果を見る")
            print("5. 終了")
            print()
            
            choice = input("選択してください (1-5): ")
            
            if choice == "1":
                self.run_client_understanding_test()
            elif choice == "2":
                self.run_data_integration_check()
            elif choice == "3":
                self.run_consistency_test()
            elif choice == "4":
                self.show_all_results()
            elif choice == "5":
                print("\n👋 測定システムを終了します")
                break
            else:
                print("❌ 1から5の数字を選んでください")


if __name__ == "__main__":
    tester = InteractivePrecisionTest()
    tester.main_menu() 