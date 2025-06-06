#!/bin/bash
# ClaudeCode自動承認システム セットアップスクリプト
# 手動承認を大幅削減して開発効率を向上

echo "🤖 ClaudeCode自動承認システム セットアップ"
echo "============================================"

# プロジェクトルート確認
PROJECT_ROOT="/Users/suetakeshuuhei/MIRRALISM_V2"
cd "$PROJECT_ROOT" || {
    echo "❌ プロジェクトルートが見つかりません: $PROJECT_ROOT"
    exit 1
}

echo "📁 プロジェクトルート: $PROJECT_ROOT"

# 必要なディレクトリ作成
echo "📂 必要なディレクトリを作成中..."
mkdir -p .mirralism/logs
mkdir -p .mirralism/config
mkdir -p .mirralism/stats

# 自動承認システムを有効化
echo "🔄 自動承認システムを有効化中..."
python3 scripts/claude_auto_approver.py --enable

# 環境変数設定
echo "🌍 環境変数を設定中..."
source .mirralism/claude_env.sh

# 設定確認
echo "📊 設定状況を確認中..."
python3 scripts/claude_auto_approver.py --status

# CLAUDE.mdに設定追加
echo "📝 CLAUDE.mdに自動承認設定を追加中..."

# CLAUDE.mdの自動承認セクションを追加
if ! grep -q "# ClaudeCode自動承認" CLAUDE.md; then
    cat >> CLAUDE.md << 'EOF'

# ClaudeCode自動承認設定

## 🤖 自動承認システム

ClaudeCodeの手動承認を大幅削減するため、以下の操作は自動承認されます：

### ✅ 自動承認対象
- **ファイル操作**: 読み込み、編集、作成、移動
- **コード操作**: フォーマット、リファクタリング、コメント追加
- **Git操作**: add, commit, status, diff, log
- **ビルド操作**: テスト実行、リント、依存関係インストール
- **ドキュメント**: README更新、ドキュメント作成

### ⚠️ 手動確認が必要
- システム設定変更
- データベース操作
- 本番環境関連
- 一括ファイル削除
- セキュリティ設定変更

### 🔧 設定変更
```bash
# 自動承認を有効化
python3 scripts/claude_auto_approver.py --enable

# 自動承認を無効化  
python3 scripts/claude_auto_approver.py --disable

# 状況確認
python3 scripts/claude_auto_approver.py --status
```

### 📊 使用統計
自動承認の使用統計は `.mirralism/claude_auto_approval.json` で確認できます。

EOF
    echo "✅ CLAUDE.mdに自動承認設定を追加しました"
else
    echo "ℹ️ CLAUDE.mdに自動承認設定は既に存在します"
fi

# 完了メッセージ
echo ""
echo "🎉 ClaudeCode自動承認システムのセットアップが完了しました！"
echo ""
echo "📋 設定内容:"
echo "   ✅ 自動承認: 有効"
echo "   ✅ ファイル操作: 自動"
echo "   ✅ Git操作: 自動"
echo "   ✅ コード品質: 自動"
echo "   ⚠️ 高リスク操作: 手動確認"
echo ""
echo "🚀 これで ClaudeCode での作業がずっと楽になります！"
echo "   毎回「Yes」と答える必要がなくなりました。"
echo ""
echo "💡 設定を変更したい場合:"
echo "   python3 scripts/claude_auto_approver.py --help"
echo ""