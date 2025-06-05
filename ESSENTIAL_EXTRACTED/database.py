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
from typing import Dict, List

# ログ設定
logger = logging.getLogger(__name__)


class Database:
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
                    importance_score INTEGER NOT NULL CHECK (
                        importance_score >= 1 AND importance_score <= 10
                    ),
                    expression_pattern TEXT NOT NULL,
                    context_info TEXT,
                    frequency_daily INTEGER DEFAULT 0,
                    frequency_weekly INTEGER DEFAULT 0,
                    frequency_monthly INTEGER DEFAULT 0,
                    first_detected DATE NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    confidence_score REAL DEFAULT 0.5 CHECK (
                        confidence_score >= 0.0 AND confidence_score <= 1.0
                    ),
                    evolution_stage TEXT DEFAULT 'discovered' CHECK (
                        evolution_stage IN (
                            'discovered', 'learning', 'stable', 'evolving'
                        )
                    ),
                    source_type TEXT DEFAULT 'journal' CHECK (
                        source_type IN (
                            'journal', 'voice', 'task', 'interaction'
                        )
                    ),
                    learning_vector TEXT -- JSON: 53%→95%進化ベクター
                );
            """
            )

            # 2. 表現スタイル (統合・改良版)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expression_styles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    formality_level TEXT NOT NULL CHECK (
                        formality_level IN ('formal', 'semi_formal', 'casual')
                    ),
                    technical_level TEXT NOT NULL CHECK (
                        technical_level IN ('high', 'medium', 'low')
                    ),
                    emotional_level TEXT NOT NULL CHECK (
                        emotional_level IN ('high', 'medium', 'low')
                    ),
                    reader_consideration TEXT NOT NULL CHECK (
                        reader_consideration IN ('high', 'medium', 'low')
                    ),
                    pattern_example TEXT NOT NULL,
                    usage_context TEXT,
                    frequency_count INTEGER DEFAULT 1,
                    effectiveness_score REAL DEFAULT 0.5 CHECK (
                        effectiveness_score >= 0.0 AND effectiveness_score <= 1.0
                    ),
                    accuracy_contribution REAL DEFAULT 0.0 CHECK (
                        accuracy_contribution >= 0.0 AND 
                        accuracy_contribution <= 1.0
                    ),
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
                    reaction_type TEXT NOT NULL CHECK (
                        reaction_type IN ('positive', 'negative', 'neutral', 'mixed')
                    ),
                    trigger_category TEXT NOT NULL,
                    emotion_intensity INTEGER NOT NULL CHECK (
                        emotion_intensity >= 1 AND emotion_intensity <= 10
                    ),
                    duration_type TEXT NOT NULL CHECK (
                        duration_type IN ('instant', 'short', 'medium', 'long')
                    ),
                    impact_scope TEXT NOT NULL CHECK (
                        impact_scope IN (
                            'personal', 'interpersonal', 'professional', 'global'
                        )
                    ),
                    expression_text TEXT NOT NULL,
                    context_description TEXT,
                    journal_date DATE NOT NULL,
                    analysis_confidence REAL DEFAULT 0.5 CHECK (
                        analysis_confidence >= 0.0 AND analysis_confidence <= 1.0
                    ),
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
                    suetake_likeness_index REAL NOT NULL DEFAULT 0.0 CHECK (
                        suetake_likeness_index >= 0.0 AND 
                        suetake_likeness_index <= 100.0
                    ),
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
                    emotion_analysis_accuracy REAL CHECK (
                        emotion_analysis_accuracy >= 0.0 AND 
                        emotion_analysis_accuracy <= 1.0
                    ),
                    expression_prediction_accuracy REAL CHECK (
                        expression_prediction_accuracy >= 0.0 AND 
                        expression_prediction_accuracy <= 1.0
                    ),
                    value_judgment_accuracy REAL CHECK (
                        value_judgment_accuracy >= 0.0 AND 
                        value_judgment_accuracy <= 1.0
                    ),
                    overall_accuracy REAL CHECK (
                        overall_accuracy >= 0.0 AND overall_accuracy <= 1.0
                    ),
                    total_patterns_learned INTEGER DEFAULT 0,
                    improvement_suggestions TEXT,
                    accuracy_delta REAL DEFAULT 0.0,
                    confidence_level REAL DEFAULT 0.5 CHECK (
                        confidence_level >= 0.0 AND confidence_level <= 1.0
                    ),
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
                    learning_phase TEXT NOT NULL CHECK (
                        learning_phase IN (
                            'initial', 'training', 'validation', 'production'
                        )
                    ),
                    accuracy_target REAL NOT NULL CHECK (
                        accuracy_target >= 0.0 AND accuracy_target <= 1.0
                    ),
                    accuracy_current REAL NOT NULL CHECK (
                        accuracy_current >= 0.0 AND accuracy_current <= 1.0
                    ),
                    progress_percentage REAL NOT NULL CHECK (
                        progress_percentage >= 0.0 AND 
                        progress_percentage <= 100.0
                    ),
                    milestone_achieved BOOLEAN DEFAULT FALSE,
                    validation_method TEXT,
                    training_data_count INTEGER DEFAULT 0,
                    feedback_incorporated INTEGER DEFAULT 0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
