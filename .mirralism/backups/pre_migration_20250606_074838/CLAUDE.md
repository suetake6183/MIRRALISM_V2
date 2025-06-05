# MIRRALISM V2 プロジェクトガイド

## 🎯 プロジェクト概要

MIRRALISM V2 は、パーソナリティ学習と価値創造戦略の統合プラットフォームです。

**核心原則**:

- 技術的完璧性
- 段階的品質保証
- 日付精度システム（必須）
- AI 計算禁止（必須）

## 📋 必須ルール遵守

### 1. 日付システム

```bash
# 必ず最初に実行
node scripts/getDate.js
```

### 2. AI 計算禁止

- 全ての計算は `scripts/calculations/` のスクリプトを使用
- AI による直接計算は禁止

```bash
# 例：基本計算
node scripts/calculations/basic_math.js add 480 1027

# 例：日付計算
node scripts/calculations/date_calc.js period 2025-06-05 2025-08-05

# 例：ROI計算
node scripts/calculations/roi_calc.js roi 480 1027
```

## 🏗️ プロジェクト構造

```
.mirralism/          # コア設定・レポート
.cursor/rules/       # Cursor用ルール
scripts/             # 実行スクリプト
├── calculations/    # 計算システム
└── getDate.js      # 日付確認
```

## 💻 開発ワークフロー

1. **開始前**: `node scripts/getDate.js` で現在時刻確認
2. **計算時**: 専用スクリプト使用（AI 計算禁止）
3. **コミット前**: 日付間違いチェック
4. **品質確認**: 段階的品質保証システム適用

## 🔧 開発環境

- **Node.js**: v22.14.0
- **Git**: 2.39.5
- **OS**: macOS 15.5
- **プロジェクトルート**: `/Users/suetakeshuuhei/MIRRALISM_V2`

## 📊 品質指標

- 日付精度: 100%
- 計算精度: 100%（プログラム実行）
- コード品質: MIRRALISM 基準準拠

## 🚨 注意事項

- 未来日付の使用禁止
- AI 計算の使用禁止
- `.mirralism/` ディレクトリの重要性認識
- SSOT（Single Source of Truth）原則遵守
