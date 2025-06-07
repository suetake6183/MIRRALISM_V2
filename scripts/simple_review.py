#!/usr/bin/env python3
"""
簡単レビューシステム
==================

一つのファイルを表示して、手動で判定結果を入力するシステム
"""

import json
from pathlib import Path

def show_first_file():
    """最初のファイルを表示"""
    project_root = Path("/Users/suetakeshuuhei/MIRRALISM_V2")
    files = list(project_root.rglob("superwhisper_*.md"))
    
    if not files:
        print("SuperWhisperファイルが見つかりません")
        return None
        
    # 最新ファイルを取得
    latest_file = max(files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("=" * 60)
        print("📄 SuperWhisperデータ サンプル表示")
        print("=" * 60)
        print(f"📁 ファイル: {latest_file.name}")
        print()
        
        # 音声内容抽出
        if "## 音声内容" in content:
            start = content.find("## 音声内容")
            end = content.find("##", start + 1)
            if end == -1:
                audio_content = content[start:]
            else:
                audio_content = content[start:end]
            
            audio_text = audio_content.replace("## 音声内容", "").strip()
            
            print("🎤 音声内容:")
            print("-" * 40)
            print(audio_text)
            print("-" * 40)
        
        print()
        print("💭 判定をお聞かせください:")
        print("このようなデータをPersonalityLearningに取り込むべきかどうか、")
        print("チャットで教えてください。")
        
        return {
            "file_path": str(latest_file),
            "content": content,
            "audio_content": audio_text if "audio_text" in locals() else ""
        }
        
    except Exception as e:
        print(f"エラー: {e}")
        return None

if __name__ == "__main__":
    show_first_file()