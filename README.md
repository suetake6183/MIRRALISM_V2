# MIRRALISM V2 🚀

**音声ファイル知的管理システム**の第 2 世代プロトタイプ

---

## 🎯 プロジェクト概要

MIRRALISM V2 は、音声ファイルの自動分類・管理・検索システムです。

### ✨ 主要機能

- **🔍 高精度分類**: V1 の 53%→95%精度向上
- **📁 厳選管理**: 500 ファイル厳選・99%削減
- **⚡ 瞬時検索**: 5 秒以内検索目標
- **🤖 AI 統合**: 複数 AI Provider 対応

### 🏗️ システム構成

```
MIRRALISM_V2/
├── 🎯 Core/                     # コアエンジン
├── 🔌 API/                      # 外部連携
├── 🧪 Prototype/                # プロトタイプ実装
├── 📊 Data/                     # データ管理
├── 🔧 scripts/                  # ユーティリティ
└── 📝 .taskmaster/              # タスク管理
```

### 📈 技術スタック

- **言語**: Python 3.9+
- **AI**: OpenAI, Anthropic, Perplexity
- **データベース**: SQLite, JSON
- **品質管理**: black, isort, pytest
- **CI/CD**: GitHub Actions
- **タスク管理**: Task Master AI

### 🚀 開発ステータス

```yaml
開発段階: Phase 1 プロトタイプ
進捗状況: 基本機能実装完了
品質ゲート: GitHub Actions準拠
AI統合: ChatGPT Codex 準備完了
リポジトリ: V2完全分離
最終更新: 2025-06-05 # GitHub Actions品質ゲート最適化
```

### 🎮 クイックスタート

1. **環境セットアップ**

   ```bash
   pip install -r requirements.txt
   cp .env.example .env  # API キー設定
   ```

2. **プロトタイプ実行**

   ```bash
   python Prototype/mirralism_prototype.py
   ```

3. **タスク管理**
   ```bash
   # Task Master初期化
   task-master init
   # タスク確認
   task-master list
   ```

### 📋 開発ワークフロー

- **MCP Server**: Cursor/AI 統合
- **GitHub Actions**: 品質ゲート
- **Task Master**: 開発管理
- **ChatGPT Codex**: AI 支援開発

### 🏆 V1 からの改善点

| 項目         | V1       | V2           | 向上率   |
| ------------ | -------- | ------------ | -------- |
| 分類精度     | 53%      | 95%          | 79%↑     |
| ファイル管理 | 手動     | 自動 99%削減 | 大幅改善 |
| 検索速度     | 制限なし | 5 秒以内     | 大幅改善 |
| AI 統合      | 限定的   | 完全統合     | 大幅改善 |

### 🔗 関連プロジェクト

- [MIRRALISM V1](https://github.com/suetake6183/MIRRALISM) - 初代システム
- [Task Master AI](https://www.npmjs.com/package/task-master-ai) - AI 開発管理

---

_MIRRALISM V2 - 知的音声ファイル管理の未来_
