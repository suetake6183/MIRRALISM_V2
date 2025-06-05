# MIRRALISM V2 ClaudeCode 使用ガイド

## 🚀 起動方法

```bash
# プロジェクトルートで実行
claude
```

初回起動時に Anthropic 認証が必要です（ブラウザが自動で開きます）。

## 💡 基本的な使用方法

### 日常的なタスク

```bash
# コードベースの理解
> how does our authentication system work?

# ファイル編集
> add input validation to the signup form

# Git操作
> commit my changes
> create a pr

# テスト実行
> run tests for the auth module and fix failures
```

### MIRRALISM ルール遵守

```bash
# 日付確認（常に最初に実行）
> node scripts/getDate.js

# 計算実行（AI計算禁止ルール）
> node scripts/calculations/basic_math.js add 480 1027
> node scripts/calculations/date_calc.js period 2025-06-05 2025-08-05
```

## 🔧 便利なスラッシュコマンド

| コマンド  | 説明               |
| --------- | ------------------ |
| `/init`   | プロジェクト初期化 |
| `/clear`  | 会話履歴クリア     |
| `/cost`   | トークン使用量確認 |
| `/config` | 設定変更           |
| `/memory` | メモリファイル編集 |
| `/bug`    | バグレポート送信   |

## 🎯 MIRRALISM 特化の使用例

### 1. 品質チェック

```bash
> check for any future dates in the codebase
> validate that all calculations use scripts instead of AI
```

### 2. 開発ワークフロー

```bash
> review the .mirralism directory structure
> check compliance with MIRRALISM quality standards
```

### 3. 計算検証

```bash
> verify all ROI calculations in the project
> check date accuracy across all files
```

## ⚠️ 注意事項

1. **AI 計算禁止**: 必ず `scripts/calculations/` を使用
2. **日付確認**: セッション開始時に `getDate.js` 実行
3. **メモリ活用**: `CLAUDE.md` でプロジェクト知識を蓄積
4. **セキュリティ**: プロジェクトフォルダを信頼して実行

## 📊 コスト管理

- 平均日次コスト: 約 6 ドル
- `/cost` で現在の使用量確認
- 会話履歴は適宜 `/clear` でリセット

## 🔗 関連ファイル

- `CLAUDE.md`: プロジェクトメモリ
- `.cursor/rules/`: Cursor 統合ルール
- `scripts/calculations/`: 計算システム
- `scripts/getDate.js`: 日付確認システム
