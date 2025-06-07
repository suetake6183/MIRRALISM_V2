#!/usr/bin/env python3
"""
データレビューシステム
===================

全てのSuperWhisperデータを一つずつレビューして、
ユーザーフィードバックから学習ルールを構築するシステム
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class DataReviewSystem:
    def __init__(self):
        self.project_root = Path("/Users/suetakeshuuhei/MIRRALISM_V2")
        self.review_db = self.project_root / ".mirralism" / "data_review.json"
        self.rules_db = self.project_root / ".mirralism" / "learning_rules.json"
        
        # ディレクトリ作成
        self.review_db.parent.mkdir(exist_ok=True)
        
        # データベース初期化
        self.reviews = self.load_reviews()
        self.rules = self.load_rules()
        
    def load_reviews(self) -> Dict:
        """レビューデータ読み込み"""
        if self.review_db.exists():
            with open(self.review_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"reviews": [], "stats": {"approved": 0, "rejected": 0, "pending": 0}}
    
    def save_reviews(self):
        """レビューデータ保存"""
        with open(self.review_db, 'w', encoding='utf-8') as f:
            json.dump(self.reviews, f, ensure_ascii=False, indent=2)
    
    def load_rules(self) -> Dict:
        """学習ルール読み込み"""
        if self.rules_db.exists():
            with open(self.rules_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "approval_patterns": [],
            "rejection_patterns": [],
            "keyword_weights": {},
            "quality_thresholds": {}
        }
    
    def save_rules(self):
        """学習ルール保存"""
        with open(self.rules_db, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=2)
    
    def find_all_superwhisper_files(self) -> List[Path]:
        """全SuperWhisperファイルを検索"""
        files = []
        for pattern in ["superwhisper_*.md", "superwhisper_raw_*.md"]:
            files.extend(self.project_root.rglob(pattern))
        return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def extract_metadata(self, file_path: Path) -> Dict:
        """ファイルからメタデータ抽出"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # YAML frontmatter解析
            metadata = {}
            if content.startswith('---'):
                yaml_end = content.find('---', 3)
                if yaml_end > 0:
                    yaml_content = content[3:yaml_end]
                    for line in yaml_content.strip().split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
            
            # 本文抽出
            if '---' in content:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
                else:
                    body = content
            else:
                body = content
                
            # 音声内容抽出
            audio_content = ""
            if "## 音声内容" in body:
                start = body.find("## 音声内容")
                end = body.find("##", start + 1)
                if end == -1:
                    audio_content = body[start:]
                else:
                    audio_content = body[start:end]
                audio_content = audio_content.replace("## 音声内容", "").strip()
            
            return {
                "file_path": str(file_path),
                "metadata": metadata,
                "audio_content": audio_content,
                "full_content": body,
                "file_size": len(content),
                "created_time": metadata.get("created", "Unknown"),
                "quality_score": float(metadata.get("quality_score", 0.0)),
                "text_length": len(audio_content)
            }
            
        except Exception as e:
            return {
                "file_path": str(file_path),
                "error": str(e),
                "metadata": {},
                "audio_content": "",
                "full_content": "",
                "file_size": 0,
                "created_time": "Unknown",
                "quality_score": 0.0,
                "text_length": 0
            }
    
    def get_next_unreviewed_file(self) -> Optional[Dict]:
        """次のレビュー対象ファイルを取得"""
        all_files = self.find_all_superwhisper_files()
        reviewed_files = {review["file_path"] for review in self.reviews["reviews"]}
        
        for file_path in all_files:
            if str(file_path) not in reviewed_files:
                return self.extract_metadata(file_path)
        
        return None
    
    def show_file_for_review(self, file_data: Dict):
        """レビュー用ファイル表示"""
        print("=" * 60)
        print("📄 SuperWhisperデータ レビュー")
        print("=" * 60)
        
        print(f"📁 ファイル: {Path(file_data['file_path']).name}")
        print(f"📅 作成日時: {file_data['created_time']}")
        print(f"📊 品質スコア: {file_data['quality_score']}")
        print(f"📝 文字数: {file_data['text_length']}文字")
        print()
        
        print("🎤 音声内容:")
        print("-" * 40)
        content = file_data['audio_content']
        if len(content) > 300:
            print(content[:300] + "...")
            print(f"（残り{len(content)-300}文字）")
        else:
            print(content)
        print("-" * 40)
        print()
    
    def collect_user_feedback(self, file_data: Dict) -> Dict:
        """ユーザーフィードバック収集"""
        print("🤔 このデータをPersonalityLearningに取り込みますか？")
        print()
        print("選択肢:")
        print("  ✅ [y] はい - 取り込む")
        print("  ❌ [n] いいえ - 取り込まない") 
        print("  ⏭️  [s] スキップ - 後で判断")
        print("  👀 [f] 全文表示 - 全体を確認")
        print("  🛑 [q] 終了 - レビュー終了")
        print()
        
        while True:
            choice = input("選択してください [y/n/s/f/q]: ").lower().strip()
            
            if choice == 'y':
                reason = input("✅ 取り込む理由（任意）: ").strip()
                return {
                    "decision": "approved",
                    "reason": reason,
                    "timestamp": datetime.now().isoformat()
                }
            elif choice == 'n':
                reason = input("❌ 取り込まない理由: ").strip()
                return {
                    "decision": "rejected", 
                    "reason": reason,
                    "timestamp": datetime.now().isoformat()
                }
            elif choice == 's':
                return {"decision": "skipped", "timestamp": datetime.now().isoformat()}
            elif choice == 'f':
                print("\n" + "="*60)
                print("📄 全文表示")
                print("="*60)
                print(file_data['full_content'])
                print("="*60 + "\n")
                continue
            elif choice == 'q':
                return {"decision": "quit"}
            else:
                print("❌ 無効な選択です。y/n/s/f/q のいずれかを入力してください。")
    
    def save_review(self, file_data: Dict, feedback: Dict):
        """レビュー結果保存"""
        review_entry = {
            "file_path": file_data["file_path"],
            "file_name": Path(file_data["file_path"]).name,
            "created_time": file_data["created_time"],
            "quality_score": file_data["quality_score"],
            "text_length": file_data["text_length"],
            "decision": feedback["decision"],
            "reason": feedback.get("reason", ""),
            "review_timestamp": feedback["timestamp"],
            "audio_content_preview": file_data["audio_content"][:100] + "..." if len(file_data["audio_content"]) > 100 else file_data["audio_content"]
        }
        
        self.reviews["reviews"].append(review_entry)
        
        # 統計更新
        if feedback["decision"] == "approved":
            self.reviews["stats"]["approved"] += 1
        elif feedback["decision"] == "rejected":
            self.reviews["stats"]["rejected"] += 1
        else:
            self.reviews["stats"]["pending"] += 1
        
        self.save_reviews()
    
    def show_stats(self):
        """統計表示"""
        stats = self.reviews["stats"]
        total = stats["approved"] + stats["rejected"] + stats["pending"]
        
        print("\n📊 レビュー統計:")
        print(f"   ✅ 承認: {stats['approved']}件")
        print(f"   ❌ 拒否: {stats['rejected']}件") 
        print(f"   ⏭️ 保留: {stats['pending']}件")
        print(f"   📊 合計: {total}件")
        
        if total > 0:
            print(f"   📈 承認率: {stats['approved']/total*100:.1f}%")
    
    def run_review_session(self):
        """レビューセッション実行"""
        print("🎯 SuperWhisperデータ レビューシステム")
        print("=" * 60)
        
        while True:
            # 次のファイル取得
            file_data = self.get_next_unreviewed_file()
            
            if not file_data:
                print("🎉 全てのファイルのレビューが完了しました！")
                self.show_stats()
                break
            
            # ファイル表示
            self.show_file_for_review(file_data)
            
            # フィードバック収集
            feedback = self.collect_user_feedback(file_data)
            
            if feedback["decision"] == "quit":
                print("🛑 レビューを終了します")
                self.show_stats()
                break
            
            # レビュー保存
            if feedback["decision"] != "skipped":
                self.save_review(file_data, feedback)
                print(f"💾 レビュー結果を保存しました: {feedback['decision']}")
            
            print()

def main():
    review_system = DataReviewSystem()
    review_system.run_review_session()

if __name__ == "__main__":
    main()