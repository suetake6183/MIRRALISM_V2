#!/usr/bin/env python3
"""
MIRRALISM V2 オートラン専用スクリプト
================================

ClaudeCodeや自動化システムから呼び出し用の
シンプルなオートラン実行スクリプト
"""

import sys
import os
from pathlib import Path

# パス設定
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

from file_organizer import FlexibleFileOrganizer


def auto_cleanup(silent=False):
    """サイレントオートラン実行"""
    try:
        organizer = FlexibleFileOrganizer()
        
        if not silent:
            print("🤖 MIRRALISM オートクリーンアップ開始...")
        
        # オートラン強制有効化（このスクリプト用）
        organizer.config["auto_run"]["enabled"] = True
        organizer.config["auto_run"]["auto_confirm"] = True
        
        # オートラン実行
        results = organizer.auto_run_cleanup()
        
        if not silent:
            print(f"✅ 完了: {results['moved']}ファイル整理, {results['errors']}エラー")
        
        return results
        
    except Exception as e:
        if not silent:
            print(f"❌ エラー: {e}")
        return {"moved": 0, "errors": 1, "skipped": 0}


def main():
    """メイン実行"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MIRRALISM オートクリーンアップ")
    parser.add_argument("--silent", action="store_true", help="サイレント実行")
    parser.add_argument("--check", action="store_true", help="整理対象ファイル数のみ確認")
    
    args = parser.parse_args()
    
    if args.check:
        # 整理対象ファイル数確認のみ
        from pathlib import Path
        organizer = FlexibleFileOrganizer()
        
        target_files = []
        for item in organizer.root_dir.iterdir():
            if item.is_file() and not item.name.startswith("."):
                category, _ = organizer.classify_file(item.name)
                if category != "unknown":
                    target_files.append(item)
        
        print(f"📁 整理対象: {len(target_files)}ファイル")
        if target_files:
            print("ファイル一覧:")
            for f in target_files[:5]:  # 最初の5件のみ表示
                print(f"  - {f.name}")
            if len(target_files) > 5:
                print(f"  ... 他{len(target_files)-5}件")
        return
    
    # オートクリーンアップ実行
    results = auto_cleanup(silent=args.silent)
    
    # 終了コード設定
    sys.exit(0 if results["errors"] == 0 else 1)


if __name__ == "__main__":
    main()