# ファイル整理実行チェックリスト

## 🔒 事前安全確保（必須）

### バックアップ実施
- [ ] Git commit実行（現状保存）
- [ ] 削除対象ファイルの個別バックアップ
- [ ] バックアップ先の確認（復旧可能性確認）

### 影響確認
- [ ] 削除対象ファイルの参照関係確認
- [ ] grep -r でファイル名検索実施
- [ ] リンク切れリスクの評価

## 🎯 段階的削除実行

### Stage 1: 低リスクファイル削除
- [ ] high_priority_files.txt 削除
- [ ] medium_priority_files.txt 削除  
- [ ] low_priority_files.txt 削除
- [ ] 削除後の動作確認

### Stage 2: 重複レポート削除
- [ ] SecondBrain_SystemIntegrated_Report_20250528.md
  - [ ] Emergency_Response_Reportとの内容比較
  - [ ] 削除実行
  - [ ] 動作確認
- [ ] SecondBrain_Comprehensive_Report_20250528.md
  - [ ] Emergency_Response_Reportとの内容比較
  - [ ] 削除実行
  - [ ] 動作確認

### Stage 3: 条件付きファイル評価
- [ ] Failure_Analysis_Report_20250528.md
  - [ ] Emergency_Response_Reportに統合済みか確認
  - [ ] 統合済みなら削除実行
  - [ ] 動作確認

## ✅ 最終検証

### SSOT原則確認
- [ ] 重複ファイルの完全削除確認
- [ ] 情報の一意性確保確認
- [ ] 情報の完全性確認

### システム動作確認
- [ ] 全システムの正常稼働確認
- [ ] リンク切れなし確認
- [ ] 機能テスト実施

### 清掃結果記録
- [ ] 削除ファイル一覧作成
- [ ] 削除理由の記録
- [ ] 改善効果の測定

## 📊 完了報告項目

### 定量結果
- 削除ファイル数: ___個
- 削減容量: ___KB/MB
- SSOT違反解消: ___件

### 品質確認
- システム稼働: 正常/異常
- 機能テスト: 合格/不合格
- リンク切れ: なし/あり

### 改善効果
- ファイル構造明確化: 改善/未改善
- SSOT原則遵守: 達成/未達成
- 管理効率向上: 向上/変化なし

## ⚠️ 問題発生時対応

### 即座復旧手順
1. Git reset --hard [commit_hash] で復旧
2. バックアップからの個別復旧
3. 影響範囲の確認・修正

### 報告事項
- 発生した問題の詳細
- 対応措置の内容
- 再発防止策

---
**作成日**: 2025年5月30日  
**作成者**: CTO指示  
**期限**: 明日20:00厳守  
**責任者**: Cursor Cloud4