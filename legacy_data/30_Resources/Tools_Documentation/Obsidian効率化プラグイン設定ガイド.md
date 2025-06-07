---
author: 末武修平
category: ツール設定
created: '2025-05-23'
priority: high
source_file: 00_Inbox/RawNotes/QuickAddプラグインとAuto Note Moverプラグインについて.md
status: processed
tags:
- tech/tool
- plugins
- quickadd
- auto-note
- automation
- efficiency
title: Obsidian効率化プラグイン設定ガイド：QuickAdd & Auto Note Mover
type: configuration_guide
updated: '2025-05-23'
---

# Obsidian 効率化プラグイン設定ガイド：QuickAdd & Auto Note Mover

## 概要

QuickAdd と Auto Note Mover プラグインを活用することで、ノート作成から自動整理まで、SecondBrain ワークフローの大幅な効率化を実現します。定型作業の自動化により、思考に集中できる環境を構築します。

## QuickAdd プラグイン活用法

### 基本機能

- **Template**: 定型ノートの瞬時作成
- **Capture**: 情報の迅速キャプチャ
- **Macro**: 複数操作の一括実行

### 実践的設定例

#### 1. アイデアキャプチャ（Capture 設定）

**テンプレート準備**（`30_Resources/Templates/IdeaTemplate.md`）:

```markdown
---
created: { { DATE:YYYY-MM-DD HH:mm } }
tags: [idea, inbox_item]
---

# アイデア: {{VALUE:アイデアのタイトル}}

{{VALUE:詳細}}
```

**QuickAdd 設定手順**:

1. `設定` > `QuickAdd` で新規 Choice 追加
2. 名前: `Capture Idea to Inbox`
3. タイプ: `Capture`を選択
4. 詳細設定（⚙️）:
   - **File Name**: `{{DATE:YYYY-MM-DD}}_アイデア_{{VALUE:タイトル}}`
   - **Create in folder**: `00_Inbox/RawNotes/`
   - **Template Path**: `30_Resources/Templates/IdeaTemplate.md`
   - **Create file if it does not exist**: オン

**結果**: `Ctrl+Shift+I`（設定例）でアイデア入力プロンプト → 自動的に Inbox へ整理されたノート作成

#### 2. プロジェクトノート作成（Macro 設定）

**プロジェクトテンプレート**（`30_Resources/Templates/ProjectTemplate.md`）:

```markdown
---
created: { { DATE:YYYY-MM-DD } }
project: "{{VALUE:プロジェクト名}}"
status: "planning"
tags: [project, { { VALUE:プロジェクト名 } }]
---

# {{VALUE:プロジェクト名}} - プロジェクト概要

## 目標

## タスク

- [ ]

## 関連リソース

## 進捗メモ
```

**Macro 設定**:

1. 新規 Choice 作成: `Create New Project Note`
2. タイプ: `Macro`
3. ステップ設定:
   - プロジェクト名入力
   - テンプレート適用
   - 適切なフォルダへ移動

### 高度な活用パターン

#### Web クリップ整形

```yaml
設定:
  - Capture format: Webクリップテンプレート適用
  - 自動タグ付け: #webclip, #{{DATE:YYYY-MM}}
  - フォルダ: 00_Inbox/WebClips/
```

#### 定期レビュー用ノート

```yaml
設定:
  - Template: レビューテンプレート
  - 自動ファイル名: Weekly_Review_{{DATE:YYYY-MM-DD}}
  - フォルダ: 20_Areas/Personal_Development/01_Daily_Journal/
```

## Auto Note Mover プラグイン設定

### 基本概念

特定のルールに基づいてノートを自動的に適切なフォルダに移動し、手動整理の負担を削減します。

### 実践的ルール設定

#### 1. タグベース自動整理

**プロジェクトノート移動**:

```yaml
Rule Name: "Move Project Notes by Tag"
Trigger: Tag
Tag: "project/"
Destination Folder: "10_Projects/{{match}}"
Enable: ON
```

**結果**: `#project/Client_Alpha`タグ → `10_Projects/Client_Alpha/`へ自動移動

#### 2. フロントマッター基準移動

**完了タスクのアーカイブ**:

```yaml
Rule Name: "Archive Completed Tasks"
Trigger: Frontmatter
Frontmatter Key: "status"
Frontmatter Value Regex: "done|completed"
Destination Folder: "40_Archive/Old_Systems/CompletedTasks/"
Enable: ON
```

**結果**: `status: done`のノート → アーカイブフォルダへ自動移動

#### 3. ファイル名パターン移動

**デイリーノート整理**:

```yaml
Rule Name: "Organize Daily Notes"
Trigger: File name
File name pattern: "^\d{4}-\d{2}-\d{2}"
Destination Folder: "20_Areas/Personal_Development/01_Daily_Journal/{{match:YYYY}}/{{match:MM}}"
Enable: ON
```

### SecondBrain ワークフロー統合設定

#### Inbox 処理自動化

```yaml
# アイデアノート → 知識ベース
Rule: tag:#processed → 20_KnowledgeBase/Ideas/

# Webクリップ → 適切なカテゴリ
Rule: tag:#tech → 20_KnowledgeBase/Technology/
Rule: tag:#business → 20_KnowledgeBase/Business/

# 体験メモ → 内面世界
Rule: tag:#experience → 20_Areas/Personal_Development/02_Experience_Log/
```

#### ステータス管理連携

```yaml
# 作業中 → 進行中フォルダ
Rule: status:in_progress → 10_Projects/Active/

# 完了 → アーカイブ
Rule: status:completed → 40_Archive/Old_Systems/Projects/

# 参考資料 → 知識ベース
Rule: type:reference → 20_KnowledgeBase/References/
```

## 効率化ワークフローの設計

### 統合フロー例

**1. 情報キャプチャ**

```
QuickAdd Capture → 00_Inbox/ → 基本タグ自動付与
```

**2. 初期処理**

```
手動でタグ追加/修正 → Auto Note Mover作動 → 適切フォルダへ移動
```

**3. 継続管理**

```
ステータス更新 → Auto Note Mover → アーカイブ/アクティブ管理
```

### 推奨設定テンプレート

#### QuickAdd 推奨 Choice 構成

1. **Daily Capture**: 日常のアイデア・メモ
2. **Project Start**: 新規プロジェクト立ち上げ
3. **Web Research**: Web 情報の構造化キャプチャ
4. **Review Create**: 定期レビュー用ノート

#### Auto Note Mover 推奨ルール

1. **Tag-based Sorting**: タグによる基本分類
2. **Status Management**: 作業ステータス管理
3. **Archive Automation**: 完了項目の自動アーカイブ
4. **Cleanup Rules**: 孤立ファイルの整理

## パフォーマンス最適化

### 設定時の注意点

- **ルール競合回避**: 複数ルールが同一ファイルにマッチしないよう調整
- **フォルダ事前作成**: 移動先フォルダの存在確認
- **テスト環境**: 小規模テストでの動作確認

### トラブルシューティング

```yaml
よくある問題:
  - 移動先フォルダが存在しない → 手動作成またはルール修正
  - ルール優先度の競合 → ルール順序の調整
  - テンプレート変数エラー → 変数名の確認
```

## 運用・メンテナンス

### 定期メンテナンス（月 1 回）

- [ ] 移動ルールの効果測定
- [ ] 孤立ファイルの確認
- [ ] テンプレートの改善
- [ ] 新規ルールの必要性検討

### 効果測定指標

- **処理時間短縮**: 手動整理時間の削減量
- **分類精度**: 自動分類の適切性
- **ファイル発見性**: 目的ファイルへのアクセス時間

## セキュリティ・バックアップ

### 重要な注意事項

- **テストファースト**: 新規ルール導入前の小規模テスト
- **バックアップ**: 自動移動前のバックアップ習慣
- **ログ確認**: 移動履歴の定期確認

## 関連リンク

- [[SecondBrain/30_Resources/Tools_Documentation/Obsidian知識管理戦略_グラフビューとMOC活用法]]
- [[SecondBrainワークフロー完全ガイド]]
- _テンプレート活用術_（参照未設定）

## 処理ログ

- 処理日: 2025-05-23
- 処理種別: RawNotes → プラグイン設定ガイド体系化
- アーカイブ予定: Yes
- 分類: ツール効率化設定
