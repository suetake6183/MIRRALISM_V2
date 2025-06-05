#!/usr/bin/env python3
"""プロセス監視による制約強制"""
import os
import sys
import time

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil not available - process monitoring disabled")


def monitor_file_creation():
    """ファイル作成プロセス監視"""
    if not PSUTIL_AVAILABLE:
        print("⚠️ psutil not available - monitoring disabled")
        return

    forbidden_patterns = ["REDIRECT", "redirect"]

    while True:
        try:
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    cmdline = proc.info["cmdline"]
                    if cmdline and any(
                        pattern in " ".join(cmdline) for pattern in forbidden_patterns
                    ):
                        print(f"⚠️ 制約違反プロセス検知: {proc.info['name']} - {cmdline}")
                        # プロセス停止は危険なので警告のみ
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    monitor_file_creation()
