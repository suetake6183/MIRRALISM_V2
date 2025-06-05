#!/usr/bin/env python3
"""
MIRRALISM Cursor×Codex統合設定確認スクリプト
PersonalityLearning開発環境の最適化検証

実行: python3 verify_cursor_setup.py
"""

import json
import os
from pathlib import Path

import requests


def check_environment_variables():
    """環境変数の確認"""
    print("🔍 環境変数確認...")

    required_vars = {
        "OPENAI_API_KEY": "OpenAI API Key",
        "GOOGLE_API_KEY": "Google API Key",
    }

    status = {}
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != "sk-your-openai-api-key-here":
            print(f"✅ {description}: 設定済み")
            status[var] = True
        else:
            print(f"❌ {description}: 未設定")
            status[var] = False

    return status


def check_cursor_mcp_config():
    """Cursor MCP設定確認"""
    print("\n🔍 Cursor MCP設定確認...")

    mcp_path = Path.home() / ".cursor" / "mcp.json"

    if not mcp_path.exists():
        print("❌ MCP設定ファイルが見つかりません")
        return False

    try:
        with open(mcp_path, "r") as f:
            config = json.load(f)

        if "mcpServers" in config:
            print("✅ MCP設定ファイル存在")

            if "task-master-ai" in config["mcpServers"]:
                print("✅ TaskMaster AI設定済み")

                env_vars = config["mcpServers"]["task-master-ai"].get("env", {})
                if "OPENAI_API_KEY" in env_vars:
                    print("✅ OpenAI API Key in MCP設定済み")
                else:
                    print("⚠️ OpenAI API Key in MCP未設定")

                return True

        print("❌ MCP設定が不完全")
        return False

    except Exception as e:
        print(f"❌ MCP設定読み込みエラー: {e}")
        return False


def test_openai_connection():
    """OpenAI接続テスト"""
    print("\n🔍 OpenAI接続テスト...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "sk-your-openai-api-key-here":
        print("❌ OpenAI API Keyが設定されていません")
        return False

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # OpenAI Models APIでテスト
        response = requests.get(
            "https://api.openai.com/v1/models", headers=headers, timeout=10
        )

        if response.status_code == 200:
            models = response.json()
            codex_models = [m["id"] for m in models["data"] if "code" in m["id"]]

            if codex_models:
                print("✅ OpenAI API接続成功")
                print(f"✅ Codex利用可能: {len(codex_models)}モデル")
                return True
            else:
                print("⚠️ Codexモデルが見つかりません")
                return False
        else:
            print(f"❌ OpenAI API接続失敗: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ OpenAI接続テストエラー: {e}")
        return False


def check_cursor_extensions():
    """Cursor拡張機能確認"""
    print("\n🔍 Cursor拡張機能確認...")

    extensions_path = Path.home() / ".cursor" / "extensions"

    if not extensions_path.exists():
        print("❌ Cursor拡張ディレクトリが見つかりません")
        return False

    extensions = list(extensions_path.iterdir())
    ai_extensions = [
        ext
        for ext in extensions
        if any(
            keyword in ext.name.lower()
            for keyword in ["openai", "chatgpt", "copilot", "ai"]
        )
    ]

    if ai_extensions:
        print(f"✅ AI拡張機能: {len(ai_extensions)}個発見")
        for ext in ai_extensions:
            print(f"  - {ext.name}")
        return True
    else:
        print("⚠️ AI関連拡張機能が見つかりません")
        return False


def generate_cursor_config_instructions():
    """Cursor設定手順の生成"""
    print("\n📋 Cursor設定手順:")

    instructions = """

1. Cursorを開く
2. ⌘, (Preferences) を押す
3. 左サイドバー → "AI" を選択
4. OpenAI設定:
   - API Key: {api_key_status}
   - Model: code-davinci-002
   - Max Tokens: 2048

5. Chat Panel:
   - 右サイド Chat アイコン
   - 設定 → Model → OpenAI Codex

6. インライン補完:
   - Preferences → AI → Autocomplete
   - Provider: OpenAI
   - Model: code-davinci-002
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "sk-your-openai-api-key-here":
        api_key_status = "設定済み ✅"
    else:
        api_key_status = "要設定 ❌"

    print(instructions.format(api_key_status=api_key_status))


def main():
    """設定確認メイン処理"""
    print("🚀 MIRRALISM Cursor×Codex統合設定確認")
    print("=" * 50)

    # 各種確認実行
    env_status = check_environment_variables()
    mcp_status = check_cursor_mcp_config()
    openai_status = test_openai_connection()
    ext_status = check_cursor_extensions()

    # 総合評価
    print("\n🏆 総合評価:")
    print("=" * 50)

    total_checks = 4
    passed_checks = sum(
        [any(env_status.values()), mcp_status, openai_status, ext_status]
    )

    success_rate = (passed_checks / total_checks) * 100

    if success_rate >= 75:
        print(f"✅ 設定完了度: {success_rate:.0f}%")
        print("🚀 Cursor×Codex統合準備完了！")
        print("PersonalityLearning 95%精度達成へ突進しましょう！")
    elif success_rate >= 50:
        print(f"⚠️ 設定進行度: {success_rate:.0f}%")
        print("追加設定が必要です")
    else:
        print(f"❌ 設定完了度: {success_rate:.0f}%")
        print("基本設定から始めてください")

    # 設定手順表示
    generate_cursor_config_instructions()

    print("\n📖 詳細設定: cursor_codex_setup.md を参照")


if __name__ == "__main__":
    main()
