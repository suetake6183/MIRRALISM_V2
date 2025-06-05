#!/usr/bin/env python3
"""
MIRRALISM V2 開発環境自動セットアップスクリプト
V1の教訓を活かした品質保証環境の構築
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description, check=True):
    """コマンド実行とエラーハンドリング"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=check, capture_output=True, text=True
        )
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ エラー: {e}")
        if e.stderr:
            print(f"詳細: {e.stderr}")
        return False


def check_python_version():
    """Python 3.9+ の確認"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9以上が必要です。現在: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True


def setup_pre_commit():
    """pre-commit環境のセットアップ"""
    print("\n🎯 MIRRALISM品質保証システム セットアップ開始\n")

    # Python バージョンチェック
    if not check_python_version():
        return False

    # pre-commit インストール
    if not run_command("pip install pre-commit", "pre-commitインストール"):
        return False

    # pre-commit セットアップ
    if not run_command("pre-commit install", "pre-commitフック登録"):
        return False

    # 初回実行（全ファイル対象）
    print("\n🔍 初回品質チェック実行...")
    result = run_command("pre-commit run --all-files", "全ファイル品質チェック", check=False)

    if not result:
        print("\n⚠️ ファイルが自動修正されました。これは正常な動作です。")
        print("📋 次の手順:")
        print("1. git add . でファイルをステージング")
        print("2. git commit でコミット実行")
        print("3. 以降のコミットでは自動的に品質チェックが実行されます")
    else:
        print("\n✅ すべてのファイルが品質基準を満たしています！")

    return True


def setup_additional_tools():
    """追加開発ツールのセットアップ"""
    print("\n🛠️ 追加開発ツールセットアップ...")

    tools = [
        ("black", "コードフォーマッター"),
        ("isort", "import順序整理"),
        ("pytest", "テストフレームワーク"),
        ("pytest-cov", "テストカバレッジ"),
    ]

    for tool, description in tools:
        run_command(f"pip install {tool}", f"{description}インストール", check=False)


def create_development_guide():
    """開発ガイドの作成"""
    guide_content = """# MIRRALISM V2 開発環境ガイド

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
"""

    with open("DEVELOPMENT_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("📚 開発ガイド (DEVELOPMENT_GUIDE.md) を作成しました")


def main():
    """メイン実行関数"""
    print("🏗️ MIRRALISM V2 開発環境セットアップ")
    print("=" * 50)

    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 プロジェクトディレクトリ: {project_root}")

    # セットアップ実行
    success = True
    success &= setup_pre_commit()
    setup_additional_tools()  # エラーでも継続
    create_development_guide()

    # 結果表示
    print("\n" + "=" * 50)
    if success:
        print("🎉 MIRRALISM V2 開発環境セットアップ完了！")
        print("✅ 品質保証システム: 稼働中")
        print("✅ V1問題防止策: 実装済み")
        print("\n📖 DEVELOPMENT_GUIDE.md をご参照ください")
    else:
        print("⚠️ セットアップ中にエラーが発生しました")
        print("🔧 手動でのセットアップをお試しください")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
