#!/usr/bin/env python3
"""
MIRRALISM制約強制エンジン - V1問題の技術的根絶
設計思想: 制約ファースト設計の技術実装

目的:
- 分散ファイル生成の物理的阻止
- REDIRECT生成の技術的防止
- 測定値不整合の自動検知・修正
- V1問題パターンの永続的根絶

原則:
- 問題発生前の予防的阻止
- 技術的制約による品質強制
- 自動監視・自動修正
- 違反時の即座対応
"""

import os
import sqlite3
import shutil
import time
import json
import hashlib
import threading
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [CONSTRAINT] - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mirralism_constraint_engine.log"),
        logging.StreamHandler(),
    ],
)


class MirralismConstraintEngine:
    """MIRRALISM制約強制エンジン"""

    def __init__(self, project_root="/Users/suetakeshuuhei/MIRRALISM_V2"):
        self.project_root = Path(project_root)
        self.unified_db = (
            self.project_root / "Core/PersonalityLearning/MIRRALISM_UNIFIED.db"
        )
        self.constraints_config = self.project_root / ".mirralism/constraints.json"
        self.violation_log = self.project_root / ".mirralism/violations.log"

        # 制約設定
        self.max_personality_files = 1  # personality_learningファイルは1個のみ
        self.max_redirect_files = 0  # REDIRECTファイルは0個（完全禁止）
        self.max_duplicate_dbs = 1  # 重複DBは1個のみ

        # 監視対象パターン
        self.forbidden_patterns = [
            "*REDIRECT*",
            "*personality_learning*.db",
            "*duplicate*",
            "*copy*",
            "*backup*",
        ]

        # 許可されたファイル
        self.allowed_files = {
            str(self.unified_db),
            str(self.project_root / "ESSENTIAL_EXTRACTED"),
            str(self.project_root / ".mirralism"),
        }

        self.observer = None
        self.is_monitoring = False

    def initialize_constraints_system(self):
        """制約システム初期化"""
        logging.info("Initializing MIRRALISM Constraint Engine...")

        # 制約設定ディレクトリ作成
        os.makedirs(self.project_root / ".mirralism", exist_ok=True)

        # 制約設定ファイル作成
        constraints = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "constraints": {
                "max_personality_files": self.max_personality_files,
                "max_redirect_files": self.max_redirect_files,
                "max_duplicate_dbs": self.max_duplicate_dbs,
                "forbidden_patterns": self.forbidden_patterns,
                "allowed_files": [str(f) for f in self.allowed_files],
            },
            "enforcement_rules": {
                "auto_delete_violations": True,
                "backup_before_delete": True,
                "send_notifications": True,
                "log_all_actions": True,
            },
        }

        with open(self.constraints_config, "w") as f:
            json.dump(constraints, f, indent=2)

        logging.info(f"Constraints configuration saved: {self.constraints_config}")

    def scan_violations(self) -> Dict[str, List[str]]:
        """制約違反ファイルのスキャン"""
        violations = {
            "personality_learning_files": [],
            "redirect_files": [],
            "duplicate_dbs": [],
            "other_violations": [],
        }

        # personality_learningファイルのスキャン
        personality_files = list(self.project_root.rglob("*personality_learning*"))
        for file in personality_files:
            if str(file) != str(self.unified_db):
                violations["personality_learning_files"].append(str(file))

        # REDIRECTファイルのスキャン
        redirect_files = list(self.project_root.rglob("*REDIRECT*"))
        violations["redirect_files"] = [str(f) for f in redirect_files]

        # 重複DBのスキャン
        db_files = list(self.project_root.rglob("*.db"))
        for file in db_files:
            if str(file) != str(self.unified_db) and "personality" in str(file).lower():
                violations["duplicate_dbs"].append(str(file))

        return violations

    def quarantine_violation(self, violation_file: str) -> bool:
        """違反ファイルの隔離"""
        try:
            source = Path(violation_file)
            if not source.exists():
                return True  # 既に削除済み

            # 隔離ディレクトリ作成
            quarantine_dir = (
                self.project_root
                / ".mirralism/quarantine"
                / datetime.now().strftime("%Y%m%d")
            )
            os.makedirs(quarantine_dir, exist_ok=True)

            # ファイル名に時刻を追加
            timestamp = datetime.now().strftime("%H%M%S")
            quarantine_file = quarantine_dir / f"{timestamp}_{source.name}"

            # 隔離実行
            shutil.move(str(source), str(quarantine_file))

            # 違反ログ記録
            violation_record = {
                "timestamp": datetime.now().isoformat(),
                "original_path": str(source),
                "quarantine_path": str(quarantine_file),
                "file_size": quarantine_file.stat().st_size,
                "action": "quarantined",
            }

            with open(self.violation_log, "a") as f:
                f.write(json.dumps(violation_record) + "\n")

            logging.warning(f"VIOLATION QUARANTINED: {source} -> {quarantine_file}")
            return True

        except Exception as e:
            logging.error(f"Failed to quarantine {violation_file}: {e}")
            return False

    def enforce_constraints(self) -> Dict[str, int]:
        """制約強制実行"""
        logging.info("Starting constraint enforcement...")

        violations = self.scan_violations()
        enforcement_results = {
            "personality_learning_removed": 0,
            "redirect_removed": 0,
            "duplicate_dbs_removed": 0,
            "total_violations_found": 0,
            "total_violations_resolved": 0,
        }

        # 違反ファイル総数カウント
        total_violations = sum(len(v) for v in violations.values())
        enforcement_results["total_violations_found"] = total_violations

        if total_violations == 0:
            logging.info("No constraint violations found.")
            return enforcement_results

        logging.warning(f"Found {total_violations} constraint violations:")
        for category, files in violations.items():
            if files:
                logging.warning(f"  {category}: {len(files)} files")

        # personality_learningファイルの制約強制
        for file in violations["personality_learning_files"]:
            if self.quarantine_violation(file):
                enforcement_results["personality_learning_removed"] += 1
                enforcement_results["total_violations_resolved"] += 1

        # REDIRECTファイルの制約強制
        for file in violations["redirect_files"]:
            if self.quarantine_violation(file):
                enforcement_results["redirect_removed"] += 1
                enforcement_results["total_violations_resolved"] += 1

        # 重複DBの制約強制
        for file in violations["duplicate_dbs"]:
            if self.quarantine_violation(file):
                enforcement_results["duplicate_dbs_removed"] += 1
                enforcement_results["total_violations_resolved"] += 1

        logging.info(
            f"Constraint enforcement completed. Resolved {enforcement_results['total_violations_resolved']}/{total_violations} violations."
        )
        return enforcement_results

    def create_file_creation_monitor(self):
        """ファイル作成監視システム"""

        class ConstraintFileHandler(FileSystemEventHandler):
            def __init__(self, constraint_engine):
                self.engine = constraint_engine

            def on_created(self, event):
                if event.is_directory:
                    return

                file_path = event.src_path

                # 禁止パターンチェック
                for pattern in self.engine.forbidden_patterns:
                    if Path(file_path).match(pattern.replace("*", "")):
                        logging.warning(f"FORBIDDEN FILE CREATED: {file_path}")
                        # 即座に隔離
                        self.engine.quarantine_violation(file_path)
                        break

            def on_moved(self, event):
                if event.is_directory:
                    return

                # 移動先もチェック
                self.on_created(
                    type(
                        "Event",
                        (),
                        {"src_path": event.dest_path, "is_directory": False},
                    )()
                )

        return ConstraintFileHandler(self)

    def start_monitoring(self):
        """リアルタイム監視開始"""
        if self.is_monitoring:
            logging.warning("Monitoring is already active.")
            return

        logging.info("Starting real-time constraint monitoring...")

        self.observer = Observer()
        event_handler = self.create_file_creation_monitor()

        # プロジェクト全体を監視
        self.observer.schedule(event_handler, str(self.project_root), recursive=True)
        self.observer.start()
        self.is_monitoring = True

        logging.info("Real-time monitoring started successfully.")

    def stop_monitoring(self):
        """監視停止"""
        if self.observer and self.is_monitoring:
            self.observer.stop()
            self.observer.join()
            self.is_monitoring = False
            logging.info("Real-time monitoring stopped.")

    def generate_constraint_report(self) -> Dict:
        """制約状況レポート生成"""
        violations = self.scan_violations()

        report = {
            "timestamp": datetime.now().isoformat(),
            "constraints_status": (
                "ENFORCED"
                if sum(len(v) for v in violations.values()) == 0
                else "VIOLATIONS_DETECTED"
            ),
            "violations_summary": {
                "personality_learning_files": len(
                    violations["personality_learning_files"]
                ),
                "redirect_files": len(violations["redirect_files"]),
                "duplicate_dbs": len(violations["duplicate_dbs"]),
                "total_violations": sum(len(v) for v in violations.values()),
            },
            "system_health": {
                "unified_db_exists": self.unified_db.exists(),
                "unified_db_size": (
                    self.unified_db.stat().st_size if self.unified_db.exists() else 0
                ),
                "monitoring_active": self.is_monitoring,
            },
            "recommended_actions": [],
        }

        # 推奨アクション生成
        if report["violations_summary"]["total_violations"] > 0:
            report["recommended_actions"].append(
                "Run enforce_constraints() to resolve violations"
            )

        if not report["system_health"]["unified_db_exists"]:
            report["recommended_actions"].append("Recreate unified database")

        if not report["system_health"]["monitoring_active"]:
            report["recommended_actions"].append("Start real-time monitoring")

        return report

    def validate_measurement_consistency(self) -> Dict:
        """測定値一貫性検証"""
        if not self.unified_db.exists():
            return {"status": "ERROR", "message": "Unified database not found"}

        try:
            conn = sqlite3.connect(self.unified_db)
            cursor = conn.cursor()

            # 異なる精度測定値の検出
            cursor.execute(
                """
                SELECT DISTINCT overall_accuracy, COUNT(*) as count 
                FROM unified_learning_accuracy 
                GROUP BY overall_accuracy 
                ORDER BY overall_accuracy DESC
            """
            )
            accuracy_values = cursor.fetchall()

            # 最新測定値取得
            cursor.execute(
                """
                SELECT overall_accuracy, measurement_date 
                FROM unified_learning_accuracy 
                ORDER BY measurement_date DESC LIMIT 1
            """
            )
            latest = cursor.fetchone()

            conn.close()

            return {
                "status": "OK",
                "accuracy_values": accuracy_values,
                "latest_accuracy": latest[0] if latest else None,
                "latest_date": latest[1] if latest else None,
                "consistency_check": "PASS" if len(accuracy_values) <= 2 else "WARNING",
            }

        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def execute_full_cleanup(self) -> Dict:
        """完全クリーンアップ実行"""
        logging.info("Starting MIRRALISM full cleanup...")

        # 1. 制約システム初期化
        self.initialize_constraints_system()

        # 2. 制約強制実行
        enforcement_results = self.enforce_constraints()

        # 3. 監視開始
        self.start_monitoring()

        # 4. 測定値一貫性検証
        consistency_check = self.validate_measurement_consistency()

        # 5. 最終レポート生成
        final_report = self.generate_constraint_report()

        cleanup_summary = {
            "cleanup_completed": datetime.now().isoformat(),
            "enforcement_results": enforcement_results,
            "consistency_check": consistency_check,
            "final_status": final_report,
            "next_phase_ready": final_report["constraints_status"] == "ENFORCED",
        }

        # レポート保存
        report_path = self.project_root / ".mirralism/cleanup_report.json"
        with open(report_path, "w") as f:
            json.dump(cleanup_summary, f, indent=2)

        logging.info(f"Full cleanup completed. Report saved: {report_path}")
        return cleanup_summary


if __name__ == "__main__":
    engine = MirralismConstraintEngine()
    results = engine.execute_full_cleanup()

    print("\n" + "=" * 80)
    print("MIRRALISM制約強制エンジン実行完了")
    print("=" * 80)
    print(f"違反ファイル検出: {results['enforcement_results']['total_violations_found']}個")
    print(f"違反ファイル解決: {results['enforcement_results']['total_violations_resolved']}個")
    print(
        f"personality_learning除去: {results['enforcement_results']['personality_learning_removed']}個"
    )
    print(f"REDIRECT除去: {results['enforcement_results']['redirect_removed']}個")
    print(f"重複DB除去: {results['enforcement_results']['duplicate_dbs_removed']}個")
    print(f"制約状況: {results['final_status']['constraints_status']}")
    print(f"次フェーズ準備: {'OK' if results['next_phase_ready'] else 'NG'}")
    print("=" * 80)
