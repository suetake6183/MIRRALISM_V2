#!/usr/bin/env python3
"""
MIRRALISM時刻修正システム
正確な時刻取得と表示のための統一システム
"""

import datetime
import json
import locale
import os
from typing import Any
from typing import Dict
from typing import Optional

import pytz


class MIRRALISMTimeSystem:
    """MIRRALISM統一時刻システム"""

    def __init__(self):
        """時刻システム初期化"""
        self.jst = pytz.timezone("Asia/Tokyo")
        self.utc = pytz.UTC

        # 日本語ロケール設定試行
        try:
            locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, "Japanese_Japan.932")
            except locale.Error:
                # ロケール設定失敗時はデフォルトのまま
                pass

    def get_current_time_jst(self) -> datetime.datetime:
        """現在時刻をJSTで取得"""
        return datetime.datetime.now(self.jst)

    def get_current_time_utc(self) -> datetime.datetime:
        """現在時刻をUTCで取得"""
        return datetime.datetime.now(self.utc)

    def format_time_japanese(self, dt: Optional[datetime.datetime] = None) -> str:
        """日本語形式での時刻フォーマット"""
        if dt is None:
            dt = self.get_current_time_jst()

        return dt.strftime("%Y年%m月%d日 %H時%M分")

    def format_time_iso(self, dt: Optional[datetime.datetime] = None) -> str:
        """ISO形式での時刻フォーマット"""
        if dt is None:
            dt = self.get_current_time_jst()

        return dt.isoformat()

    def get_timestamp_info(self) -> Dict[str, Any]:
        """詳細なタイムスタンプ情報を取得"""
        now_jst = self.get_current_time_jst()
        now_utc = self.get_current_time_utc()

        return {
            "jst": {
                "datetime": now_jst.isoformat(),
                "formatted": self.format_time_japanese(now_jst),
                "unix_timestamp": now_jst.timestamp(),
                "timezone": "Asia/Tokyo",
            },
            "utc": {
                "datetime": now_utc.isoformat(),
                "formatted": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "unix_timestamp": now_utc.timestamp(),
                "timezone": "UTC",
            },
            "system_info": {
                "locale": locale.getlocale(locale.LC_TIME),
                "timezone_detected": str(now_jst.tzinfo),
            },
        }

    def validate_and_fix_timestamp(self, timestamp_str: str) -> Dict[str, Any]:
        """タイムスタンプの検証と修正"""
        result = {
            "original": timestamp_str,
            "is_valid": False,
            "fixed": None,
            "fix_applied": False,
            "error": None,
        }

        try:
            # ISO形式での解析試行
            if "T" in timestamp_str:
                dt = datetime.datetime.fromisoformat(
                    timestamp_str.replace("Z", "+00:00")
                )
                result["is_valid"] = True
                result["fixed"] = dt.isoformat()
            else:
                # 日付のみの場合は現在時刻で補完
                current = self.get_current_time_jst()
                result["fixed"] = current.isoformat()
                result["fix_applied"] = True

        except Exception as e:
            # 解析失敗時は現在時刻で代替
            current = self.get_current_time_jst()
            result["fixed"] = current.isoformat()
            result["fix_applied"] = True
            result["error"] = str(e)

        return result


def main():
    """時刻システムのテストと実証"""
    print("🕐 MIRRALISM時刻修正システム - 実行開始")
    print("=" * 50)

    time_sys = MIRRALISMTimeSystem()

    # 現在時刻情報の取得
    timestamp_info = time_sys.get_timestamp_info()

    print("📊 現在時刻情報:")
    print(f"JST: {timestamp_info['jst']['formatted']}")
    print(f"ISO形式: {timestamp_info['jst']['datetime']}")
    print(f"UTC: {timestamp_info['utc']['formatted']}")
    print(f"Unix: {timestamp_info['jst']['unix_timestamp']}")

    # レポート保存
    report_path = "mirralism_time_correction_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(timestamp_info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 時刻修正システム動作確認完了")
    print(f"📝 詳細レポート: {report_path}")

    return timestamp_info


if __name__ == "__main__":
    main()
