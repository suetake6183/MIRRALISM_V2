---
title: "mcp setup guide"
created: "2025-05-26"
type: "document"
status: "active"
---

# 既存MCPユーザー向け：Claude 4 MCPコネクタ移行・設定手順書

## 前提条件

- 既にMCPの設定経験がある
- Claude Desktop で従来のMCPサーバーを使用している
- Claude 4（Opus 4 / Sonnet 4）にアップグレード済み、または予定

---

## Step 1: 現在の設定状況の確認

### 1-1. 既存のMCP設定ファイルの確認

**操作手順：**
1. 既存の `claude_desktop_config.json` ファイルを開く
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. 現在の設定内容をメモまたはバックアップとして保存

**典型的な既存設定例：**
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@suekou/mcp-notion-server"],
      "env": {
        "NOTION_API_TOKEN": "your-token"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username"],
      "env": {}
    }
  }
}
```

### 1-2. Claude 4 バージョンの確認

**確認手順：**
1. Claude Desktop のメニューから「About Claude」を選択
2. Claude 4（Opus 4 または Sonnet 4）になっているか確認
3. 古いバージョンの場合は最新版にアップデート

**重要：** Claude 4の新機能を活用するには最新版が必要

---

## Step 2: Claude 4 新機能の理解

### 2-1. 従来MCPとの主な違い

**新機能一覧：**
- **並列ツール実行**: 複数のMCPサーバーを同時に使用可能
- **拡張思考機能**: ツール使用中の深い推論
- **スコープ管理**: local、project、user の3段階管理
- **API統合**: プログラマティックな管理機能

### 2-2. 既存設定の互換性

**良いニュース：**
既存の `claude_desktop_config.json` 設定は **そのまま動作** します

**ただし以下の恩恵を受けるには設定更新が推奨：**
- 並列処理の最適化
- エラーハンドリングの改善
- 新しい管理機能の活用

---

## Step 3: 設定の最適化（既存ユーザー向け）

### 3-1. 並列処理対応の設定確認

**現在の設定がこの形式の場合：**
```json
{
  "mcpServers": {
    "notion": { ... },
    "filesystem": { ... }
  }
}
```

**そのまま使用可能ですが、以下の追加設定で最適化：**

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@suekou/mcp-notion-server"],
      "env": {
        "NOTION_API_TOKEN": "your-token"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username"],
      "env": {}
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key"
      }
    }
  }
}
```

### 3-2. 新しいサーバーの追加（Claude 4 推奨）

**Claude 4 で特に効果的なサーバー：**

**1. GitHub サーバー（コード管理）：**
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "your-github-token"
  }
}
```

**2. PostgreSQL サーバー（データベース連携）：**
```json
"postgres": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-postgres"],
  "env": {
    "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/db"
  }
}
```

---

## Step 4: Claude Code の活用（新機能）

### 4-1. Claude Code のインストール

**既存ユーザーで Claude Code 未使用の場合：**

1. ターミナルで以下のコマンドを実行：
   ```bash
   npm install -g @anthropic-ai/claude-cli
   ```

2. インストール確認：
   ```bash
   claude --version
   ```

### 4-2. Claude Code での MCP 管理

**新しい管理コマンド：**

```bash
# 現在のMCPサーバー一覧確認
claude mcp list

# 新しいサーバーの追加
claude mcp add github-server /path/to/github-server

# スコープを指定してサーバー追加
claude mcp add team-notion -s project /path/to/notion-server

# サーバーの削除
claude mcp remove server-name
```

### 4-3. スコープ管理の活用

**3つのスコープの使い分け：**

**Local スコープ（個人用）：**
```bash
claude mcp add my-personal-server -s local /path/to/server
```

**Project スコープ（プロジェクト共有）：**
```bash
claude mcp add team-tools -s project /path/to/server
```

**User スコープ（全プロジェクト共通）：**
```bash
claude mcp add global-utils -s user /path/to/server
```

---

## Step 5: 設定の更新と最適化

### 5-1. 既存設定のバックアップ

**操作手順：**
1. 現在の `claude_desktop_config.json` をコピー
2. `claude_desktop_config_backup.json` として保存
3. 元ファイルを編集

### 5-2. Claude 4 最適化設定の適用

**既存設定を以下のように更新：**

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@suekou/mcp-notion-server"],
      "env": {
        "NOTION_API_TOKEN": "your-token",
        "NOTION_MARKDOWN_CONVERSION": "true"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username"],
      "env": {
        "FILESYSTEM_WATCH_MODE": "true"
      }
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key"
      }
    }
  }
}
```

**新しい環境変数の説明：**
- `NOTION_MARKDOWN_CONVERSION`: レスポンスのMarkdown変換でトークン消費を削減
- `FILESYSTEM_WATCH_MODE`: ファイル変更の自動検知

---

## Step 6: 新機能のテスト

### 6-1. 並列処理のテスト

**テスト手順：**
1. Claude Desktop を再起動
2. 以下のような複数タスクを同時に依頼：

```
Notionの今日のタスクを確認して、同時にホームディレクトリの最新ファイルも表示してください。また、今日の天気も教えてください。
```

**期待される動作：**
- 複数のMCPサーバーが並列で動作
- 従来よりも高速な応答
- 結果の統合表示

### 6-2. 拡張思考機能のテスト

**テスト手順：**
複雑なタスクを依頼して拡張思考機能を確認：

```
私のNotionタスクリストとローカルファイルの状況を分析して、今週の作業優先順位を提案してください。必要に応じて最新情報を検索してください。
```

**期待される動作：**
- 段階的な思考プロセスの表示
- ツール使用と推論の交互実行
- より詳細な分析結果

---

## Step 7: トラブルシューティング（既存ユーザー向け）

### 7-1. 既存設定で動かない場合

**問題1: 従来のサーバーが "disconnected" 状態**
- **対処法**: サーバーの最新版確認とアップデート
  ```bash
  npm update -g @suekou/mcp-notion-server
  ```

**問題2: 並列処理が動作しない**
- **対処法**: Claude Desktop の完全再起動と設定再読み込み

**問題3: 新機能が利用できない**
- **対処法**: Claude 4 へのアップグレード確認

### 7-2. パフォーマンス問題

**レスポンスが遅い場合：**
1. 不要なMCPサーバーを一時的に無効化
2. タイムアウト設定の調整：
   ```json
   "env": {
     "MCP_TIMEOUT": "30000"
   }
   ```

### 7-3. ログの確認方法

**詳細ログの確認：**
```bash
# Claude Code でのログ確認
claude mcp logs

# または従来の方法
# macOS: ~/Library/Logs/Claude/
# Windows: %APPDATA%\Claude\logs\
```

---

## Step 8: 移行後の最適化

### 8-1. 新しいワークフローの構築

**Claude 4 の新機能を活用した例：**

**1. 並列データ分析：**
```
Notionのプロジェクトデータ、GitHubのコミット履歴、ローカルの作業ファイルを同時に分析して、プロジェクトの進捗レポートを作成してください。
```

**2. 統合的な情報管理：**
```
最新のニュースを検索して、関連する情報をNotionデータベースに追加し、ローカルの研究ファイルも更新してください。
```

### 8-2. チーム向け設定の共有

**プロジェクトスコープでのチーム設定：**
1. `.mcp.json` ファイルをプロジェクトルートに作成
2. チーム共通のMCPサーバー設定を記述
3. バージョン管理システムにコミット

**例：**
```json
{
  "mcpServers": {
    "team-notion": {
      "command": "npx",
      "args": ["-y", "@suekou/mcp-notion-server"],
      "env": {
        "NOTION_API_TOKEN": "${NOTION_TEAM_TOKEN}"
      }
    }
  }
}
```

---

## 移行完了チェックリスト

- [ ] 既存設定のバックアップ完了
- [ ] Claude 4 への更新確認
- [ ] 既存MCPサーバーが正常動作することを確認
- [ ] 新しい環境変数の追加完了
- [ ] 並列処理のテスト成功
- [ ] 拡張思考機能の動作確認
- [ ] Claude Code のインストール・設定完了
- [ ] 新しいワークフローのテスト実行

すべてにチェックが入れば、Claude 4 MCPコネクタへの移行は完了です！

**次のステップ：**
Claude 4 の新機能を活用した高度なワークフローの構築に進んでください。