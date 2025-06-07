# 🔍 SecondBrain v2.0 データ分類・移植計画

**作成日**: 2025 年 6 月 1 日  
**目的**: 絶対に移植すべき情報とそうでない情報の厳格仕分け

## 📊 **G-TECH バックアップシステム確認結果**

```yaml
G-TECHボリューム状況:
✅ 接続状態: 正常（/Volumes/G-TECH/確認済み）
✅ 利用可能スペース: 十分
✅ 過去のバックアップ: 2025-05-31まで実行済み
✅ バックアップパス: /Volumes/G-TECH/SecondBrain_Emergency_Backups/

結論: G-TECH利用は問題なし
```

## 🎯 **絶対に移植すべき情報（Tier 1）**

### **1. PersonalityLearning 53%精度システム**

```yaml
移植対象:
📊 データベースファイル:
  - personality_learning.db（4エントリの学習データ）
  - emotion_reactions テーブル
  - value_patterns テーブル
  - analysis_history テーブル

📊 学習パラメータ:
  - 53%精度達成の設定ファイル
  - アルゴリズム調整値
  - 学習済みモデルパラメータ

📊 分析ロジック:
  - 説明的表現パターン認識
  - 論理的思考判定ロジック
  - 感情分析アルゴリズム

推定サイズ: 2MB
重要度: 最高（1000万円技術資産）
```

### **2. 核心概念・設計思想（文書）**

```yaml
移植対象:
📝 基本原則文書:
  - SYSTEM_FUNDAMENTAL_PRINCIPLE.md
  - SSOT原則の完全定義
  - 第一の脳・第二の脳協働概念

📝 設計文書:
  - SecondBrain_Essential_Concepts_Extract.md（作成済み）
  - SecondBrain_v2_Migration_Plan.md（作成済み）
  - PARA Method定義

推定サイズ: 500KB
重要度: 最高（システムの魂）
```

### **3. 実際の知識ベース（REDIRECT ファイル除外）**

```yaml
移植対象:
📝 実際のコンテンツ:
  - 実在する.mdファイル（*REDIRECT*除外）
  - 重要なテンプレート
  - 実際の日記・ノートデータ
  - 価値あるプロジェクトファイル

📝 除外対象: ❌ 28,066個のREDIRECTファイル
  ❌ 重複ファイル
  ❌ 空の.mdファイル

推定サイズ: 5MB
重要度: 高（実際の知識）
```

### **4. API 統合設定（最小限）**

```yaml
移植対象:
🔑 SuperWhisper統合:
  - API認証情報
  - 統合ワークフロー設定
  - 音声処理パラメータ

🔑 Notion統合:
  - API keys
  - データベースID
  - 連携設定

推定サイズ: 100KB
重要度: 高（機能継続）
```

## ❌ **移植しない情報（Tier 2 - 技術負債）**

### **1. REDIRECT ファイルシステム**

```yaml
完全廃棄対象:
❌ 28,066個のREDIRECTファイル
❌ SSOT_REDIRECT系統
❌ 自動生成されたリダイレクト

理由: 複雑性の元凶、価値なし
削減効果: 99%のファイル数削減
```

### **2. 過剰な自動化システム**

```yaml
完全廃棄対象:
❌ 57,271行の複雑なPythonコード
❌ 87個のデータベースファイル（大部分）
❌ 複雑な監視・チェックシステム
❌ Phase08_Migration系統

理由: 過度な複雑性、保守不可能
削減効果: 90%のコード量削減
```

### **3. 重複・バックアップファイル**

```yaml
完全廃棄対象:
❌ .backup_102539 系統ファイル
❌ 古いアーカイブファイル
❌ Emergency_Backups（重複分）
❌ Legacy_90_System

理由: 重複、古い、不要
削減効果: 80%のストレージ削減
```

## 🔄 **保管のみ（移植しないが保存）**

```yaml
G-TECHバックアップ対象:
📦 現在のSecondBrain全体（完全コピー）
📦 PersonalityLearning完全バックアップ
📦 重要設定ファイル群
📦 作業履歴・ログファイル

保管理由: 緊急時復旧、参考資料
バックアップ先: /Volumes/G-TECH/SecondBrain_v1_Complete_Archive/
```

## 📈 **移植データ作成計画**

### **Phase 1: 重要データ抽出（2 時間）**

```bash
# PersonalityLearning完全抽出
mkdir -p /tmp/SecondBrain_v2_Migration/essential_data/
sqlite3 .system_core/PersonalityLearning/Data/Processed/personality_learning.db \
  ".backup /tmp/SecondBrain_v2_Migration/essential_data/personality_core.db"

# 設定ファイル抽出
cp .system_core/SYSTEM_FUNDAMENTAL_PRINCIPLE.md \
   /tmp/SecondBrain_v2_Migration/essential_data/

# 実際の知識ファイル抽出（REDIRECTファイル完全除外）
find . -name "*.md" -not -name "*REDIRECT*" -not -path "./.system_core/Archive/*" \
  -not -path "./test_environment/*" | \
  xargs tar -czf /tmp/SecondBrain_v2_Migration/essential_data/knowledge_base_pure.tar.gz
```

### **Phase 2: データ変換・最適化（1 時間）**

```bash
# データベースの最適化
sqlite3 /tmp/SecondBrain_v2_Migration/essential_data/personality_core.db "VACUUM;"

# 設定ファイルの統合・最適化
# API設定の安全な抽出と統合
```

### **Phase 3: 品質確認（30 分）**

```bash
# データ整合性確認
# ファイル数・サイズ確認
# 必要最小限の確認
```

## 📊 **移植効果予測**

```yaml
削減効果:
  - ファイル数: 42,000 → 500（99%削減）
  - システムサイズ: 1GB → 10MB（99%削減）
  - データベース: 87個 → 3個（97%削減）
  - コード行数: 57,271行 → 2,000行（96%削減）

保護される価値:
✅ PersonalityLearning 53%精度: 100%保護
✅ 核心思想・概念: 100%保護
✅ 実際の知識: 100%保護
✅ API統合: 100%保護

品質向上:
✅ 理解時間: 数日 → 1時間
✅ 開発効率: 10倍向上
✅ 保守性: 20倍向上
✅ 拡張性: 容易
```

---

**この分類に基づき、段階的データ移植を実行します**
