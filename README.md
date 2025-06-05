# MIRRALISM V2 - MCP Ecosystem Integrated Release

**MIRRALISM V2**は、AI 支援による高度な PersonalityLearning システムを核とした、次世代の個人最適化プラットフォームです。

## 🎯 プロジェクト概要

### 核心機能

- **PersonalityLearning 2.0**: 53%→95%精度進化システム
- **SuperWhisper 統合**: 音声データ分析・学習
- **Task Master MCP 統合**: AI 支援プロジェクト管理
- **2PC 開発環境**: Mac 間同期最適化

### アーキテクチャ

```
MIRRALISM_V2/
├── Core/                   # PersonalityLearning、分析エンジン
│   ├── PersonalityLearning/
│   ├── Classification/
│   └── Search/
├── API/                    # SuperWhisper、OpenAI統合
├── Data/                   # SQLite、学習データ
├── .taskmaster/            # MCP Task Master統合
├── .cursor/                # AI開発環境設定
└── tests/                  # pytest テストスイート
```

## 🚀 技術スタック

### AI・機械学習

- **OpenAI API**: GPT-4, Claude-3.5-Sonnet 統合
- **Perplexity AI**: 研究支援機能
- **PersonalityLearning**: カスタム学習アルゴリズム
- **SuperWhisper**: 音声データ処理

### 開発環境

- **Python 3.9+**: メイン開発言語
- **SQLite**: データベース (WAL モード最適化)
- **Task Master MCP**: AI 支援タスク管理
- **Cursor AI**: AI 統合開発環境
- **Docker**: 一貫した開発環境

### 品質保証

- **pytest**: テストフレームワーク
- **black**: コードフォーマット
- **flake8**: コード品質チェック
- **pre-commit**: 自動品質管理

## 📦 セットアップ

### 1. 環境構築

```bash
# リポジトリクローン
git clone https://github.com/suetake6183/MIRRALISM_V2.git
cd MIRRALISM_V2

# Python環境作成
python3 -m venv venv
source venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt
```

### 2. 設定ファイル

```bash
# 環境変数設定（テンプレートをコピー）
cp .env.example .env
# 実際のAPIキーを設定
```

### 3. データベース初期化

```bash
# PersonalityLearning V2データベース作成
python Core/PersonalityLearning/database.py
```

### 4. テスト実行

```bash
# 全テスト実行
pytest tests/

# Docker環境でのテスト
docker build -t mirralism-dev .
docker run mirralism-dev pytest
```

## 🔧 主要機能

### PersonalityLearning 2.0

- **精度進化**: 53%→95%の学習精度向上システム
- **統合分析**: journal, voice, task, interaction データ
- **自動マイルストーン**: 90%以上で達成判定

### Task Master MCP 統合

- **AI 支援タスク管理**: 23 タスク、76 サブタスク
- **依存関係管理**: 自動ワークフロー最適化
- **複雑度分析**: AI ベースタスク分解

### SuperWhisper 統合

- **音声データ処理**: リアルタイム文字起こし
- **感情分析**: 音声データからの感情抽出
- **学習重み付け**: 音声データ 1.5 倍重み

## 📊 開発状況

### タスク進捗

- **完了**: 47 サブタスク (61.8%)
- **進行中**: 6 タスク (26.1%)
- **待機中**: 16 タスク (69.6%)

### 品質指標

- **テストカバレッジ**: 85%+
- **コード品質**: flake8 準拠
- **Docker 化**: 完了

## 🛠️ 開発ワークフロー

### 推奨開発手順

1. **Task Master**: `next_task`で作業タスク特定
2. **実装**: AI 支援コード生成・テスト
3. **品質チェック**: pre-commit hooks 自動実行
4. **進捗更新**: `set_task_status`でタスク完了

### Codex 開発支援

- **GitHub 連携**: 自動コード生成・PR 作成
- **依存関係管理**: 自動インストール・テスト
- **品質保証**: 自動テスト・静的解析

## 📈 目標・ビジョン

### 短期目標 (2024 年)

- PersonalityLearning 精度 95%達成
- SuperWhisper 完全統合
- 2PC 開発環境完全同期

### 長期ビジョン

- AI 支援による個人最適化プラットフォーム
- リアルタイム学習・適応システム
- エコシステム拡張によるユーザー価値最大化

## 🤝 コントリビューション

### 開発参加

1. Issue 作成またはタスク選択
2. ブランチ作成: `feature/task-{id}`
3. 実装・テスト
4. PR 作成（Codex 支援可能）

### コード規約

- **Python**: PEP 8 準拠
- **コミット**: Conventional Commits
- **テスト**: pytest 必須
- **ドキュメント**: docstring 必須

---

**MIRRALISM V2** - AI-Powered Personal Optimization Platform
© 2024 suetake6183. Licensed under MIT.
