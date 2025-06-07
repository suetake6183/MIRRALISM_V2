#!/usr/bin/env python3
"""
Notion統合診断ツール
==================

目的: SuperWhisper-Notion統合の接続問題を診断・修復
作成日: 2025年6月6日
"""

import json
import requests
from pathlib import Path


def diagnose_notion_connection():
    """Notion接続の診断"""
    print("🔍 Notion統合診断開始")
    print("=" * 50)
    
    # 設定ファイル読み込み
    config_path = Path(__file__).parent.parent / "API" / "30_Resources" / "Configuration" / "superwhisper_config.json"
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        token = config.get("notion_token")
        database_id = config.get("notion_database_id")
        
        print(f"✅ 設定ファイル読み込み完了")
        print(f"   Token: {token[:20]}...{token[-4:] if len(token) > 24 else token}")
        print(f"   Database ID: {database_id}")
        
    except Exception as e:
        print(f"❌ 設定ファイル読み込み失敗: {e}")
        return
    
    # APIトークン検証
    print("\n🔑 APIトークン検証中...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    try:
        # ユーザー情報取得
        response = requests.get("https://api.notion.com/v1/users/me", headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ APIトークン有効")
            print(f"   User: {user_info.get('name', 'Unknown')}")
            print(f"   Type: {user_info.get('type', 'Unknown')}")
        else:
            print(f"❌ APIトークンエラー: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ APIリクエスト失敗: {e}")
        return
    
    # データベースアクセス検証
    print("\n📊 データベースアクセス検証中...")
    try:
        db_url = f"https://api.notion.com/v1/databases/{database_id}"
        response = requests.get(db_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            db_info = response.json()
            print(f"✅ データベースアクセス成功")
            print(f"   タイトル: {db_info.get('title', [{}])[0].get('text', {}).get('content', 'Unknown')}")
            print(f"   作成日: {db_info.get('created_time', 'Unknown')}")
            
            # プロパティ確認
            properties = db_info.get('properties', {})
            print(f"   プロパティ数: {len(properties)}")
            for prop_name in list(properties.keys())[:5]:  # 最初の5つまで表示
                prop_type = properties[prop_name].get('type', 'unknown')
                print(f"     - {prop_name}: {prop_type}")
                
        elif response.status_code == 404:
            print(f"❌ データベースが見つかりません")
            print(f"   ID: {database_id}")
            print(f"   エラー: {response.text}")
            print("\n💡 解決方法:")
            print("   1. NotionでデータベースページでIntegrationを共有")
            print("   2. データベースIDが正しいか確認")
            print("   3. Integrationに適切な権限があるか確認")
            
        else:
            print(f"❌ データベースアクセスエラー: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ データベースリクエスト失敗: {e}")
    
    # クエリテスト
    print("\n🔍 データベースクエリテスト...")
    try:
        query_url = f"https://api.notion.com/v1/databases/{database_id}/query"
        query_data = {
            "page_size": 1,
            "sorts": [{"property": "日付", "direction": "descending"}]
        }
        
        response = requests.post(query_url, headers=headers, json=query_data, timeout=10)
        
        if response.status_code == 200:
            query_result = response.json()
            results = query_result.get('results', [])
            print(f"✅ クエリ成功")
            print(f"   総エントリ数確認可能: {len(results)}件取得")
            
            if results:
                entry = results[0]
                print(f"   最新エントリID: {entry.get('id', 'Unknown')}")
                created_time = entry.get('created_time', 'Unknown')
                print(f"   最新エントリ作成日: {created_time}")
                
        else:
            print(f"❌ クエリエラー: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ クエリリクエスト失敗: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 診断完了")


def suggest_fixes():
    """修復提案"""
    print("\n🔧 修復提案:")
    print("1. Notionワークスペースでの設定:")
    print("   - データベースページを開く")
    print("   - 右上の「共有」ボタンをクリック")
    print("   - 「Integrationを追加」でAPIキーのIntegrationを追加")
    print("   - 「読み取り」「更新」権限を有効化")
    
    print("\n2. データベースID確認:")
    print("   - NotionのデータベースURLを確認")
    print("   - URLの形式: https://notion.so/{database_id}?v=...")
    print("   - {database_id}部分を設定ファイルに設定")
    
    print("\n3. APIキー確認:")
    print("   - Notion DevelopersでIntegrationを確認")
    print("   - 新しいSecretを生成して設定")


if __name__ == "__main__":
    diagnose_notion_connection()
    suggest_fixes()