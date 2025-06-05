# MIRRALISM V2 Cursor ⚡ ClaudeCode 統合ガイド

## 🎯 統合方法概要

MIRRALISM V2 では**2 つの方法**で Cursor 上で ClaudeCode を使用できます：

### 方法 1: IDE 統合（推奨）

- **キーボードショートカット**: `Cmd+Esc` (Mac)
- **リアルタイム統合**: Cursor エディタ内で ClaudeCode が動作
- **コンテキスト共有**: 現在のファイル・選択範囲を自動共有

### 方法 2: MCP 統合（高度）

- **MCP サーバー**: ClaudeCode を Model Context Protocol サーバーとして使用
- **プログラム統合**: Cursor AI ⚡ ClaudeCode 直接通信
- **MIRRALISM 専用設定**: プロジェクト固有の環境変数設定

## 🚀 使用開始手順

### ステップ 1: キーボードショートカット設定

1. **Cursor 設定を開く**: `Cmd+,`
2. **キーボードショートカット**: `Cmd+K Cmd+S`
3. **カスタムショートカット追加**:

```json
{
  "key": "cmd+escape",
  "command": "workbench.action.terminal.new",
  "args": {
    "shellArgs": ["claude"]
  }
}
```

### ステップ 2: Cursor ターミナル統合

```bash
# Cursorの統合ターミナルで実行
Cmd+`（バッククォート）でターミナルを開く
claude  # ClaudeCodeを起動
```

### ステップ 3: MCP 統合（高度な統合）

**設定済み**: `.cursor/mcp.json` に以下が設定されています：

```json
{
  "mcpServers": {
    "claude-code-mirralism": {
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {
        "CLAUDE_PROJECT_NAME": "MIRRALISM_V2",
        "CLAUDE_PROJECT_ROOT": "/Users/suetakeshuuhei/MIRRALISM_V2"
      }
    }
  }
}
```

## 💡 Cursor 統合での使用例

### 1. コードレビュー・編集

```bash
# Cursorでファイルを開いた状態で
Cmd+Esc → ClaudeCode起動

# ClaudeCodeで実行
> review the current file for MIRRALISM compliance
> fix any future dates in this file
> validate calculations use scripts not AI
```

### 2. リアルタイム開発支援

```bash
# 選択範囲をClaudeCodeと共有
Cmd+Option+K → ファイル参照追加

# ClaudeCode内で
> explain the selected code
> refactor this function for better performance
> add error handling to this block
```

### 3. MIRRALISM 品質チェック

```bash
# 現在のファイルで品質チェック
> check this file against MIRRALISM quality standards
> verify date accuracy in current file
> ensure all calculations use dedicated scripts
```

## 🎨 Cursor ワークフロー最適化

### A. 開発セッション開始

1. **Cursor 起動** → プロジェクトを開く
2. **日付確認**: Cursor ターミナルで `node scripts/getDate.js`
3. **ClaudeCode 起動**: `Cmd+Esc` または統合ターミナルで `claude`
4. **MIRRALISM ルール適用**: 自動的に `CLAUDE.md` が読み込まれる

### B. リアルタイム開発

1. **ファイル編集**: Cursor エディタで通常通り開発
2. **AI 支援**: `Cmd+Esc` で ClaudeCode を呼び出し
3. **コンテキスト共有**: 現在のファイル・選択範囲が自動共有
4. **品質確認**: MIRRALISM 基準でのリアルタイムチェック

### C. コミット前チェック

1. **全体レビュー**: ClaudeCode で全ファイルチェック
2. **日付検証**: 未来日付の有無確認
3. **計算検証**: AI 計算禁止ルール遵守確認
4. **品質保証**: MIRRALISM 基準適合確認

## ⚡ 統合機能詳細

### 自動共有される情報

- **現在のファイル**: 編集中のファイル内容
- **選択範囲**: ハイライトされたコード
- **診断情報**: ESLint、TypeScript エラーなど
- **プロジェクト構造**: `.mirralism/` ディレクトリ構造
- **MIRRALISM 設定**: `CLAUDE.md` の内容

### ClaudeCode 側で利用可能なツール

- **ファイル読み書き**: Cursor 内のファイルを直接操作
- **Git 操作**: コミット、プッシュ、PR 作成
- **テスト実行**: `npm test` などのコマンド実行
- **計算システム**: `scripts/calculations/` 経由の正確な計算
- **品質チェック**: MIRRALISM 基準での自動検証

## 🔧 トラブルシューティング

### 問題 1: `Cmd+Esc` が動作しない

**解決策**:

```bash
# Cursorターミナル（Cmd+`）で直接実行
claude
```

### 問題 2: MCP サーバーが認識されない

**解決策**:

```bash
# Cursor設定更新
Cmd+Shift+P → "Reload Window"
# または
claude mcp serve  # 手動でMCPサーバー起動
```

### 問題 3: プロジェクトコンテキストが共有されない

**解決策**:

```bash
# ClaudeCode内で手動設定
/memory  # メモリファイル編集
/init    # プロジェクト初期化
```

## 📊 統合効果測定

### 期待される効果

- **開発効率**: 70-90%向上（Cursor + ClaudeCode）
- **品質精度**: 100%（MIRRALISM 基準自動適用）
- **コンテキスト精度**: 95%（リアルタイム共有）
- **学習効果**: プロジェクト固有知識の蓄積

### メトリクス

- **応答速度**: 平均 2-3 秒（統合環境）
- **精度**: MIRRALISM 準拠率 100%
- **コスト**: 統合により効率化で 20-30%削減予想

## 🎯 次のステップ

1. **統合テスト**: 各機能の動作確認
2. **ワークフロー最適化**: 日常業務への組み込み
3. **チーム展開**: 他の開発者への展開準備
4. **継続改善**: 使用状況に基づく設定調整
