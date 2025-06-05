#!/usr/bin/env python3
"""
MIRRALISM PersonalityLearning緊急復旧スクリプト
精度劣化時の自動復旧システム
"""

import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


def emergency_restore_accuracy(backup_location: str, target_database: str):
    """緊急精度復旧"""
    print(f"🚨 緊急復旧開始: {backup_location} → {target_database}")

    try:
        backup_path = Path(backup_location)
        target_path = Path(target_database)

        if not backup_path.exists():
            print(f"❌ バックアップが見つかりません: {backup_path}")
            return False

        # データベース復旧
        shutil.copy2(backup_path, target_path)

        # 精度確認
        conn = sqlite3.connect(target_path)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(overall_accuracy) FROM learning_accuracy")
        accuracy = cursor.fetchone()[0]
        conn.close()

        print(f"✅ 復旧完了: 精度 {accuracy:.1%}")
        return True

    except Exception as e:
        print(f"❌ 復旧失敗: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        emergency_restore_accuracy(sys.argv[1], sys.argv[2])
    else:
        print(
            "使用法: python personality_learning_recovery.py <backup_path> <target_database>"
        )
