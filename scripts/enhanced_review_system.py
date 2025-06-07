#!/usr/bin/env python3
"""
MIRRALISM V2: 強化レビューシステム
================================

CTO承認に基づく戦略的実装
- 100%透明性保証
- ユーザー満足度95%以上達成
- 全68件SuperWhisperデータの体系的レビュー
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class MirralismReviewSystem:
    def __init__(self):
        self.project_root = Path("/Users/suetakeshuuhei/MIRRALISM_V2")
        self.review_log = self.project_root / ".mirralism" / "user_feedback_log.json"
        self.progress_file = self.project_root / ".mirralism" / "review_progress.json"
        
        # レビューデータ読み込み
        self.feedback_data = self.load_feedback_data()
        self.progress_data = self.load_progress_data()
        
    def load_feedback_data(self) -> Dict:
        """フィードバックデータ読み込み"""
        if self.review_log.exists():
            with open(self.review_log, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"reviews": [], "learned_rules": {"rejection_patterns": [], "approval_patterns": []}}
    
    def load_progress_data(self) -> Dict:
        """進捗データ読み込み"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "phase": "phase_1_superwhisper_review",
            "total_files": 0,
            "reviewed_files": 0,
            "approved_files": 0,
            "rejected_files": 0,
            "current_batch": 1,
            "target_daily_review": 10,
            "estimated_completion": "2025-06-13"
        }
    
    def get_all_superwhisper_files(self) -> List[Path]:
        """全SuperWhisperファイル取得"""
        files = []
        patterns = ["superwhisper_*.md", "superwhisper_raw_*.md"]
        
        for pattern in patterns:
            files.extend(self.project_root.rglob(pattern))
        
        # 作成日時でソート（古い順）
        return sorted(files, key=lambda x: x.stat().st_mtime)
    
    def get_reviewed_files(self) -> set:
        """レビュー済みファイル一覧"""
        reviewed = set()
        for review in self.feedback_data.get("reviews", []):
            reviewed.add(review["file_name"])
        return reviewed
    
    def get_next_review_batch(self, batch_size: int = 5) -> List[Dict]:
        """次のレビューバッチ取得"""
        all_files = self.get_all_superwhisper_files()
        reviewed_files = self.get_reviewed_files()
        
        batch_data = []
        count = 0
        
        for file_path in all_files:
            if file_path.name not in reviewed_files and count < batch_size:
                file_data = self.extract_file_data(file_path)
                if file_data:
                    batch_data.append(file_data)
                    count += 1
        
        return batch_data
    
    def extract_file_data(self, file_path: Path) -> Optional[Dict]:
        """ファイルデータ抽出"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # メタデータ抽出
            metadata = {}
            if content.startswith('---'):
                yaml_end = content.find('---', 3)
                if yaml_end > 0:
                    yaml_content = content[3:yaml_end]
                    for line in yaml_content.strip().split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
            
            # 音声内容抽出
            audio_content = ""
            if "## 音声内容" in content:
                start = content.find("## 音声内容")
                end = content.find("##", start + 1)
                if end == -1:
                    audio_content = content[start:]
                else:
                    audio_content = content[start:end]
                audio_content = audio_content.replace("## 音声内容", "").strip()
            
            return {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "created_time": metadata.get("created", "Unknown"),
                "quality_score": float(metadata.get("quality_score", 0.0)),
                "classification": metadata.get("classification", "Unknown"),
                "audio_content": audio_content,
                "content_length": len(audio_content),
                "file_size": file_path.stat().st_size
            }
            
        except Exception as e:
            print(f"⚠️ ファイル読み込みエラー: {file_path} - {e}")
            return None
    
    def display_review_batch(self, batch_data: List[Dict]):
        """レビューバッチ表示"""
        print("=" * 80)
        print("🎯 MIRRALISM Phase 1: SuperWhisperデータレビュー")
        print("=" * 80)
        print(f"📊 進捗: {len(self.get_reviewed_files())}/68件完了")
        print(f"📅 目標: 1日10件レビュー")
        print(f"🎯 完了予定: 2025年6月13日")
        print()
        
        for i, file_data in enumerate(batch_data, 1):
            print(f"📄 {i}. {file_data['file_name']}")
            print(f"   📅 作成: {file_data['created_time']}")
            print(f"   📊 品質: {file_data['quality_score']}")
            print(f"   📝 文字数: {file_data['content_length']}文字")
            print()
            
            # 音声内容プレビュー
            content = file_data['audio_content']
            if len(content) > 200:
                preview = content[:200] + "..."
            else:
                preview = content
            
            print(f"🎤 音声内容:")
            print(f"   {preview}")
            print("-" * 60)
            print()
        
        print("💭 レビュー方法:")
        print("   各ファイルについて Yes/No とその理由をお聞かせください")
        print("   一つずつ丁寧にレビューして、学習ルールを構築していきます")
        print()
    
    def show_learning_progress(self):
        """学習進捗表示"""
        stats = self.feedback_data.get("learned_rules", {}).get("stats", {})
        
        print("📈 現在の学習状況:")
        print(f"   ✅ 承認: {stats.get('approved', 0)}件")
        print(f"   ❌ 拒否: {stats.get('rejected', 0)}件")
        print(f"   📊 承認率: {stats.get('approval_rate', 0):.1f}%")
        print()
        
        # 学習済みパターン表示
        approval_patterns = self.feedback_data.get("learned_rules", {}).get("approval_patterns", [])
        rejection_patterns = self.feedback_data.get("learned_rules", {}).get("rejection_patterns", [])
        
        if approval_patterns:
            print("✅ 承認パターン:")
            for pattern in approval_patterns:
                print(f"   - {pattern['rule_name']}: {pattern['keywords'][:3]}...")
        
        if rejection_patterns:
            print("❌ 拒否パターン:")
            for pattern in rejection_patterns:
                print(f"   - {pattern['rule_name']}: {pattern['keywords'][:3]}...")
        print()
    
    def save_progress(self):
        """進捗保存"""
        all_files = self.get_all_superwhisper_files()
        reviewed_files = self.get_reviewed_files()
        
        self.progress_data.update({
            "total_files": len(all_files),
            "reviewed_files": len(reviewed_files),
            "last_update": datetime.now().isoformat(),
            "completion_rate": len(reviewed_files) / len(all_files) * 100 if all_files else 0
        })
        
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress_data, f, ensure_ascii=False, indent=2)

def main():
    system = MirralismReviewSystem()
    
    # 進捗表示
    system.show_learning_progress()
    
    # 次のバッチ取得
    batch = system.get_next_review_batch(5)
    
    if batch:
        system.display_review_batch(batch)
        print("👆 上記5件のデータについて、一つずつレビューをお願いします")
    else:
        print("🎉 全てのレビューが完了しました！")
    
    # 進捗保存
    system.save_progress()

if __name__ == "__main__":
    main()