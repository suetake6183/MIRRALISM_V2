#!/usr/bin/env python3
"""
ClaudeCode 完全自動化ツール
===========================

目的: ClaudeCodeのダイアログ確認を自動でYesクリック
方針: 画面監視 + 自動クリックによる完全自動化
作成日: 2025年6月6日
"""

import time
import threading
import subprocess
import json
import logging
from datetime import datetime
from pathlib import Path
import signal
import sys

# macOS専用: pyautogui
try:
    import pyautogui
    pyautogui.FAILSAFE = True  # マウスを左上角に移動で緊急停止
except ImportError:
    print("pyautogui not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui

# 画像認識用: opencv
try:
    import cv2
    import numpy as np
except ImportError:
    print("opencv-python not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python"])
    import cv2
    import numpy as np


class ClaudeAutoClicker:
    """ClaudeCode自動クリックシステム"""
    
    def __init__(self):
        self.running = False
        self.click_count = 0
        self.log_file = Path(".mirralism/claude_auto_clicker.log")
        self.config_file = Path(".mirralism/claude_auto_clicker_config.json")
        
        # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - AUTO_CLICKER - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 設定ロード
        self.config = self.load_config()
        
        # 監視対象のボタンテキスト（優先順位順）
        self.target_buttons = [
            "Yes",
            "OK", 
            "Allow",
            "Continue",
            "Proceed",
            "Confirm",
            "はい",
            "OK",
            "許可",
            "続行",
            "確認"
        ]
        
        # Claude特有のダイアログパターン
        self.claude_patterns = [
            "Do you want to",
            "Would you like to", 
            "Shall I",
            "Continue with",
            "Proceed with",
            "Allow Claude to"
        ]
    
    def load_config(self):
        """設定ファイル読み込み"""
        default_config = {
            "enabled": True,
            "scan_interval": 0.5,  # 0.5秒間隔でスキャン
            "click_delay": 0.1,    # クリック前の待機時間
            "confidence": 0.8,     # 画像認識の信頼度
            "auto_modes": {
                "aggressive": True,    # 積極的自動化
                "conservative": False, # 保守的自動化
                "claude_only": False   # Claude関連のみ
            },
            "excluded_apps": [
                "System Preferences",
                "Finder", 
                "Terminal"
            ]
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # デフォルト設定とマージ
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                self.logger.warning(f"設定ファイル読み込み失敗: {e}, デフォルト設定使用")
        
        # デフォルト設定保存
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config=None):
        """設定ファイル保存"""
        if config is None:
            config = self.config
            
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get_active_app(self):
        """現在のアクティブアプリケーション取得"""
        try:
            script = '''
            tell application "System Events"
                return name of first application process whose frontmost is true
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        except Exception:
            return ""
    
    def is_claude_dialog(self):
        """ClaudeCode関連のダイアログかチェック"""
        try:
            # ウィンドウタイトルをチェック
            script = '''
            tell application "System Events"
                return name of front window of first application process whose frontmost is true
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            window_title = result.stdout.strip()
            
            # Claude関連キーワードチェック
            claude_keywords = [
                "Claude", "claude", "CLAUDE",
                "Terminal", "Code", "VS Code",
                "confirmation", "confirm"
            ]
            
            return any(keyword in window_title for keyword in claude_keywords)
        except Exception:
            return True  # エラー時は安全のためTrueを返す
    
    def find_and_click_button(self):
        """ボタンを探して自動クリック"""
        try:
            # アクティブアプリチェック
            active_app = self.get_active_app()
            if active_app in self.config["excluded_apps"]:
                return False
            
            # Claude関連チェック（claude_onlyモードの場合）
            if self.config["auto_modes"]["claude_only"] and not self.is_claude_dialog():
                return False
            
            # AppleScriptでボタン検索・クリック
            for button_text in self.target_buttons:
                try:
                    script = f'''
                    tell application "System Events"
                        tell process "{active_app}"
                            if exists button "{button_text}" of front window then
                                click button "{button_text}" of front window
                                return true
                            end if
                        end tell
                    end tell
                    return false
                    '''
                    
                    result = subprocess.run(['osascript', '-e', script], 
                                          capture_output=True, text=True, timeout=2)
                    
                    if result.stdout.strip() == "true":
                        self.click_count += 1
                        self.logger.info(f"自動クリック実行: {button_text} in {active_app}")
                        return True
                        
                except subprocess.TimeoutExpired:
                    continue
                except Exception as e:
                    self.logger.debug(f"ボタン検索エラー ({button_text}): {e}")
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"自動クリック処理エラー: {e}")
            return False
    
    def monitor_loop(self):
        """メイン監視ループ"""
        self.logger.info("🤖 ClaudeCode自動クリック監視開始")
        
        while self.running:
            try:
                if self.config["enabled"]:
                    if self.find_and_click_button():
                        # クリック後の待機
                        time.sleep(self.config["click_delay"] * 2)
                
                time.sleep(self.config["scan_interval"])
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"監視ループエラー: {e}")
                time.sleep(1)
        
        self.logger.info("🛑 ClaudeCode自動クリック監視終了")
    
    def start(self):
        """自動クリック開始"""
        if self.running:
            print("既に実行中です")
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print("🚀 ClaudeCode自動クリック開始!")
        print("   停止: Ctrl+C または claude_auto_clicker.py --stop")
        print(f"   設定: {self.config_file}")
        print(f"   ログ: {self.log_file}")
    
    def stop(self):
        """自動クリック停止"""
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        
        print(f"🛑 自動クリック停止 (総クリック数: {self.click_count})")
    
    def status(self):
        """現在の状態表示"""
        print("📊 ClaudeCode自動クリック状態")
        print("=" * 40)
        print(f"状態: {'✅ 実行中' if self.running else '⏹️ 停止中'}")
        print(f"有効: {'✅' if self.config['enabled'] else '❌'}")
        print(f"総クリック数: {self.click_count}")
        print(f"スキャン間隔: {self.config['scan_interval']}秒")
        print(f"モード: {[k for k, v in self.config['auto_modes'].items() if v]}")
        print(f"除外アプリ: {self.config['excluded_apps']}")
    
    def configure(self, mode=None, interval=None, enable=None):
        """設定変更"""
        if enable is not None:
            self.config["enabled"] = enable
            print(f"自動クリック: {'有効' if enable else '無効'}")
        
        if interval is not None:
            self.config["scan_interval"] = interval
            print(f"スキャン間隔: {interval}秒")
        
        if mode:
            # 全モードリセット
            for key in self.config["auto_modes"]:
                self.config["auto_modes"][key] = False
            # 指定モード有効化
            if mode in self.config["auto_modes"]:
                self.config["auto_modes"][mode] = True
                print(f"モード変更: {mode}")
        
        self.save_config()


def signal_handler(sig, frame):
    """シグナルハンドラー"""
    print("\n🛑 終了シグナル受信")
    if 'auto_clicker' in globals():
        auto_clicker.stop()
    sys.exit(0)


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ClaudeCode自動クリックツール')
    parser.add_argument('--start', action='store_true', help='自動クリック開始')
    parser.add_argument('--stop', action='store_true', help='自動クリック停止')
    parser.add_argument('--status', action='store_true', help='状態確認')
    parser.add_argument('--enable', action='store_true', help='自動クリック有効化')
    parser.add_argument('--disable', action='store_true', help='自動クリック無効化')
    parser.add_argument('--mode', choices=['aggressive', 'conservative', 'claude_only'], 
                      help='動作モード設定')
    parser.add_argument('--interval', type=float, help='スキャン間隔(秒)')
    
    args = parser.parse_args()
    
    global auto_clicker
    auto_clicker = ClaudeAutoClicker()
    
    # シグナルハンドラー設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        if args.stop:
            auto_clicker.stop()
        elif args.status:
            auto_clicker.status()
        elif args.enable:
            auto_clicker.configure(enable=True)
        elif args.disable:
            auto_clicker.configure(enable=False)
        elif args.mode or args.interval:
            auto_clicker.configure(mode=args.mode, interval=args.interval)
        else:
            # デフォルト: 開始
            auto_clicker.start()
            
            # 無限待機（Ctrl+Cで終了）
            try:
                while auto_clicker.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            finally:
                auto_clicker.stop()
                
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()