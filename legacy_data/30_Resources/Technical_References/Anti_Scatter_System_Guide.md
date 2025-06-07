# 🛡️ 散在防止システム使用方法

## 🎯 機能概要

このシステムは以下の機能を提供します：

### 1. リアルタイム監視
- ファイル・ディレクトリ作成の即座検出
- 違反パターンの自動識別
- 緊急移動処理の実行

### 2. 違反パターン検出
- ルート直下のファイル作成
- 禁止ディレクトリ (90_*, System*, Report*)
- 計画・レポート関連の不適切配置

### 3. 自動修正
- 40_Archive/Emergency_Cleanup/ への安全移動
- 移動記録の自動作成
- ログによる完全追跡

## 🚀 使用方法

### 基本実行
```bash
python anti_scatter_system.py
```

### バックグラウンド実行
```bash
python anti_scatter_system.py &
```

### システム起動時自動実行（推奨）
launchd設定ファイルをUser/Library/LaunchAgents/に配置

## 📋 監視ルール

### ✅ 許可される場所
- 40_Archive/配下の全ディレクトリ
- 30_Resources/配下
- 50_Templates/配下
- README.md (ルート直下のみ)

### ❌ 禁止される場所
- SecondBrain/ 直下 (README.md以外)
- 90_* で始まるディレクトリ
- System* で始まるディレクトリ
- Report* で始まるディレクトリ

### 🔍 検出対象ファイル
- *.md (マークダウンファイル)
- *計画*, *レポート* (日本語)
- *plan*, *report* (英語)

## 🆘 緊急時対応

### 誤移動の場合
1. 40_Archive/Emergency_Cleanup/ 内を確認
2. MOVE_RECORD_*.md で移動理由確認
3. 必要に応じて適切な場所に手動移動

### システム停止
```bash
# プロセス確認
ps aux | grep anti_scatter

# 停止
kill [プロセスID]
```

---
*自動生成ガイド - 2025年6月1日*
