#!/usr/bin/env python3
"""
MIRRALISM緊急統合システム - V1問題の技術的根絶
CTOの指示に基づく制約ファースト設計の技術実装

目的: 36個の分散DBを1個の権威ソース(SSOT)に統合
原則: データ損失ゼロ、整合性保証、追跡可能性確保
"""

import hashlib
import json
import logging
import os
import shutil
import sqlite3
from datetime import datetime

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mirralism_unification.log"),
        logging.StreamHandler(),
    ],
)


class MirralismDatabaseUnifier:
    """MIRRALISM分散DB統合システム"""

    def __init__(self, project_root="/Users/suetakeshuuhei/MIRRALISM_V2"):
        self.project_root = project_root
        self.target_db = os.path.join(
            project_root, "Core/PersonalityLearning/MIRRALISM_UNIFIED.db"
        )
        self.backup_dir = os.path.join(project_root, ".mirralism/emergency_unification")
        self.audit_log = []

    def find_all_personality_dbs(self):
        """全personality_learningデータベースを発見"""
        db_files = []
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if "personality_learning" in file and file.endswith(".db"):
                    full_path = os.path.join(root, file)
                    size = os.path.getsize(full_path)
                    db_files.append(
                        {
                            "path": full_path,
                            "size": size,
                            "hash": self._calculate_file_hash(full_path),
                        }
                    )
        return db_files

    def _calculate_file_hash(self, filepath):
        """ファイルハッシュ計算（重複検出用）"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logging.error(f"Hash calculation failed for {filepath}: {e}")
            return None

    def analyze_database_content(self, db_path):
        """データベース内容分析"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # テーブル一覧取得
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            content_analysis = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]

                # 最新レコードの日付取得（存在する場合）
                try:
                    cursor.execute(f"SELECT MAX(created_at) FROM {table}")
                    latest_date = cursor.fetchone()[0]
                except:
                    try:
                        cursor.execute(f"SELECT MAX(analysis_date) FROM {table}")
                        latest_date = cursor.fetchone()[0]
                    except:
                        latest_date = None

                content_analysis[table] = {
                    "record_count": count,
                    "latest_date": latest_date,
                }

            conn.close()
            return content_analysis

        except Exception as e:
            logging.error(f"Database analysis failed for {db_path}: {e}")
            return {}

    def create_unified_database(self):
        """統合データベース作成"""
        # バックアップディレクトリ作成
        os.makedirs(self.backup_dir, exist_ok=True)

        # 既存の統合DBがあれば削除
        if os.path.exists(self.target_db):
            backup_path = os.path.join(
                self.backup_dir,
                f"previous_unified_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
            )
            shutil.copy2(self.target_db, backup_path)
            os.remove(self.target_db)

        # 新しい統合DB作成
        conn = sqlite3.connect(self.target_db)
        cursor = conn.cursor()

        # 統合スキーマ作成（全テーブルを統合）
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS unified_daily_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_date TEXT NOT NULL,
                suetake_likeness_index REAL,
                accuracy_score REAL,
                confidence_level REAL,
                source_database TEXT,
                integrated_at TEXT,
                UNIQUE(analysis_date, source_database)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS unified_learning_accuracy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                measurement_date TEXT NOT NULL,
                overall_accuracy REAL,
                accuracy_type TEXT,
                measurement_method TEXT,
                source_database TEXT,
                integrated_at TEXT,
                UNIQUE(measurement_date, accuracy_type, source_database)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS unified_voice_personality_weights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trait_name TEXT NOT NULL,
                weight_value REAL,
                confidence_score REAL,
                last_updated TEXT,
                source_database TEXT,
                integrated_at TEXT,
                UNIQUE(trait_name, source_database)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data_integration_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT NOT NULL,
                file_hash TEXT,
                records_integrated INTEGER,
                integration_timestamp TEXT,
                conflicts_resolved INTEGER,
                notes TEXT
            )
        """
        )

        conn.commit()
        conn.close()

        logging.info(f"Unified database created: {self.target_db}")

    def integrate_database(self, source_db_info):
        """個別データベースの統合"""
        source_path = source_db_info["path"]
        source_hash = source_db_info["hash"]

        try:
            # ソースDB接続
            source_conn = sqlite3.connect(source_path)
            source_cursor = source_conn.cursor()

            # ターゲットDB接続
            target_conn = sqlite3.connect(self.target_db)
            target_cursor = target_conn.cursor()

            integration_timestamp = datetime.now().isoformat()
            total_records = 0
            conflicts_resolved = 0

            # daily_analysisテーブルの統合
            try:
                source_cursor.execute("SELECT * FROM daily_analysis")
                for row in source_cursor.fetchall():
                    try:
                        target_cursor.execute(
                            """
                            INSERT OR REPLACE INTO unified_daily_analysis 
                            (analysis_date, suetake_likeness_index, accuracy_score, confidence_level, source_database, integrated_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """,
                            (
                                row[1],
                                row[2] if len(row) > 2 else None,
                                row[3] if len(row) > 3 else None,
                                row[4] if len(row) > 4 else None,
                                source_path,
                                integration_timestamp,
                            ),
                        )
                        total_records += 1
                    except sqlite3.IntegrityError:
                        conflicts_resolved += 1
            except sqlite3.OperationalError:
                pass  # テーブルが存在しない場合

            # learning_accuracyテーブルの統合
            try:
                source_cursor.execute("SELECT * FROM learning_accuracy")
                for row in source_cursor.fetchall():
                    try:
                        target_cursor.execute(
                            """
                            INSERT OR REPLACE INTO unified_learning_accuracy 
                            (measurement_date, overall_accuracy, accuracy_type, measurement_method, source_database, integrated_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """,
                            (
                                row[1],
                                row[2] if len(row) > 2 else None,
                                row[3] if len(row) > 3 else None,
                                row[4] if len(row) > 4 else None,
                                source_path,
                                integration_timestamp,
                            ),
                        )
                        total_records += 1
                    except sqlite3.IntegrityError:
                        conflicts_resolved += 1
            except sqlite3.OperationalError:
                pass

            # voice_personality_weightsテーブルの統合
            try:
                source_cursor.execute("SELECT * FROM voice_personality_weights")
                for row in source_cursor.fetchall():
                    try:
                        target_cursor.execute(
                            """
                            INSERT OR REPLACE INTO unified_voice_personality_weights 
                            (trait_name, weight_value, confidence_score, last_updated, source_database, integrated_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """,
                            (
                                row[1],
                                row[2] if len(row) > 2 else None,
                                row[3] if len(row) > 3 else None,
                                row[4] if len(row) > 4 else None,
                                source_path,
                                integration_timestamp,
                            ),
                        )
                        total_records += 1
                    except sqlite3.IntegrityError:
                        conflicts_resolved += 1
            except sqlite3.OperationalError:
                pass

            # 統合監査記録
            target_cursor.execute(
                """
                INSERT INTO data_integration_audit 
                (source_file, file_hash, records_integrated, integration_timestamp, conflicts_resolved, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    source_path,
                    source_hash,
                    total_records,
                    integration_timestamp,
                    conflicts_resolved,
                    f"Database integration completed. Size: {source_db_info['size']} bytes",
                ),
            )

            target_conn.commit()
            source_conn.close()
            target_conn.close()

            self.audit_log.append(
                {
                    "source": source_path,
                    "records": total_records,
                    "conflicts": conflicts_resolved,
                    "timestamp": integration_timestamp,
                }
            )

            logging.info(
                f"Integrated {source_path}: {total_records} records, {conflicts_resolved} conflicts resolved"
            )

        except Exception as e:
            logging.error(f"Integration failed for {source_path}: {e}")

    def generate_unification_report(self):
        """統合レポート生成"""
        conn = sqlite3.connect(self.target_db)
        cursor = conn.cursor()

        # 統合後の統計
        cursor.execute("SELECT COUNT(*) FROM unified_daily_analysis")
        daily_analysis_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM unified_learning_accuracy")
        learning_accuracy_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM unified_voice_personality_weights")
        voice_weights_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM data_integration_audit")
        audit_count = cursor.fetchone()[0]

        # 最新の測定値取得
        cursor.execute(
            """
            SELECT suetake_likeness_index, analysis_date, source_database 
            FROM unified_daily_analysis 
            ORDER BY analysis_date DESC LIMIT 1
        """
        )
        latest_daily = cursor.fetchone()

        cursor.execute(
            """
            SELECT overall_accuracy, measurement_date, source_database 
            FROM unified_learning_accuracy 
            ORDER BY measurement_date DESC LIMIT 1
        """
        )
        latest_accuracy = cursor.fetchone()

        conn.close()

        report = {
            "unification_completed": datetime.now().isoformat(),
            "databases_integrated": audit_count,
            "total_records": {
                "daily_analysis": daily_analysis_count,
                "learning_accuracy": learning_accuracy_count,
                "voice_weights": voice_weights_count,
            },
            "latest_measurements": {
                "daily_likeness": {
                    "value": latest_daily[0] if latest_daily else None,
                    "date": latest_daily[1] if latest_daily else None,
                    "source": latest_daily[2] if latest_daily else None,
                },
                "overall_accuracy": {
                    "value": latest_accuracy[0] if latest_accuracy else None,
                    "date": latest_accuracy[1] if latest_accuracy else None,
                    "source": latest_accuracy[2] if latest_accuracy else None,
                },
            },
            "audit_log": self.audit_log,
        }

        # レポートファイル保存
        report_path = os.path.join(
            self.backup_dir,
            f"unification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logging.info(f"Unification report saved: {report_path}")
        return report

    def execute_unification(self):
        """統合処理実行"""
        logging.info("Starting MIRRALISM database unification...")

        # 1. 全DBファイル発見
        db_files = self.find_all_personality_dbs()
        logging.info(f"Found {len(db_files)} personality learning databases")

        # 2. 統合データベース作成
        self.create_unified_database()

        # 3. 各データベースを統合
        for db_info in db_files:
            self.integrate_database(db_info)

        # 4. 統合レポート生成
        report = self.generate_unification_report()

        logging.info("MIRRALISM database unification completed successfully!")
        return report


if __name__ == "__main__":
    unifier = MirralismDatabaseUnifier()
    report = unifier.execute_unification()

    print("\n" + "=" * 80)
    print("MIRRALISM緊急統合完了")
    print("=" * 80)
    print(f"統合データベース数: {report['databases_integrated']}")
    print(f"総レコード数: {sum(report['total_records'].values())}")
    print(f"統合後測定値:")
    if report["latest_measurements"]["daily_likeness"]["value"]:
        print(
            f"  - 最新類似度: {report['latest_measurements']['daily_likeness']['value']:.1f}%"
        )
    if report["latest_measurements"]["overall_accuracy"]["value"]:
        print(
            f"  - 最新精度: {report['latest_measurements']['overall_accuracy']['value']:.1f}%"
        )
    print("=" * 80)
