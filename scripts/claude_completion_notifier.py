#!/usr/bin/env python3
"""
ClaudeCode作業完了通知システム
=============================

ClaudeCodeでの作業が完了した際に音声通知を行うシステム
macOS環境での様々な通知方法に対応

使用方法:
    python scripts/claude_completion_notifier.py --play success
    python scripts/claude_completion_notifier.py --play error  
    python scripts/claude_completion_notifier.py --custom "作業が完了しました"
    python scripts/claude_completion_notifier.py --enable-auto
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class ClaudeCompletionNotifier:
    """ClaudeCode作業完了通知システム"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.config_path = self.project_root / ".mirralism" / "notification_config.json"
        self.log_path = self.project_root / ".mirralism" / "logs" / "notifications.log"
        
        # ログ設定
        self.setup_logging()
        
        # 設定読み込み
        self.config = self.load_config()
        
        self.logger.info("ClaudeCode作業完了通知システム初期化完了")

    def setup_logging(self):
        """ログ設定"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - CLAUDE_NOTIFY - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self) -> Dict:
        """設定ファイル読み込み"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("設定ファイルが見つかりません。デフォルト設定を使用します。")
            return self.get_default_config()
        except Exception as e:
            self.logger.error(f"設定ファイル読み込みエラー: {e}")
            return self.get_default_config()

    def get_default_config(self) -> Dict:
        """デフォルト設定"""
        return {
            "notification_settings": {
                "enabled": True,
                "auto_notify": False,
                "sound_enabled": True,
                "voice_enabled": False,
                "visual_enabled": True
            },
            "sound_settings": {
                "success_sound": "Glass",
                "error_sound": "Basso", 
                "warning_sound": "Ping",
                "completion_sound": "Hero",
                "custom_sounds_dir": str(self.project_root / "sounds")
            },
            "voice_settings": {
                "voice": "Kyoko",  # 日本語音声
                "rate": 200,       # 話速
                "volume": 0.8      # 音量
            },
            "auto_detection": {
                "success_patterns": [
                    "完了", "成功", "✅", "finished", "completed", "success"
                ],
                "error_patterns": [
                    "エラー", "失敗", "❌", "error", "failed", "exception"
                ],
                "warning_patterns": [
                    "警告", "注意", "⚠️", "warning", "caution"
                ]
            },
            "usage_stats": {
                "notifications_sent": 0,
                "last_notification": None
            }
        }

    def save_config(self):
        """設定ファイル保存"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.logger.info("設定ファイルを保存しました")
        except Exception as e:
            self.logger.error(f"設定ファイル保存エラー: {e}")

    def play_system_sound(self, sound_name: str):
        """macOSシステム音再生"""
        try:
            # afplayコマンドでシステム音を再生
            sound_path = f"/System/Library/Sounds/{sound_name}.aiff"
            if os.path.exists(sound_path):
                subprocess.run(["afplay", sound_path], check=True)
                self.logger.info(f"システム音再生: {sound_name}")
            else:
                # 代替としてsayコマンドでビープ音
                subprocess.run(["say", "beep"], check=True)
                self.logger.warning(f"システム音が見つかりません: {sound_name}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"音声再生エラー: {e}")
        except Exception as e:
            self.logger.error(f"予期しないエラー: {e}")

    def speak_message(self, message: str):
        """音声メッセージ読み上げ"""
        try:
            voice_settings = self.config.get("voice_settings", {})
            voice = voice_settings.get("voice", "Kyoko")
            rate = voice_settings.get("rate", 200)
            
            # sayコマンドで音声読み上げ
            subprocess.run([
                "say", 
                "-v", voice,
                "-r", str(rate),
                message
            ], check=True)
            
            self.logger.info(f"音声メッセージ再生: {message}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"音声読み上げエラー: {e}")
        except Exception as e:
            self.logger.error(f"予期しないエラー: {e}")

    def show_notification(self, title: str, message: str, sound: Optional[str] = None):
        """macOS通知センターに通知表示"""
        try:
            # osascriptでAppleScriptを実行して通知表示
            script = f'''
            display notification "{message}" with title "{title}"
            '''
            
            if sound:
                script = f'''
                display notification "{message}" with title "{title}" sound name "{sound}"
                '''
            
            subprocess.run(["osascript", "-e", script], check=True)
            self.logger.info(f"通知表示: {title} - {message}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"通知表示エラー: {e}")
        except Exception as e:
            self.logger.error(f"予期しないエラー: {e}")

    def detect_completion_type(self, message: str) -> str:
        """メッセージから完了タイプを検出"""
        message_lower = message.lower()
        
        patterns = self.config.get("auto_detection", {})
        
        # エラーパターンチェック（優先度高）
        for pattern in patterns.get("error_patterns", []):
            if pattern.lower() in message_lower:
                return "error"
        
        # 警告パターンチェック
        for pattern in patterns.get("warning_patterns", []):
            if pattern.lower() in message_lower:
                return "warning"
        
        # 成功パターンチェック
        for pattern in patterns.get("success_patterns", []):
            if pattern.lower() in message_lower:
                return "success"
        
        # デフォルト
        return "completion"

    def notify_completion(self, message: str = "作業が完了しました", completion_type: str = "auto"):
        """作業完了通知"""
        
        # 通知が無効の場合はスキップ
        if not self.config.get("notification_settings", {}).get("enabled", True):
            self.logger.info("通知が無効のためスキップ")
            return
        
        # 完了タイプの自動検出
        if completion_type == "auto":
            completion_type = self.detect_completion_type(message)
        
        # 通知内容の決定
        notification_config = {
            "success": {
                "title": "✅ Claude作業完了",
                "sound": self.config.get("sound_settings", {}).get("success_sound", "Glass"),
                "voice_message": f"作業が正常に完了しました。{message}"
            },
            "error": {
                "title": "❌ Claude作業エラー", 
                "sound": self.config.get("sound_settings", {}).get("error_sound", "Basso"),
                "voice_message": f"エラーが発生しました。{message}"
            },
            "warning": {
                "title": "⚠️ Claude作業警告",
                "sound": self.config.get("sound_settings", {}).get("warning_sound", "Ping"),
                "voice_message": f"注意が必要です。{message}"
            },
            "completion": {
                "title": "🎯 Claude作業完了",
                "sound": self.config.get("sound_settings", {}).get("completion_sound", "Hero"),
                "voice_message": f"作業を完了しました。{message}"
            }
        }
        
        config = notification_config.get(completion_type, notification_config["completion"])
        
        # 各種通知実行
        settings = self.config.get("notification_settings", {})
        
        # 音声通知
        if settings.get("sound_enabled", True):
            self.play_system_sound(config["sound"])
        
        # 音声読み上げ（無効のままにする）
        if settings.get("voice_enabled", False):
            self.speak_message(config["voice_message"])
        
        # 視覚的通知
        if settings.get("visual_enabled", True):
            self.show_notification(config["title"], message, config["sound"])
        
        # 統計更新
        self.update_stats()
        
        self.logger.info(f"完了通知送信: {completion_type} - {message}")

    def update_stats(self):
        """使用統計更新"""
        stats = self.config.get("usage_stats", {})
        stats["notifications_sent"] = stats.get("notifications_sent", 0) + 1
        stats["last_notification"] = datetime.now().isoformat()
        self.config["usage_stats"] = stats
        self.save_config()

    def enable_auto_notification(self):
        """自動通知を有効化"""
        self.config["notification_settings"]["auto_notify"] = True
        self.save_config()
        settings = self.config.get("notification_settings", {})
        print("✅ ClaudeCode自動通知が有効になりました")
        print("📋 設定:")
        print(f"   音声通知: {'有効' if settings.get('sound_enabled', True) else '無効'}")
        print(f"   音声読み上げ: {'有効' if settings.get('voice_enabled', False) else '無効'}")
        print(f"   視覚的通知: {'有効' if settings.get('visual_enabled', True) else '無効'}")
        print("   自動検出: 有効")

    def disable_auto_notification(self):
        """自動通知を無効化"""
        self.config["notification_settings"]["auto_notify"] = False
        self.save_config()
        print("⚠️ ClaudeCode自動通知が無効になりました")

    def test_notifications(self):
        """通知テスト"""
        print("🧪 ClaudeCode通知システムテスト開始")
        
        test_cases = [
            ("success", "テスト作業が正常に完了しました"),
            ("error", "テストエラーが発生しました"),
            ("warning", "テスト警告: 注意が必要です"),
            ("completion", "通常のテスト作業完了です")
        ]
        
        for completion_type, message in test_cases:
            print(f"\n🔊 {completion_type.upper()}通知テスト...")
            self.notify_completion(message, completion_type)
            
            # 少し待機
            import time
            time.sleep(2)
        
        print("\n✅ 通知システムテスト完了")

    def show_status(self):
        """現在の状態表示"""
        settings = self.config.get("notification_settings", {})
        stats = self.config.get("usage_stats", {})
        
        print("📊 ClaudeCode通知システム状態")
        print("=" * 40)
        print(f"状態: {'✅ 有効' if settings.get('enabled', True) else '❌ 無効'}")
        print(f"自動通知: {'✅ 有効' if settings.get('auto_notify', False) else '❌ 無効'}")
        print(f"音声通知: {'✅ 有効' if settings.get('sound_enabled', True) else '❌ 無効'}")
        print(f"音声読み上げ: {'✅ 有効' if settings.get('voice_enabled', True) else '❌ 無効'}")
        print(f"視覚的通知: {'✅ 有効' if settings.get('visual_enabled', True) else '❌ 無効'}")
        print(f"通知送信回数: {stats.get('notifications_sent', 0)}回")
        print(f"最終通知: {stats.get('last_notification', 'なし')}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="ClaudeCode作業完了通知システム")
    parser.add_argument("--play", choices=["success", "error", "warning", "completion"], 
                       help="指定されたタイプの通知を再生")
    parser.add_argument("--custom", type=str, help="カスタムメッセージで通知")
    parser.add_argument("--enable-auto", action="store_true", help="自動通知を有効化")
    parser.add_argument("--disable-auto", action="store_true", help="自動通知を無効化")
    parser.add_argument("--test", action="store_true", help="通知システムテスト")
    parser.add_argument("--status", action="store_true", help="現在の状態を表示")
    
    args = parser.parse_args()
    
    notifier = ClaudeCompletionNotifier()
    
    if args.play:
        notifier.notify_completion(f"{args.play.upper()}タイプの通知テストです", args.play)
    elif args.custom:
        notifier.notify_completion(args.custom)
    elif args.enable_auto:
        notifier.enable_auto_notification()
    elif args.disable_auto:
        notifier.disable_auto_notification()
    elif args.test:
        notifier.test_notifications()
    elif args.status:
        notifier.show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()