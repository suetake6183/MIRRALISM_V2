# 🚀 Cursor で ClaudeCode をチャット形式で使う方法

> **2025 年 6 月 6 日（金）7 時 37 分 更新** - MIRRALISM 品質基準準拠

## 🎯 目標

**ターミナルを使わずに、今の Cursor チャットのような画面で ClaudeCode と直接会話する**

## 📋 設定手順（3 分で完了）

### ステップ 1: ClaudeCode 拡張機能を手動インストール

```bash
# まず、ClaudeCodeがローカルインストールされているか確認
claude

# ClaudeCodeセッション内で実行
/doctor
```

**期待される結果:**

```
You are running Claude Code from your local installation (~/.claude/local).
```

### ステップ 2: Cursor 拡張機能インストール

```bash
# ターミナルで実行（ClaudeCodeセッションを終了してから）
cursor --install-extension ~/.claude/local/node_modules/@anthropic-ai/claude-code/vendor/claude-code.vsix
```

**期待される結果:**

```
Extension 'claude-code.vsix' was successfully installed.
```

### ステップ 3: もしくは簡単ドラッグ&ドロップ方式

1. **ファイルを見つける:**

   ```bash
   open ~/.claude/local/node_modules/@anthropic-ai/claude-code/vendor/
   ```

2. **Cursor に直接ドロップ:**
   - `claude-code.vsix` ファイルを見つける
   - Cursor の拡張機能パネルに**ドラッグ&ドロップ**

## 🎉 使用方法

### 方法 1: キーボードショートカット

```
⌘ + Esc (Mac) / Ctrl + Esc (Windows)
```

- **今のチャット画面のような**ClaudeCode インターフェースが開きます！

### 方法 2: Cursor のチャット内から

1. Cursor のチャットパネルを開く
2. **ClaudeCode ボタン**をクリック
3. **直接対話開始**

## ✨ 利用可能な機能

### 🔄 **リアルタイム統合**

- **現在のファイル/選択範囲**が自動共有
- **Cursor のエラー診断**が自動共有
- **コード変更**が Cursor 内で直接表示

### 🎯 **ショートカット**

- `⌘ + Option + K` (Mac): ファイル参照挿入
- **Cursor 内 diff 表示**: 変更が Cursor エディタ内で直接表示

### 💬 **チャット体験**

- **今のチャットと同じような**対話形式
- **ファイル編集提案**がインライン表示
- **プロジェクト全体の理解**

## 🔧 トラブルシューティング

### 問題 1: 拡張機能がインストールされない

**解決策:**

```bash
# ClaudeCodeを一度ローカルに移行
claude
/migrate-installer
```

### 問題 2: 特定の Cursor プロファイルで使いたい

**解決策:**

```bash
cursor --install-extension ~/.claude/local/node_modules/@anthropic-ai/claude-code/vendor/claude-code.vsix --profile "プロファイル名"
```

### 問題 3: `cursor`コマンドが見つからない

**解決策:**

1. Cursor を開く
2. `⌘ + Shift + P` → "Install 'cursor' command in PATH"を実行

## 🎯 **完成！これで準備完了**

**今後の使い方:**

1. Cursor で開発作業
2. `⌘ + Esc`で ClaudeCode チャット起動
3. **今のチャットのような画面**で ClaudeCode と対話
4. コード提案を直接 Cursor で確認・適用

## 🔥 **さらに高度な使い方**

### GitHub 統合

```bash
# ClaudeCodeセッション内で
/install-github-app
```

- PR レビューへの自動対応
- CI エラー修正
- コード修正提案

### バックグラウンドタスク

- **GitHub Actions**での自動実行
- **長時間実行タスク**の継続実行

## 📊 **コスト管理**

### リアルタイム使用量確認

Cursor 拡張機能をインストールすることで、**ステータスバーに今日の使用料金**が表示されます：

- 30 秒ごとに自動更新
- クリックで過去 7 日間の詳細表示

---

## 🎉 **まとめ**

これで**Cursor のチャット画面と同じような環境**で ClaudeCode が使えます！

**主な違い:**

- ✅ **ターミナル不要**
- ✅ **チャット形式対話**
- ✅ **リアルタイムファイル共有**
- ✅ **インラインコード表示**
- ✅ **Cursor 完全統合**

**次のステップ:**

1. `⌘ + Esc`を試してみる
2. ファイルを開いた状態で ClaudeCode と対話
3. コード提案を Cursor 内で確認

お疲れ様でした！🎊
