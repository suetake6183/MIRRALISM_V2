# MIRRALISM V2 開発環境ガイド

## 🎯 品質保証システム

### Pre-commit フック
- **自動実行**: 各コミット前に品質チェック実行
- **対象**: コードフォーマット、import順序、構文チェック等
- **修正**: 問題があれば自動修正（再コミット必要）

### 手動実行
```bash
# 全ファイル対象
pre-commit run --all-files

# 特定ファイル対象  
pre-commit run --files path/to/file.py
```

### トラブルシューティング
- **修正後の再コミット**: ファイルが自動修正された場合は再度コミット
- **フック無効化**: 緊急時のみ `git commit --no-verify`
- **設定更新**: `.pre-commit-config.yaml` 編集後は `pre-commit install`

## 🧪 テスト実行
```bash
# 基本テスト
pytest tests/

# カバレッジ付き
pytest tests/ --cov=.
```

## 🔧 コード品質チェック
```bash
# フォーマット確認
black --check .

# import順序確認
isort --check-only .
```

---
*MIRRALISM V2: V1の教訓を活かした高品質開発環境*
