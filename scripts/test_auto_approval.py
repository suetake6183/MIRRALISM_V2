#!/usr/bin/env python3
"""
自動承認システムテスト
=====================

強化された自動承認システムの動作確認用テストスクリプト
"""

import sys
from pathlib import Path

# claude_auto_approver.pyをインポート
sys.path.append(str(Path(__file__).parent))
from claude_auto_approver import ClaudeAutoApprover

def test_auto_approval():
    """自動承認システムのテスト"""
    
    approver = ClaudeAutoApprover()
    
    # テストケース
    test_cases = [
        ("node scripts/getDate.js", "MIRRALISM必須の日付確認"),
        ("read file operation", "ファイル読み込み"),
        ("file search with grep", "ファイル検索"),
        ("browse files in directory", "ディレクトリブラウズ"),
        ("git status check", "Git状態確認"),
        ("directory listing", "ディレクトリ一覧"),
        ("mirralism calculation script", "MIRRALISM計算"),
        ("date check", "日付確認"),
        ("search operation", "検索操作"),
        ("view file contents", "ファイル表示")
    ]
    
    print("🧪 自動承認システムテスト")
    print("=" * 50)
    
    auto_approved = 0
    manual_required = 0
    
    for operation, description in test_cases:
        should_approve, reason = approver.should_auto_approve(operation, description)
        
        status = "✅ 自動承認" if should_approve else "⚠️ 手動確認"
        print(f"{status}: {operation}")
        print(f"   理由: {reason}")
        print(f"   詳細: {description}")
        print()
        
        if should_approve:
            auto_approved += 1
        else:
            manual_required += 1
    
    print("📊 テスト結果サマリー")
    print(f"自動承認: {auto_approved}件")
    print(f"手動確認: {manual_required}件")
    print(f"自動承認率: {auto_approved / len(test_cases) * 100:.1f}%")

if __name__ == "__main__":
    test_auto_approval()