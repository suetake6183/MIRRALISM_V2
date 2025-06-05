"""
MIRRALISM PersonalityLearning統合データベース管理
=====================================================

V2データベーススキーマ：
- 既存テーブル統合 (value_patterns, expression_styles, emotion_reactions, daily_analysis, learning_accuracy)
- TaskMaster統合 (task_learning_correlation)
- SuperWhisper統合 (voice_data_metadata)
- 学習進捗管理 (learning_progress)
- キーワード学習 (keyword_learning)
- 分析履歴 (analysis_history)

進化目標: 53% → 95% 精度向上
"""

import json
import logging
import sqlite3
import threading
from contextlib import contextmanager
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

# ログ設定
logger = logging.getLogger(__name__)


class PersonalityLearningDatabase:
    """MIRRALISM PersonalityLearning統合データベース管理クラス"""

    def __init__(self, db_path: str = "personality_learning_v2.db"):
        """
        データベース初期化

        Args:
            db_path: データベースファイルパス
        """
        self.db_path = db_path
        self._local = threading.local()
        self.init_database()
        logger.info(f"PersonalityLearning Database initialized: {db_path}")

    @contextmanager
    def get_connection(self):
        """スレッドセーフなデータベース接続管理"""
        if not hasattr(self._local, "connection"):
            self._local.connection = sqlite3.connect(
                self.db_path, check_same_thread=False, timeout=30.0
            )
            self._local.connection.row_factory = sqlite3.Row
            self._local.connection.execute("PRAGMA foreign_keys = ON")
            self._local.connection.execute("PRAGMA journal_mode = WAL")

        try:
            yield self._local.connection
        except Exception as e:
            self._local.connection.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            self._local.connection.commit()

    def init_database(self):
        """データベーススキーマ初期化"""
        with self.get_connection() as conn:
            # 1. 価値観パターン (統合・改良版)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS value_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    subcategory TEXT,
                    importance_score INTEGER NOT NULL CHECK (importance_score >= 1 AND importance_score <= 10),
                    expression_pattern TEXT NOT NULL,
                    context_info TEXT,
                    frequency_daily INTEGER DEFAULT 0,
                    frequency_weekly INTEGER DEFAULT 0,
                    frequency_monthly INTEGER DEFAULT 0,
                    first_detected DATE NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    confidence_score REAL DEFAULT 0.5 CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
                    evolution_stage TEXT DEFAULT 'discovered' CHECK (evolution_stage IN ('discovered', 'learning', 'stable', 'evolving')),
                    source_type TEXT DEFAULT 'journal' CHECK (source_type IN ('journal', 'voice', 'task', 'interaction')),
                    learning_vector TEXT -- JSON: 53%→95%進化ベクター
                );
            """
            )

            # 2. 表現スタイル (統合・改良版)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expression_styles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    formality_level TEXT NOT NULL CHECK (formality_level IN ('formal', 'semi_formal', 'casual')),
                    technical_level TEXT NOT NULL CHECK (technical_level IN ('high', 'medium', 'low')),
                    emotional_level TEXT NOT NULL CHECK (emotional_level IN ('high', 'medium', 'low')),
                    reader_consideration TEXT NOT NULL CHECK (reader_consideration IN ('high', 'medium', 'low')),
                    pattern_example TEXT NOT NULL,
                    usage_context TEXT,
                    frequency_count INTEGER DEFAULT 1,
                    effectiveness_score REAL DEFAULT 0.5 CHECK (effectiveness_score >= 0.0 AND effectiveness_score <= 1.0),
                    accuracy_contribution REAL DEFAULT 0.0 CHECK (accuracy_contribution >= 0.0 AND accuracy_contribution <= 1.0),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # 3. 感情反応 (統合・改良版)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS emotion_reactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reaction_type TEXT NOT NULL CHECK (reaction_type IN ('positive', 'negative', 'neutral', 'mixed')),
                    trigger_category TEXT NOT NULL,
                    emotion_intensity INTEGER NOT NULL CHECK (emotion_intensity >= 1 AND emotion_intensity <= 10),
                    duration_type TEXT NOT NULL CHECK (duration_type IN ('instant', 'short', 'medium', 'long')),
                    impact_scope TEXT NOT NULL CHECK (impact_scope IN ('personal', 'interpersonal', 'professional', 'global')),
                    expression_text TEXT NOT NULL,
                    context_description TEXT,
                    journal_date DATE NOT NULL,
                    analysis_confidence REAL DEFAULT 0.5 CHECK (analysis_confidence >= 0.0 AND analysis_confidence <= 1.0),
                    voice_data_id INTEGER,
                    task_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (voice_data_id) REFERENCES voice_data_metadata(id),
                    FOREIGN KEY (task_id) REFERENCES task_learning_correlation(task_id)
                );
            """
            )

            # 4. 日次分析 (統合・改良版)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_date DATE UNIQUE NOT NULL,
                    total_personality_elements INTEGER NOT NULL DEFAULT 0,
                    new_patterns_discovered INTEGER NOT NULL DEFAULT 0,
                    existing_patterns_reinforced INTEGER NOT NULL DEFAULT 0,
                    suetake_likeness_index REAL NOT NULL DEFAULT 0.0 CHECK (suetake_likeness_index >= 0.0 AND suetake_likeness_index <= 100.0),
                    dominant_emotion TEXT,
                    key_insights TEXT,
                    analysis_summary TEXT,
                    processing_time_seconds REAL NOT NULL DEFAULT 0.0,
                    accuracy_improvement REAL DEFAULT 0.0,
                    task_completion_correlation REAL DEFAULT 0.0,
                    voice_interaction_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # 5. 学習精度管理 (統合・改良版)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS learning_accuracy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    measurement_date DATE NOT NULL,
                    emotion_analysis_accuracy REAL CHECK (emotion_analysis_accuracy >= 0.0 AND emotion_analysis_accuracy <= 1.0),
                    expression_prediction_accuracy REAL CHECK (expression_prediction_accuracy >= 0.0 AND expression_prediction_accuracy <= 1.0),
                    value_judgment_accuracy REAL CHECK (value_judgment_accuracy >= 0.0 AND value_judgment_accuracy <= 1.0),
                    overall_accuracy REAL CHECK (overall_accuracy >= 0.0 AND overall_accuracy <= 1.0),
                    total_patterns_learned INTEGER DEFAULT 0,
                    improvement_suggestions TEXT,
                    accuracy_delta REAL DEFAULT 0.0,
                    confidence_level REAL DEFAULT 0.5 CHECK (confidence_level >= 0.0 AND confidence_level <= 1.0),
                    methodology TEXT DEFAULT 'v2_mirralism',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # 6. 学習進捗追跡 (NEW)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS learning_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    progress_date DATE NOT NULL,
                    learning_phase TEXT NOT NULL CHECK (learning_phase IN ('initial', 'training', 'validation', 'production')),
                    accuracy_target REAL NOT NULL CHECK (accuracy_target >= 0.0 AND accuracy_target <= 1.0),
                    accuracy_current REAL NOT NULL CHECK (accuracy_current >= 0.0 AND accuracy_current <= 1.0),
                    progress_percentage REAL NOT NULL CHECK (progress_percentage >= 0.0 AND progress_percentage <= 100.0),
                    milestone_achieved BOOLEAN DEFAULT FALSE,
                    validation_method TEXT,
                    training_data_count INTEGER DEFAULT 0,
                    feedback_incorporated INTEGER DEFAULT 0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # 7. キーワード学習 (NEW)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS keyword_learning (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL UNIQUE,
                    category TEXT NOT NULL,
                    weight_initial REAL DEFAULT 1.0 CHECK (weight_initial >= 0.0),
                    weight_current REAL DEFAULT 1.0 CHECK (weight_current >= 0.0),
                    weight_evolution REAL DEFAULT 0.0,
                    frequency_total INTEGER DEFAULT 1,
                    frequency_recent INTEGER DEFAULT 1,
                    context_patterns TEXT, -- JSON: 出現コンテキスト
                    sentiment_association REAL DEFAULT 0.0 CHECK (sentiment_association >= -1.0 AND sentiment_association <= 1.0),
                    accuracy_contribution REAL DEFAULT 0.0 CHECK (accuracy_contribution >= 0.0 AND accuracy_contribution <= 1.0),
                    learning_confidence REAL DEFAULT 0.5 CHECK (learning_confidence >= 0.0 AND learning_confidence <= 1.0),
                    first_learned DATE NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # 8. 分析履歴 (NEW)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_id TEXT NOT NULL,
                    analysis_type TEXT NOT NULL CHECK (analysis_type IN ('journal', 'voice', 'task', 'periodic')),
                    input_text TEXT NOT NULL,
                    analysis_result TEXT, -- JSON: 分析結果
                    confidence_score REAL DEFAULT 0.5 CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
                    processing_time_ms INTEGER DEFAULT 0,
                    accuracy_estimated REAL DEFAULT 0.0 CHECK (accuracy_estimated >= 0.0 AND accuracy_estimated <= 1.0),
                    feedback_received BOOLEAN DEFAULT FALSE,
                    feedback_accuracy REAL CHECK (feedback_accuracy >= 0.0 AND feedback_accuracy <= 1.0),
                    methodology TEXT DEFAULT 'v2_mirralism',
                    error_log TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # 9. TaskMaster統合相関 (NEW)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_learning_correlation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    task_title TEXT,
                    task_status TEXT,
                    completion_date DATE,
                    learning_impact_score REAL DEFAULT 0.0 CHECK (learning_impact_score >= 0.0 AND learning_impact_score <= 10.0),
                    personality_elements_discovered INTEGER DEFAULT 0,
                    accuracy_before REAL CHECK (accuracy_before >= 0.0 AND accuracy_before <= 1.0),
                    accuracy_after REAL CHECK (accuracy_after >= 0.0 AND accuracy_after <= 1.0),
                    knowledge_gain TEXT, -- JSON: 獲得知識
                    behavioral_changes TEXT, -- JSON: 行動変化
                    correlation_strength REAL DEFAULT 0.0 CHECK (correlation_strength >= 0.0 AND correlation_strength <= 1.0),
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # 10. SuperWhisper音声データメタデータ (NEW)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS voice_data_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    duration_seconds REAL NOT NULL,
                    transcription_text TEXT,
                    transcription_confidence REAL CHECK (transcription_confidence >= 0.0 AND transcription_confidence <= 1.0),
                    audio_quality_score REAL CHECK (audio_quality_score >= 0.0 AND audio_quality_score <= 10.0),
                    personality_analysis_done BOOLEAN DEFAULT FALSE,
                    personality_elements_count INTEGER DEFAULT 0,
                    sentiment_analysis TEXT, -- JSON: 感情分析結果
                    keywords_extracted TEXT, -- JSON: 抽出キーワード
                    learning_contribution REAL DEFAULT 0.0 CHECK (learning_contribution >= 0.0 AND learning_contribution <= 1.0),
                    recording_date DATE,
                    processed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # インデックス作成
            self._create_indexes(conn)

            logger.info("Database schema initialized successfully")

    def _create_indexes(self, conn):
        """パフォーマンス最適化インデックス作成"""
        indexes = [
            # 既存テーブル最適化
            "CREATE INDEX IF NOT EXISTS idx_value_patterns_category ON value_patterns(category)",
            "CREATE INDEX IF NOT EXISTS idx_value_patterns_importance ON value_patterns(importance_score DESC)",
            "CREATE INDEX IF NOT EXISTS idx_value_patterns_evolution ON value_patterns(evolution_stage)",
            "CREATE INDEX IF NOT EXISTS idx_expression_styles_formality ON expression_styles(formality_level)",
            "CREATE INDEX IF NOT EXISTS idx_emotion_reactions_date ON emotion_reactions(journal_date)",
            "CREATE INDEX IF NOT EXISTS idx_emotion_reactions_type ON emotion_reactions(reaction_type)",
            "CREATE INDEX IF NOT EXISTS idx_daily_analysis_date ON daily_analysis(analysis_date DESC)",
            "CREATE INDEX IF NOT EXISTS idx_daily_analysis_likeness ON daily_analysis(suetake_likeness_index DESC)",
            "CREATE INDEX IF NOT EXISTS idx_learning_accuracy_date ON learning_accuracy(measurement_date DESC)",
            # 新テーブル最適化
            "CREATE INDEX IF NOT EXISTS idx_learning_progress_date ON learning_progress(progress_date DESC)",
            "CREATE INDEX IF NOT EXISTS idx_learning_progress_phase ON learning_progress(learning_phase)",
            "CREATE INDEX IF NOT EXISTS idx_keyword_learning_keyword ON keyword_learning(keyword)",
            "CREATE INDEX IF NOT EXISTS idx_keyword_learning_weight ON keyword_learning(weight_current DESC)",
            "CREATE INDEX IF NOT EXISTS idx_analysis_history_type ON analysis_history(analysis_type)",
            "CREATE INDEX IF NOT EXISTS idx_analysis_history_date ON analysis_history(created_at DESC)",
            "CREATE INDEX IF NOT EXISTS idx_task_correlation_task_id ON task_learning_correlation(task_id)",
            "CREATE INDEX IF NOT EXISTS idx_voice_metadata_date ON voice_data_metadata(recording_date DESC)",
            "CREATE INDEX IF NOT EXISTS idx_voice_metadata_processed ON voice_data_metadata(personality_analysis_done)",
        ]

        for index_sql in indexes:
            conn.execute(index_sql)

    # ======================
    # 学習進捗管理メソッド
    # ======================

    def record_learning_progress(
        self,
        phase: str,
        target: float,
        current: float,
        method: str = None,
        notes: str = None,
    ) -> int:
        """学習進捗記録"""
        progress_percentage = (current / target * 100) if target > 0 else 0
        # データベース制約対応: 100%以内に制限
        progress_percentage = min(progress_percentage, 100.0)
        milestone = progress_percentage >= 90  # 90%以上でマイルストーン達成

        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO learning_progress
                (progress_date, learning_phase, accuracy_target, accuracy_current,
                 progress_percentage, milestone_achieved, validation_method, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    date.today(),
                    phase,
                    target,
                    current,
                    progress_percentage,
                    milestone,
                    method,
                    notes,
                ),
            )
            return cursor.lastrowid

    def get_learning_progress(self, days: int = 30) -> List[Dict]:
        """学習進捗取得"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM learning_progress
                WHERE progress_date >= date('now', '-{} days')
                ORDER BY progress_date DESC
            """.format(
                    days
                )
            )
            return [dict(row) for row in cursor.fetchall()]

    def record_accuracy_measurement(
        self,
        emotion: float,
        expression: float,
        value: float,
        overall: float,
        suggestions: str = None,
    ) -> int:
        """精度測定記録"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO learning_accuracy
                (measurement_date, emotion_analysis_accuracy, expression_prediction_accuracy,
                 value_judgment_accuracy, overall_accuracy, improvement_suggestions)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    date.today(),
                    emotion,
                    expression,
                    value,
                    overall,
                    suggestions,
                ),
            )
            return cursor.lastrowid

    # ======================
    # キーワード学習メソッド
    # ======================

    def learn_keyword(
        self,
        keyword: str,
        category: str,
        context: str = None,
        sentiment: float = 0.0,
    ) -> int:
        """キーワード学習・更新"""
        with self.get_connection() as conn:
            # 既存チェック
            existing = conn.execute(
                "SELECT id, frequency_total, weight_current FROM keyword_learning WHERE keyword = ?",
                (keyword,),
            ).fetchone()

            if existing:
                # 更新
                new_frequency = existing["frequency_total"] + 1
                weight_evolution = 0.1 * (new_frequency / 10)  # 頻度に応じた重み増加
                new_weight = min(existing["weight_current"] + weight_evolution, 10.0)

                conn.execute(
                    """
                    UPDATE keyword_learning SET
                    frequency_total = ?, weight_current = ?, weight_evolution = ?,
                    frequency_recent = frequency_recent + 1, last_updated = ?
                    WHERE id = ?
                """,
                    (
                        new_frequency,
                        new_weight,
                        weight_evolution,
                        datetime.now(),
                        existing["id"],
                    ),
                )
                return existing["id"]
            else:
                # 新規作成
                cursor = conn.execute(
                    """
                    INSERT INTO keyword_learning
                    (keyword, category, context_patterns, sentiment_association, first_learned)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        keyword,
                        category,
                        json.dumps([context]) if context else None,
                        sentiment,
                        date.today(),
                    ),
                )
                return cursor.lastrowid

    def get_keyword_weights(self, category: str = None) -> Dict[str, float]:
        """キーワード重みマップ取得"""
        where_clause = "WHERE category = ?" if category else ""
        params = (category,) if category else ()

        with self.get_connection() as conn:
            cursor = conn.execute(
                f"""
                SELECT keyword, weight_current FROM keyword_learning {where_clause}
                ORDER BY weight_current DESC
            """,
                params,
            )
            return {row["keyword"]: row["weight_current"] for row in cursor.fetchall()}

    # ======================
    # TaskMaster統合メソッド
    # ======================

    def correlate_task_learning(
        self,
        task_id: int,
        task_title: str,
        learning_impact: float,
        elements_discovered: int = 0,
        accuracy_before: float = None,
        accuracy_after: float = None,
    ) -> int:
        """タスク学習相関記録"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO task_learning_correlation
                (task_id, task_title, learning_impact_score, personality_elements_discovered,
                 accuracy_before, accuracy_after)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    task_id,
                    task_title,
                    learning_impact,
                    elements_discovered,
                    accuracy_before,
                    accuracy_after,
                ),
            )
            return cursor.lastrowid

    def update_task_completion(
        self, task_id: int, status: str, completion_date: date = None
    ):
        """タスク完了更新"""
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE task_learning_correlation SET
                task_status = ?, completion_date = ?, updated_at = ?
                WHERE task_id = ?
            """,
                (
                    status,
                    completion_date or date.today(),
                    datetime.now(),
                    task_id,
                ),
            )

    # ======================
    # SuperWhisper統合メソッド
    # ======================

    def register_voice_data(
        self,
        file_path: str,
        file_name: str,
        duration: float,
        transcription: str = None,
        confidence: float = None,
    ) -> int:
        """音声データ登録"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO voice_data_metadata
                (file_path, file_name, duration_seconds, transcription_text, transcription_confidence, recording_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    file_path,
                    file_name,
                    duration,
                    transcription,
                    confidence,
                    date.today(),
                ),
            )
            return cursor.lastrowid

    def update_voice_analysis(
        self,
        voice_id: int,
        personality_elements: int,
        sentiment: Dict,
        keywords: List[str],
        contribution: float,
    ):
        """音声分析結果更新"""
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE voice_data_metadata SET
                personality_analysis_done = TRUE, personality_elements_count = ?,
                sentiment_analysis = ?, keywords_extracted = ?, learning_contribution = ?,
                processed_at = ?
                WHERE id = ?
            """,
                (
                    personality_elements,
                    json.dumps(sentiment),
                    json.dumps(keywords),
                    contribution,
                    datetime.now(),
                    voice_id,
                ),
            )

    # ======================
    # 分析履歴メソッド
    # ======================

    def record_analysis(
        self,
        analysis_id: str,
        analysis_type: str,
        input_text: str,
        result: Dict,
        confidence: float,
        processing_time: int = 0,
    ) -> int:
        """分析履歴記録"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO analysis_history
                (analysis_id, analysis_type, input_text, analysis_result,
                 confidence_score, processing_time_ms)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    analysis_id,
                    analysis_type,
                    input_text,
                    json.dumps(result),
                    confidence,
                    processing_time,
                ),
            )
            return cursor.lastrowid

    def update_analysis_feedback(self, analysis_id: str, feedback_accuracy: float):
        """分析フィードバック更新"""
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE analysis_history SET
                feedback_received = TRUE, feedback_accuracy = ?
                WHERE analysis_id = ?
            """,
                (feedback_accuracy, analysis_id),
            )

    # ======================
    # 統計・レポートメソッド
    # ======================

    def get_accuracy_evolution(self, days: int = 90) -> List[Dict]:
        """精度進化履歴取得"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT measurement_date, overall_accuracy, accuracy_delta
                FROM learning_accuracy
                WHERE measurement_date >= date('now', '-{} days')
                ORDER BY measurement_date
            """.format(
                    days
                )
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_learning_stats(self) -> Dict:
        """学習統計サマリー"""
        with self.get_connection() as conn:
            # 最新精度
            latest_accuracy = conn.execute(
                """
                SELECT overall_accuracy FROM learning_accuracy
                ORDER BY measurement_date DESC LIMIT 1
            """
            ).fetchone()

            # 総学習データ数
            total_patterns = conn.execute(
                "SELECT COUNT(*) as count FROM value_patterns"
            ).fetchone()
            total_keywords = conn.execute(
                "SELECT COUNT(*) as count FROM keyword_learning"
            ).fetchone()
            total_analyses = conn.execute(
                "SELECT COUNT(*) as count FROM analysis_history"
            ).fetchone()

            # TaskMaster相関
            task_correlations = conn.execute(
                """
                SELECT AVG(learning_impact_score) as avg_impact FROM task_learning_correlation
            """
            ).fetchone()

            return {
                "current_accuracy": (
                    latest_accuracy["overall_accuracy"] if latest_accuracy else 0.0
                ),
                "total_patterns": total_patterns["count"],
                "total_keywords": total_keywords["count"],
                "total_analyses": total_analyses["count"],
                "avg_task_impact": (
                    task_correlations["avg_impact"] if task_correlations else 0.0
                ),
                "target_accuracy": 0.95,
                "progress_to_target": (
                    (latest_accuracy["overall_accuracy"] / 0.95 * 100)
                    if latest_accuracy
                    else 0.0
                ),
            }

    def close(self):
        """データベース接続クローズ"""
        if hasattr(self._local, "connection"):
            self._local.connection.close()
            del self._local.connection


# シングルトンインスタンス
db_instance = None


def get_database() -> PersonalityLearningDatabase:
    """データベースインスタンス取得"""
    global db_instance
    if db_instance is None:
        db_instance = PersonalityLearningDatabase()
    return db_instance


if __name__ == "__main__":
    # テスト実行
    db = get_database()
    stats = db.get_learning_stats()
    print(f"MIRRALISM PersonalityLearning Database Stats: {stats}")
