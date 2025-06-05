#!/usr/bin/env python3
"""
SuperWhisper-Notion統合システム（時刻バグ修正統合版）
作成者: 技術者
作成日: 2025年5月30日
修正日: 2025年6月3日（時刻バグ修正統合）
目的: SuperWhisper音声データのNotion取得とインボックス配置自動化

CTO戦略指示:
- Notion→インボックス配置戦略の実装
- 💭 Personal_Thoughts/ 優先配置
- 📥 Inbox_Raw/ 補完配置
- PersonalityLearning統合準備

🔧 重要な修正（v2.1）:
- 日本語環境での時刻フォーマット問題を根本解決
- ISO 8601完全形式の強制実装
- 不完全な時刻データのバリデーション・修正機能
- 00:00:00境界時刻での処理改善
"""

import json
import logging
import re
import sqlite3
import sys
import time
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import requests

# システムパス追加
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent.parent / "AI_Systems" / "Core"))


class SuperWhisperNotionIntegration:
    """SuperWhisper-Notion統合システム（時刻バグ修正版）"""

    def __init__(self, config_path: str = None):
        """
        システム初期化

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

        self.logger.info("SuperWhisper-Notion統合システム（時刻修正版）初期化完了")

    def _setup_logger(self) -> logging.Logger:
        """ログ設定"""
        logger = logging.getLogger("SuperWhisperNotionIntegration")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # ログディレクトリ
            log_dir = self.base_dir / ".system_internal" / "_LOGS"
            log_dir.mkdir(parents=True, exist_ok=True)

            # ファイルハンドラー
            log_file = log_dir / "superwhisper_integration.log"
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
                    quality_score REAL
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
                self.logger.warning(f"不完全な時刻データを修正: {raw_datetime} → {fixed_time}")
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
                self.logger.error(f"時刻パース失敗、現在時刻で代替: {raw_datetime} → {fixed_time}")
                return fixed_time

        except Exception as e:
            # 例外発生時は現在時刻で代替
            now = datetime.now(timezone.utc)
            fixed_time = now.isoformat()
            self.logger.error(f"時刻修正処理エラー ({raw_datetime}): {e} → {fixed_time}")
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

    def fetch_notion_entries(self, hours_back: int = 24) -> List[Dict[str, Any]]:
        """
        Notionから新規エントリを取得

        Args:
            hours_back: 何時間前まで遡るか

        Returns:
            新規エントリリスト
        """
        if not self.notion_token or not self.notion_database_id:
            self.logger.error("Notion API設定が不完全です")
            return []

        try:
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }

            # 時間範囲設定
            since_time = datetime.now() - timedelta(hours=hours_back)
            since_iso = since_time.isoformat()

            # クエリ構築
            query = {
                "filter": {"property": "日付", "date": {"after": since_iso}},
                "sorts": [{"property": "日付", "direction": "descending"}],
            }

            # Notion API呼び出し
            url = f"https://api.notion.com/v1/databases/{self.notion_database_id}/query"
            response = requests.post(url, headers=headers, json=query, timeout=30)

            if response.status_code == 200:
                data = response.json()
                entries = data.get("results", [])

                # 未処理エントリのフィルタリング
                new_entries = self._filter_unprocessed_entries(entries)

                self.logger.info(f"Notionから {len(new_entries)} 件の新規エントリを取得")
                return new_entries

            else:
                self.logger.error(
                    f"Notion API エラー: {response.status_code} - {response.text}"
                )
                return []

        except Exception as e:
            self.logger.error(f"Notion取得エラー: {e}")
            return []

    def _filter_unprocessed_entries(
        self, entries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """未処理エントリのフィルタリング"""
        try:
            conn = sqlite3.connect(str(self.processed_db))
            cursor = conn.cursor()

            new_entries = []
            for entry in entries:
                notion_id = entry["id"]
                cursor.execute(
                    "SELECT 1 FROM processed_entries WHERE notion_id = ?", (notion_id,)
                )

                if not cursor.fetchone():
                    new_entries.append(entry)

            conn.close()
            return new_entries

        except Exception as e:
            self.logger.error(f"未処理エントリフィルタリングエラー: {e}")
            return entries

    def classify_and_save_entry(self, entry: Dict[str, Any]) -> Optional[str]:
        """
        エントリの分類とファイル保存

        Args:
            entry: Notionエントリ

        Returns:
            保存されたファイルパス
        """
        try:
            # エントリデータ抽出
            entry_data = self._extract_entry_data(entry)

            if not entry_data:
                self.logger.warning(f"エントリデータ抽出失敗: {entry['id']}")
                return None

            # 品質評価・分類
            classification = self._classify_entry(entry_data)

            # ファイル保存
            file_path = self._save_entry_to_inbox(entry_data, classification)

            if file_path:
                # 処理済み記録
                self._mark_as_processed(
                    entry["id"],
                    file_path,
                    classification,
                    entry_data.get("quality_score", 0.0),
                )

                self.logger.info(f"エントリ保存完了: {file_path} ({classification})")
                return file_path

            return None

        except Exception as e:
            self.logger.error(f"エントリ分類・保存エラー: {e}")
            return None

    def _extract_entry_data(self, entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Notionエントリからデータ抽出"""
        try:
            properties = entry.get("properties", {})
            notion_id = entry.get("id", "")

            # ページ本文取得（Blocksエンドポイント）
            text_content = self._fetch_page_content(notion_id)

            # タイトル取得（フォールバック用）
            title = ""
            if "タイトル" in properties:
                title_prop = properties["タイトル"]
                if title_prop.get("title"):
                    title = title_prop["title"][0]["text"]["content"]

            # 既存のContent プロパティチェック（SuperWhisper用）
            content_from_property = ""
            if "Content" in properties:
                text_prop = properties["Content"]
                if text_prop["type"] == "rich_text" and text_prop["rich_text"]:
                    content_from_property = text_prop["rich_text"][0]["text"]["content"]

            # 日記プロパティから本文取得（良かったこと、課題、感謝していること等）
            diary_content_parts = []
            diary_properties = [
                "良かったこと",
                "課題",
                "感謝していること",
                "今日のタスク",
                "振り返り",
                "学び",
                "気づき",
            ]

            for prop_name in diary_properties:
                if prop_name in properties:
                    prop_data = properties[prop_name]
                    if prop_data.get("type") == "rich_text" and prop_data.get(
                        "rich_text"
                    ):
                        for text_obj in prop_data["rich_text"]:
                            content = text_obj.get("text", {}).get("content", "")
                            if content.strip():
                                diary_content_parts.append(
                                    f"**{prop_name}**\n{content}"
                                )

            # プロパティベースの日記本文
            diary_content = (
                "\n\n".join(diary_content_parts) if diary_content_parts else ""
            )

            # 最終的な本文決定の優先順位
            # 1. SuperWhisper用コンテンツ（明示的な音声転写）
            # 2. ページブロック本文
            # 3. 日記プロパティの組み合わせ
            # 4. タイトル
            final_content = ""
            if content_from_property:
                final_content = content_from_property
            elif text_content:
                final_content = text_content
            elif diary_content:
                final_content = diary_content
            else:
                final_content = title

            # メタデータ取得
            created_time = entry.get("created_time", "")

            # 転写品質評価
            quality_score = self._estimate_transcription_quality(final_content)

            # 音声品質評価
            noise_level = self._estimate_noise_level(final_content)

            return {
                "notion_id": notion_id,
                "text_content": final_content,
                "title": title,
                "created_time": created_time,
                "quality_score": quality_score,
                "noise_level": noise_level,
                "text_length": len(final_content),
                "content_source": self._get_content_source(
                    content_from_property, text_content, diary_content, title
                ),
            }

        except Exception as e:
            self.logger.error(f"エントリデータ抽出エラー: {e}")
            return None

    def _get_content_source(
        self, content_property: str, page_content: str, diary_content: str, title: str
    ) -> str:
        """本文の取得元を特定"""
        if content_property:
            return "SuperWhisper音声転写"
        elif page_content:
            return "Notionページブロック"
        elif diary_content:
            return "日記プロパティ"
        else:
            return "タイトル"

    def _fetch_page_content(self, page_id: str) -> str:
        """Notionページの本文ブロックを取得"""
        try:
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }

            return self._fetch_blocks_recursive(page_id, headers)

        except Exception as e:
            self.logger.error(f"ページコンテンツ取得例外: {e}")
            return ""

    def _fetch_blocks_recursive(self, block_id: str, headers: dict) -> str:
        """ブロックを再帰的に取得してテキストを抽出"""
        try:
            response = requests.get(
                f"https://api.notion.com/v1/blocks/{block_id}/children", headers=headers
            )

            if response.status_code != 200:
                error_response = response.json() if response.content else {}
                error_message = error_response.get("message", "")

                # transcriptionブロックエラーの場合は空文字を返す（タイトルから取得される）
                if "transcription is not supported" in error_message:
                    self.logger.debug(
                        f"transcriptionブロック検出 - タイトルから本文取得: {error_message}"
                    )
                    return ""

                self.logger.warning(
                    f"ブロック取得エラー: {response.status_code} - {response.text}"
                )
                return ""

            blocks = response.json().get("results", [])
            content_parts = []

            for block in blocks:
                block_type = block.get("type", "")
                block_id = block.get("id", "")

                # 各ブロックタイプからテキストを抽出
                text_content = self._extract_text_from_block(block, block_type)
                if text_content:
                    content_parts.append(text_content)

                # 子ブロックがある場合は再帰的に取得
                if block.get("has_children", False):
                    child_content = self._fetch_blocks_recursive(block_id, headers)
                    if child_content:
                        content_parts.append(child_content)

            # 空でない部分のみ結合
            filtered_parts = [part for part in content_parts if part.strip()]
            return "\n".join(filtered_parts).strip()

        except Exception as e:
            self.logger.error(f"再帰的ブロック取得エラー: {e}")
            return ""

    def _extract_text_from_block(self, block: dict, block_type: str) -> str:
        """ブロックからテキストを抽出"""
        try:
            # 段落ブロック
            if block_type == "paragraph":
                paragraph = block.get("paragraph", {})
                rich_text = paragraph.get("rich_text", [])
                return "\n".join(
                    [text_obj.get("plain_text", "") for text_obj in rich_text]
                )

            # 見出しブロック
            elif block_type in ["heading_1", "heading_2", "heading_3"]:
                heading = block.get(block_type, {})
                rich_text = heading.get("rich_text", [])
                level = block_type.split("_")[-1]  # 1, 2, 3
                prefix = "#" * int(level)
                texts = [text_obj.get("plain_text", "") for text_obj in rich_text]
                return f"{prefix} {' '.join(texts)}"

            # 箇条書きブロック
            elif block_type == "bulleted_list_item":
                list_item = block.get("bulleted_list_item", {})
                rich_text = list_item.get("rich_text", [])
                texts = [text_obj.get("plain_text", "") for text_obj in rich_text]
                return f"- {' '.join(texts)}"

            # 番号付きリストブロック
            elif block_type == "numbered_list_item":
                list_item = block.get("numbered_list_item", {})
                rich_text = list_item.get("rich_text", [])
                texts = [text_obj.get("plain_text", "") for text_obj in rich_text]
                return f"1. {' '.join(texts)}"

            # コードブロック
            elif block_type == "code":
                code_block = block.get("code", {})
                rich_text = code_block.get("rich_text", [])
                texts = [text_obj.get("plain_text", "") for text_obj in rich_text]
                return f"```\n{' '.join(texts)}\n```"

            # 引用ブロック
            elif block_type == "quote":
                quote_block = block.get("quote", {})
                rich_text = quote_block.get("rich_text", [])
                texts = [text_obj.get("plain_text", "") for text_obj in rich_text]
                return f"> {' '.join(texts)}"

            # テーブルオブコンテンツ
            elif block_type == "table_of_contents":
                return "[目次]"

            # 区切り線
            elif block_type == "divider":
                return "---"

            # Toggleブロック
            elif block_type == "toggle":
                toggle_block = block.get("toggle", {})
                rich_text = toggle_block.get("rich_text", [])
                texts = [text_obj.get("plain_text", "") for text_obj in rich_text]
                return f"▶ {' '.join(texts)}"

            # Calloutブロック
            elif block_type == "callout":
                callout_block = block.get("callout", {})
                rich_text = callout_block.get("rich_text", [])
                texts = [text_obj.get("plain_text", "") for text_obj in rich_text]
                return f"💡 {' '.join(texts)}"

            # unsupportedブロック - 子ブロックに依存
            elif block_type == "unsupported":
                return ""  # 子ブロックで処理される

            # その他の不明なブロックタイプ
            else:
                # 汎用的なrich_text取得試行
                block_data = block.get(block_type, {})
                if isinstance(block_data, dict) and "rich_text" in block_data:
                    rich_text = block_data.get("rich_text", [])
                    texts = [text_obj.get("plain_text", "") for text_obj in rich_text]
                    return " ".join(texts)
                else:
                    self.logger.debug(f"未対応ブロックタイプ: {block_type}")
                    return ""

        except Exception as e:
            self.logger.error(f"ブロックテキスト抽出エラー: {e}")
            return ""

    def _estimate_transcription_quality(self, text: str) -> float:
        """転写品質推定（仮実装）"""
        try:
            if not text:
                return 0.0

            # 簡易品質評価指標
            quality_indicators = 0
            total_indicators = 5

            # 1. 文字数チェック
            if len(text) >= self.config.get("min_text_length", 20):
                quality_indicators += 1

            # 2. 句読点存在チェック
            if any(punct in text for punct in "。、．，"):
                quality_indicators += 1

            # 3. 不明文字チェック
            unknown_chars = text.count("？") + text.count("〇") + text.count("※")
            if unknown_chars / len(text) < 0.1:  # 10%未満
                quality_indicators += 1

            # 4. 連続する同じ文字チェック
            has_repetition = any(
                text[i] == text[i + 1] == text[i + 2] for i in range(len(text) - 2)
            )
            if not has_repetition:
                quality_indicators += 1

            # 5. 基本的な文章構造
            if len(text.split()) >= 3:  # 最低3単語
                quality_indicators += 1

            return quality_indicators / total_indicators

        except Exception as e:
            self.logger.error(f"品質推定エラー: {e}")
            return 0.5  # デフォルト中間値

    def _estimate_noise_level(self, text: str) -> float:
        """ノイズレベル推定（仮実装）"""
        try:
            if not text:
                return 1.0  # 高ノイズ

            # ノイズ指標

            # 意味不明な文字列
            noise_chars = text.count("あー") + text.count("えー") + text.count("うー")
            noise_ratio = noise_chars / len(text)

            return min(noise_ratio * 2, 1.0)  # 0-1の範囲

        except Exception as e:
            self.logger.error(f"ノイズレベル推定エラー: {e}")
            return 0.5

    def _classify_entry(self, entry_data: Dict[str, Any]) -> str:
        """エントリ分類"""
        quality_threshold = self.config.get("quality_threshold", 0.9)
        min_text_length = self.config.get("min_text_length", 20)
        max_noise_level = self.config.get("max_noise_level", 0.3)

        quality_score = entry_data.get("quality_score", 0.0)
        text_length = entry_data.get("text_length", 0)
        noise_level = entry_data.get("noise_level", 1.0)

        # 💭 Personal_Thoughts/ 配置条件
        if (
            quality_score >= quality_threshold
            and text_length >= min_text_length
            and noise_level <= max_noise_level
        ):
            return "personal_thoughts"

        # 📥 Inbox_Raw/ 配置条件
        return "inbox_raw"

    def _save_entry_to_inbox(
        self, entry_data: Dict[str, Any], classification: str
    ) -> Optional[str]:
        """インボックスへのファイル保存"""
        try:
            # 保存先ディレクトリ決定
            if classification == "personal_thoughts":
                save_dir = self.personal_thoughts_dir
                prefix = "superwhisper"
            else:
                save_dir = self.inbox_raw_dir
                prefix = "superwhisper_raw"

            # ファイル名生成
            created_time = entry_data.get("created_time", "")
            if created_time:
                dt = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
                timestamp = dt.strftime("%Y%m%d_%H%M%S")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            filename = f"{prefix}_{timestamp}.md"
            file_path = save_dir / filename

            # ファイル内容作成
            content = self._create_file_content(entry_data, classification)

            # ファイル保存
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return str(file_path)

        except Exception as e:
            self.logger.error(f"ファイル保存エラー: {e}")
            return None

    def _create_file_content(
        self, entry_data: Dict[str, Any], classification: str
    ) -> str:
        """保存ファイルの内容作成（🔧時刻バグ修正統合版）"""
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

        # 修正情報の追加（デバッグ用・修正適用時のみ）
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
source: SuperWhisper{" (Fixed)" if datetime_validation["is_fixed"] else ""}
created: {fixed_created_time}
classification: {classification_label}
quality_score: {quality_score:.2f}
noise_level: {noise_level:.2f}
notion_id: {notion_id}
personality_learning_ready: {classification == "personal_thoughts"}
content_source: {content_source}{f'''
datetime_fix_applied: {datetime_validation["is_fixed"]}
datetime_fix_type: {datetime_validation["fix_type"]}
processing_version: v2.1_datetime_fixed''' if datetime_validation["is_fixed"] else ""}
---

# SuperWhisper 音声記録{" (時刻修正版)" if datetime_validation["is_fixed"] else ""}

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
- **本文取得元**: {content_source}{f'''
- **時刻修正適用**: ✅ 適用済み（{datetime_validation["fix_type"]}）
- **処理バージョン**: v2.1_datetime_fixed（時刻バグ修正版）''' if datetime_validation["is_fixed"] else ""}

---
*SuperWhisper-Notion統合システム{"（時刻修正版）" if datetime_validation["is_fixed"] else ""}自動生成*
"""

        return content

    def _mark_as_processed(
        self, notion_id: str, file_path: str, classification: str, quality_score: float
    ):
        """処理済みマーク"""
        try:
            conn = sqlite3.connect(str(self.processed_db))
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO processed_entries
                (notion_id, file_path, classification, quality_score)
                VALUES (?, ?, ?, ?)
            """,
                (notion_id, file_path, classification, quality_score),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"処理済みマークエラー: {e}")

    def monitor_and_process(self, single_run: bool = False) -> int:
        """
        継続監視・処理実行

        Args:
            single_run: 一回のみ実行するか

        Returns:
            処理件数
        """
        processed_count = 0

        try:
            self.logger.info("SuperWhisper-Notion監視開始")

            while True:
                try:
                    # Notionから新規エントリ取得
                    entries = self.fetch_notion_entries()

                    # エントリ処理
                    for entry in entries:
                        file_path = self.classify_and_save_entry(entry)
                        if file_path:
                            processed_count += 1

                    if entries:
                        self.logger.info(f"バッチ処理完了: {len(entries)}件処理")

                    # 一回のみ実行の場合は終了
                    if single_run:
                        break

                    # 監視間隔待機
                    interval = self.config.get("monitor_interval", 300)
                    self.logger.debug(f"{interval}秒待機中...")
                    time.sleep(interval)

                except KeyboardInterrupt:
                    self.logger.info("監視停止が要求されました")
                    break
                except Exception as e:
                    self.logger.error(f"監視ループエラー: {e}")
                    time.sleep(60)  # エラー時は1分待機

            self.logger.info(f"監視終了 - 総処理件数: {processed_count}")
            return processed_count

        except Exception as e:
            self.logger.error(f"監視システムエラー: {e}")
            return processed_count


def main():
    """メイン実行"""
    import argparse

    parser = argparse.ArgumentParser(description="SuperWhisper-Notion統合システム")
    parser.add_argument("--single-run", action="store_true", help="一回のみ実行")
    parser.add_argument("--config", help="設定ファイルパス")

    args = parser.parse_args()

    try:
        integration = SuperWhisperNotionIntegration(args.config)
        processed_count = integration.monitor_and_process(single_run=args.single_run)

        print(f"✅ 処理完了: {processed_count}件のエントリを処理しました")

    except Exception as e:
        print(f"❌ システムエラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
