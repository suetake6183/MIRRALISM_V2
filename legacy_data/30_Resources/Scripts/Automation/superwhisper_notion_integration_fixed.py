#!/usr/bin/env python3
"""
SuperWhisper-Notion統合システム（修正版）
作成者: MIRRALISM技術者
修正日: 2025年6月3日
目的: 時刻フォーマットバグの完全修正とISO 8601準拠強制実装

重要な修正内容:
- 日本語環境での時刻フォーマット問題を根本解決
- ISO 8601完全形式の強制実装
- 不完全な時刻データのバリデーション・修正機能
- 00:00:00境界時刻での処理改善
"""

import os
import sys
import json
import time
import logging
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3
import re

# システムパス追加
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent.parent / "AI_Systems" / "Core"))


class SuperWhisperNotionIntegrationFixed:
    """SuperWhisper-Notion統合システム（時刻バグ修正版）"""

    def __init__(self, config_path: str = None):
        """
        システム初期化（修正版）

        Args:
            config_path: 設定ファイルパス
        """
        self.base_dir = Path(__file__).parent.parent.parent  # SecondBrain/
        self.inbox_dir = self.base_dir / "00_Inbox"
        self.personal_thoughts_dir = self.inbox_dir / "💭 Personal_Thoughts"
        self.inbox_raw_dir = self.inbox_dir / "📥 Inbox_Raw"

        # ディレクトリ確認・作成
        self.personal_thoughts_dir.mkdir(parents=True, exist_ok=True)
        self.inbox_raw_dir.mkdir(parents=True, exist_ok=True)

        # ログ設定
        self.logger = self._setup_logger()

        # 設定読み込み
        self.config = self._load_config(config_path)

        # Notion API設定
        self.notion_token = self.config.get("notion_token")
        self.notion_database_id = self.config.get("notion_database_id")

        # 処理済みエントリ管理用DB
        self.processed_db = (
            self.base_dir / ".system_internal" / "superwhisper_processed.db"
        )
        self.processed_db.parent.mkdir(parents=True, exist_ok=True)
        self._init_processed_db()

        self.logger.info("SuperWhisper-Notion統合システム（修正版）初期化完了")

    def _setup_logger(self) -> logging.Logger:
        """ログ設定"""
        logger = logging.getLogger("SuperWhisperNotionIntegrationFixed")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # ログディレクトリ
            log_dir = self.base_dir / ".system_internal" / "_LOGS"
            log_dir.mkdir(parents=True, exist_ok=True)

            # ファイルハンドラー
            log_file = log_dir / "superwhisper_integration_fixed.log"
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # コンソールハンドラー
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

        return logger

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """設定ファイル読み込み"""
        if config_path is None:
            config_path = (
                self.base_dir
                / "30_Resources"
                / "Configuration"
                / "superwhisper_config.json"
            )

        try:
            if Path(config_path).exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # デフォルト設定作成
                default_config = {
                    "notion_token": "YOUR_NOTION_TOKEN_HERE",
                    "notion_database_id": "YOUR_DATABASE_ID_HERE",
                    "monitor_interval": 300,  # 5分間隔
                    "quality_threshold": 0.9,  # 転写品質閾値
                    "min_text_length": 20,  # 最小文字数
                    "max_noise_level": 0.3,  # 最大ノイズレベル
                }

                # 設定ファイル作成
                config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)

                self.logger.warning(f"設定ファイルを作成しました: {config_path}")
                self.logger.warning("Notion API設定を編集してください")

                return default_config

        except Exception as e:
            self.logger.error(f"設定ファイル読み込みエラー: {e}")
            return {}

    def _init_processed_db(self):
        """処理済みエントリ管理DB初期化"""
        try:
            conn = sqlite3.connect(str(self.processed_db))
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_entries (
                    notion_id TEXT PRIMARY KEY,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_path TEXT,
                    classification TEXT,
                    quality_score REAL,
                    created_time_original TEXT,
                    created_time_fixed TEXT
                )
            """
            )

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"処理済みDB初期化エラー: {e}")

    def _fix_datetime_format(self, raw_datetime: str) -> str:
        """
        🔧 時刻フォーマット修正（バグ修正の核心）

        日本語環境で発生する不完全な時刻フォーマットを
        ISO 8601完全形式に修正する

        Args:
            raw_datetime: Notionから受け取った生の時刻文字列

        Returns:
            ISO 8601準拠の完全な時刻文字列
        """
        if not raw_datetime:
            # 空の場合は現在時刻を使用
            now = datetime.now(timezone.utc)
            fixed_time = now.isoformat()
            self.logger.warning(f"空の時刻データを修正: {fixed_time}")
            return fixed_time

        try:
            # パターン1: 完全なISO形式 (正常ケース)
            if re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", raw_datetime):
                dt = datetime.fromisoformat(raw_datetime.replace("Z", "+00:00"))
                return dt.isoformat()

            # パターン2: 日付のみ（バグパターン）
            if re.match(r"^\d{4}-\d{2}-\d{2}$", raw_datetime):
                # 日付のみの場合、00:00:00 UTCとして補完
                dt = datetime.fromisoformat(f"{raw_datetime}T00:00:00+00:00")
                fixed_time = dt.isoformat()
                self.logger.warning(
                    f"不完全な時刻データを修正: {raw_datetime} → {fixed_time}"
                )
                return fixed_time

            # パターン3: 時刻はあるがタイムゾーンなし
            if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", raw_datetime):
                dt = datetime.fromisoformat(f"{raw_datetime}+00:00")
                fixed_time = dt.isoformat()
                self.logger.info(f"タイムゾーンを補完: {raw_datetime} → {fixed_time}")
                return fixed_time

            # パターン4: その他の形式を強制パース
            try:
                # 可能な限りパースを試行
                dt = datetime.fromisoformat(raw_datetime.replace("Z", "+00:00"))
                return dt.isoformat()
            except:
                # 完全に失敗した場合は現在時刻で代替
                now = datetime.now(timezone.utc)
                fixed_time = now.isoformat()
                self.logger.error(
                    f"時刻パース失敗、現在時刻で代替: {raw_datetime} → {fixed_time}"
                )
                return fixed_time

        except Exception as e:
            # 例外発生時は現在時刻で代替
            now = datetime.now(timezone.utc)
            fixed_time = now.isoformat()
            self.logger.error(
                f"時刻修正処理エラー ({raw_datetime}): {e} → {fixed_time}"
            )
            return fixed_time

    def _validate_datetime_quality(self, original: str, fixed: str) -> Dict[str, Any]:
        """
        時刻修正の品質検証

        Args:
            original: 元の時刻文字列
            fixed: 修正後の時刻文字列

        Returns:
            検証結果
        """
        result = {
            "is_fixed": original != fixed,
            "original": original,
            "fixed": fixed,
            "fix_type": "none",
        }

        if not original:
            result["fix_type"] = "empty_to_current"
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", original):
            result["fix_type"] = "date_only_to_full"
        elif original != fixed:
            result["fix_type"] = "timezone_completion"

        return result

    # ... existing methods would continue here ...
    # （元のメソッドはここに継続されます）

    def _create_file_content_fixed(
        self, entry_data: Dict[str, Any], classification: str
    ) -> str:
        """
        🔧 修正版: 保存ファイルの内容作成（バグ修正適用）
        """
        raw_created_time = entry_data.get("created_time", "")
        text_content = entry_data.get("text_content", "")
        quality_score = entry_data.get("quality_score", 0.0)
        noise_level = entry_data.get("noise_level", 0.0)
        notion_id = entry_data.get("notion_id", "")
        content_source = entry_data.get("content_source", "不明")

        # 🔧 重要: 時刻フォーマット修正適用
        fixed_created_time = self._fix_datetime_format(raw_created_time)
        datetime_validation = self._validate_datetime_quality(
            raw_created_time, fixed_created_time
        )

        # 日時フォーマット（表示用）
        try:
            dt = datetime.fromisoformat(fixed_created_time.replace("Z", "+00:00"))
            formatted_time = dt.strftime("%Y年%m月%d日 %H:%M:%S")
        except:
            formatted_time = "時刻パースエラー"

        # 分類ラベル
        classification_label = (
            "💭 Personal Thoughts"
            if classification == "personal_thoughts"
            else "📥 Inbox Raw"
        )

        # 修正情報の追加
        fix_info = ""
        if datetime_validation["is_fixed"]:
            fix_info = f"""
# 🔧 時刻修正情報
- **元の時刻**: `{datetime_validation['original']}`
- **修正後時刻**: `{datetime_validation['fixed']}`
- **修正タイプ**: {datetime_validation['fix_type']}
- **修正日時**: {datetime.now(timezone.utc).isoformat()}

"""

        content = f"""---
source: SuperWhisper (Fixed)
created: {fixed_created_time}
classification: {classification_label}
quality_score: {quality_score:.2f}
noise_level: {noise_level:.2f}
notion_id: {notion_id}
personality_learning_ready: {classification == "personal_thoughts"}
content_source: {content_source}
datetime_fix_applied: {datetime_validation["is_fixed"]}
datetime_fix_type: {datetime_validation["fix_type"]}
processing_version: v2.1_datetime_fixed
---

# SuperWhisper 音声記録（時刻修正版）

**記録日時**: {formatted_time}  
**分類**: {classification_label}  
**品質スコア**: {quality_score:.1%}  
**本文取得元**: {content_source}

{fix_info}## 音声内容

{text_content}

## メタデータ

- **転写品質**: {quality_score:.1%}
- **ノイズレベル**: {noise_level:.1%}
- **文字数**: {len(text_content)}文字
- **PersonalityLearning投入対象**: {"✅ Yes" if classification == "personal_thoughts" else "⚠️ 要確認"}
- **本文取得元**: {content_source}
- **時刻修正適用**: {"✅ 適用済み" if datetime_validation["is_fixed"] else "不要"}
- **処理バージョン**: v2.1_datetime_fixed（時刻バグ修正版）

---
*SuperWhisper-Notion統合システム（時刻修正版）自動生成*
"""

        return content

    def test_datetime_fixes(self):
        """
        🧪 時刻修正機能のテスト
        """
        test_cases = [
            "2025-05-31",  # 問題のパターン
            "2025-05-31T00:30:00.000+00:00",  # 正常パターン
            "2025-05-31T00:30:00",  # タイムゾーンなし
            "",  # 空文字
            "invalid-date",  # 不正な形式
        ]

        print("🧪 時刻修正機能テスト開始")
        for i, test_case in enumerate(test_cases, 1):
            fixed = self._fix_datetime_format(test_case)
            validation = self._validate_datetime_quality(test_case, fixed)

            print(f"テスト{i}: {test_case or '(空文字)'}")
            print(f"  修正後: {fixed}")
            print(f"  修正タイプ: {validation['fix_type']}")
            print(f"  修正適用: {'はい' if validation['is_fixed'] else 'いいえ'}")
            print()


if __name__ == "__main__":
    # テスト実行
    integration = SuperWhisperNotionIntegrationFixed()
    integration.test_datetime_fixes()
