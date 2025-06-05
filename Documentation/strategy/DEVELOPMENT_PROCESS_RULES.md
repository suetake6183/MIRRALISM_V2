# 🔧 MIRRALISM 開発プロセスルール

**制定日**: 2025 年 6 月 3 日
**目的**: scripts ディレクトリ問題の再発防止
**効果測定**: 継続的モニタリング

## 📋 **新設ルール一覧**

### **ルール 1: 設計書事前確認義務**

```
🚨 必須チェック項目:
□ 新規ディレクトリ作成前に設計書確認
□ 設計書にない場合は事前相談
□ 承認後に設計書更新
□ 実装完了後に整合性確認
```

### **ルール 2: 自動チェック機能統合**

```python
# scripts/pre_implementation_check.py
def check_design_compliance(new_directory):
    """設計書準拠チェック"""
    design_dirs = get_design_directories()
    if new_directory not in design_dirs:
        raise DesignViolationError(
            f"❌ {new_directory}は設計書に記載されていません。"
            f"事前相談が必要です。"
        )
```

### **ルール 3: 週次レビュー制度**

```
📅 毎週月曜日:
- 新規作成ディレクトリの確認
- 設計書との整合性チェック
- 問題があれば即座に修正
```

## 📊 **機能実証実験**

### **実験 1: 故意の設計書違反テスト**

<function_calls>
<invoke name="run_terminal_cmd">
<parameter name="command">echo "🧪 Process Fix 機能テスト" && echo "=========================" && echo "テスト: 設計書にない'test_directory'を作成しようとする" && echo ""
</invoke>
</function_calls>
