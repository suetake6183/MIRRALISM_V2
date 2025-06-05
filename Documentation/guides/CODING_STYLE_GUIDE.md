# 🎨 MIRRALISM V2 コーディングスタイルガイド

**採用日**: 2025 年 6 月 3 日
**対象**: MIRRALISM V2 プロジェクト全体
**メンテナ**: 末武修平

## 📋 **選択されたスタイルガイド**

### **Python: PEP8（公式推奨）**

- **理由**: Python 公式、最も標準的、豊富なツールサポート
- **参考**: https://peps.python.org/pep-0008/
- **適用範囲**: Core/、API/、scripts/ 内の全 Python ファイル

### **JavaScript/HTML: Google Style Guide**

- **理由**: 明確なルール、保守性重視
- **参考**: https://google.github.io/styleguide/jsguide.html
- **適用範囲**: Interface/ 内のフロントエンドコード

### **Markdown: CommonMark + 日本語拡張**

- **理由**: 国際標準 + 日本語文書対応
- **適用範囲**: Documentation/ 内の全ドキュメント

## 🔧 **Python PEP8 主要ルール**

### **インデント**

```python
# ✅ 良い例
def function_name():
    if condition:
        return value

# ❌ 悪い例
def function_name():
  if condition:
      return value
```

### **行の長さ**

```python
# ✅ 79文字以内
def analyze_personality_learning_data(
    content, source_type, metadata
):
    pass

# ❌ 長すぎる行
def analyze_personality_learning_data(content, source_type, metadata, additional_params):
```

### **命名規則**

```python
# ✅ 良い例
class PersonalityLearningCore:
    def analyze_journal_entry(self):
        local_variable = "value"

# ❌ 悪い例
class personalityLearningCore:
    def analyzeJournalEntry(self):
        LocalVariable = "value"
```

### **インポート順序**

```python
# ✅ 正しい順序
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from personality_learning_core import AnalysisEngine
```

## 🛠️ **自動化ツール設定**

### **Flake8 設定**

```ini
# setup.cfg
[flake8]
max-line-length = 79
exclude = .git,__pycache__,docs/source/conf.py,old,build,dist
ignore = E203,W503
```

### **Black 設定**

```toml
# pyproject.toml
[tool.black]
line-length = 79
target-version = ['py38']
include = '\.pyi?$'
```

### **isort 設定**

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 79
multi_line_output = 3
```

## 📝 **MIRRALISM 固有ルール**

### **ファイル命名**

```
# ✅ 推奨
personality_learning_core.py
database_manager.py
superwhisper_integration.py

# ❌ 非推奨
PersonalityLearningCore.py
databaseManager.py
SuperWhisperIntegration.py
```

### **クラス設計**

```python
# ✅ MIRRALISM推奨パターン
class PersonalityLearningCore:
    """
    MIRRALISM V2 PersonalityLearning核心システム

    V1から移行された学習データを管理し、
    53%→95%精度進化を実現する。
    """

    def __init__(self):
        self.accuracy = 53.0  # V1ベースライン
        self.target_accuracy = 95.0

    def analyze_journal_entry(self, content: str) -> dict:
        """
        日記エントリー分析

        Args:
            content: 分析対象テキスト

        Returns:
            dict: 分析結果
        """
        pass
```

### **コメント規則**

```python
# ✅ 日本語コメント推奨（MIRRALISM内部）
def calculate_accuracy(self):
    """精度計算メソッド"""
    # V1互換性を保持しながら精度向上
    return self.current_accuracy

# ✅ 英語コメント（外部公開想定）
def get_system_status(self):
    """Get current system status"""
    # Maintain V1 compatibility while improving accuracy
    return self.status
```

## 🎯 **品質指標**

### **必須チェック項目**

- [ ] PEP8 準拠（flake8 でチェック）
- [ ] 行長 79 文字以内
- [ ] 適切な命名規則
- [ ] docstring 記載
- [ ] 型ヒント（Python 3.8+）

### **推奨項目**

- [ ] 関数は 20 行以内
- [ ] クラスは 200 行以内
- [ ] サイクロマティック複雑度 10 以下
- [ ] テストカバレッジ 80%以上

## 🔄 **適用プロセス**

1. **即座適用**: 新規ファイル作成時
2. **段階適用**: 既存ファイル修正時
3. **全体適用**: リファクタリング時

## 📊 **効果測定**

- **コード品質**: flake8 スコア
- **保守性**: 修正時間の短縮
- **一貫性**: スタイル違反件数の減少

---

**🎉 PEP8 採用により、MIRRALISM V2 の開発品質が統一されました！**
