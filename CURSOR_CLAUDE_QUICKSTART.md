# 🚀 Cursor ⚡ ClaudeCode クイックスタート

## 即座に開始する方法（3 ステップ）

### ステップ 1: Cursor ターミナルで起動 ⚡

```bash
# Cursor内で以下を実行:
1. Cmd+` でターミナルを開く
2. claude と入力してEnter
3. 初回は認証画面が表示されるので従う
```

### ステップ 2: リアルタイム統合使用 🎯

**基本操作**:

- ファイルを開いてから `claude` 起動 → 自動でコンテキスト共有
- ClaudeCode 内で `> review this file` などと指示
- 変更はリアルタイムで Cursor エディタに反映

**MIRRALISM 専用コマンド**:

```bash
# 日付確認（必須）
> node scripts/getDate.js

# 品質チェック
> check this file for MIRRALISM compliance
> validate all calculations use scripts not AI
```

### ステップ 3: 高度な統合（オプション） 🔧

**MCP 統合**（設定済み）:

- Cursor 設定で `.cursor/mcp.json` が自動的に利用される
- `claude-code-mirralism` サーバーが利用可能
- プロジェクト固有の環境変数が自動設定

## 🎨 実践例

### A. コードレビュー

```bash
# Cursorでファイルを開いた状態で
claude
> review the current file for bugs and improvements
> ensure MIRRALISM quality standards are met
```

### B. リファクタリング

```bash
# 特定のコードを選択してから
claude
> refactor the selected code for better performance
> add proper error handling
```

### C. Git 操作

```bash
claude
> commit these changes with a meaningful message
> create a pull request for this feature
```

## ⚡ 便利なショートカット

| 操作             | ショートカット | 説明                  |
| ---------------- | -------------- | --------------------- |
| ターミナル開く   | `Cmd+\``       | Cursor 統合ターミナル |
| ClaudeCode 起動  | `claude`       | ターミナルで実行      |
| ファイル参照追加 | `Cmd+Option+K` | ClaudeCode 内で使用   |
| 新しいターミナル | `Cmd+Shift+\`` | 複数セッション管理    |

## 🔧 設定済み内容

✅ **ClaudeCode v1.0.15 インストール済み**  
✅ **MIRRALISM 専用プロジェクトメモリ** (`CLAUDE.md`)  
✅ **MCP 統合設定** (`.cursor/mcp.json`)  
✅ **計算システム統合** (`scripts/calculations/`)  
✅ **日付精度システム** (`scripts/getDate.js`)

## 🎯 今すぐ試す

```bash
# Cursor内で実行:
Cmd+`
claude
> Hello! Please review the MIRRALISM project structure.
```

**期待される結果**: ClaudeCode がプロジェクト構造を分析し、MIRRALISM 基準に基づいた洞察を提供

---

**完全ガイド**: `scripts/cursor-claude-integration.md` 参照
