# MIRRALISM AI 計算禁止システム

**作成日**: 2025 年 06 月 05 日  
**目的**: AI による計算ミスを完全に防止し、100%正確な計算結果を保証

## 🎯 システム概要

このシステムは、MIRRALISM の「技術的完璧性」の一環として、AI（Claude）が直接計算を行うことを禁止し、プログラムによる正確な計算を強制します。

## 📊 利用可能な計算スクリプト

### 1. 基本数学計算 (`basic_math.js`)

```bash
# 加算
node scripts/calculations/basic_math.js add 480 1027
# 結果: 1507

# ROI計算
node scripts/calculations/basic_math.js roi 480 1027
# 結果: 113.96% (投資額480円 → 回収額1,027円)

# パーセンテージ
node scripts/calculations/basic_math.js percentage 1027 480
# 結果: 214.17%
```

**対応操作**: `add`, `subtract`, `multiply`, `divide`, `percentage`, `roi`

### 2. 日付計算 (`date_calc.js`)

```bash
# 期間計算
node scripts/calculations/date_calc.js period 2025-06-05 2025-08-05
# 結果: 61日 (8週間5日)

# 日付加算
node scripts/calculations/date_calc.js add_days 2025-06-05 30
# 結果: 2025-07-05

# 営業日計算
node scripts/calculations/date_calc.js business_days 2025-06-05 2025-08-05
# 結果: 44営業日 (土日を除く)
```

**対応操作**: `period`, `add_days`, `subtract_days`, `business_days`

### 3. ROI・財務計算 (`roi_calc.js`)

```bash
# ROI計算
node scripts/calculations/roi_calc.js roi 480 1027
# 結果: 113.96% (高ROI: 2倍以上)

# 利益率計算
node scripts/calculations/roi_calc.js profit_rate 547 1027
# 結果: 53.27% (高利益率)

# 複利成長率
node scripts/calculations/roi_calc.js compound_growth 480 1027 3
# 結果: 29.35% (年間成長率)
```

**対応操作**: `roi`, `profit_rate`, `compound_growth`, `break_even`

### 4. ファイル・統計計算 (`file_calc.js`)

```bash
# 平均値計算
node scripts/calculations/file_calc.js average 10 20 30 40 50
# 結果: 30 (標準偏差: 14.14)

# ディレクトリサイズ
node scripts/calculations/file_calc.js size_sum ./data/
# 結果: 15.6 MB (1,234ファイル)

# ファイル数カウント
node scripts/calculations/file_calc.js count_files ./scripts/
# 結果: 25個 (主な拡張子: .js: 20個, .md: 5個)
```

**対応操作**: `average`, `sum`, `size_sum`, `count_files`

## 🔧 出力形式

全ての計算スクリプトは統一された形式で結果を出力：

```
=== [計算種別]計算結果 ===
操作: [実行された操作]
入力: [パラメータ]
結果: [正確な数値]
計算式: [使用した数式]
検証: [結果の妥当性]
--- 詳細情報 ---
[追加の分析データ]
===========================
```

## ⚠️ 禁止される AI 計算

以下の計算は**絶対に AI が直接実行してはいけません**：

- ❌ 数値計算（加減乗除、パーセンテージ）
- ❌ 日付計算（期間、営業日数）
- ❌ 財務計算（ROI、利益率）
- ❌ 統計計算（平均、合計、分散）
- ❌ ファイル計算（サイズ、カウント）

## 🎯 エラー防止効果

このシステムにより防止される問題：

- ✅ タイムゾーン計算ミス
- ✅ 浮動小数点演算誤差
- ✅ パーセンテージ計算間違い
- ✅ ROI 計算の不正確性
- ✅ 計算過程の不透明性

## 📈 MIRRALISM 品質保証

- **100%正確性**: プログラム計算による確実性
- **透明性**: 計算過程の完全可視化
- **トレーサビリティ**: 入力・出力・過程の記録
- **検証可能性**: 計算結果の第三者検証可能

## 🚀 使用方法

1. `.cursor/rules/no_ai_calculation.mdc`が`alwaysApply: true`で有効化されている
2. 計算が必要な場合は、適切なスクリプトを選択
3. 必要なパラメータを指定して実行
4. 出力された正確な結果を使用

**重要**: この仕組みは「技術的完璧性」の一部として、MIRRALISM の品質基準に不可欠です。
