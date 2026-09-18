"""
data_manager.py
----------------
Module 1: Data Input & Processing

Responsibilities:
  1. Generate/load the student dataset.
  2. Clean and validate it (handle missing values, invalid ranges).
  3. Persist the clean data into a SQLite database (acts as the project's
     storage layer, referenced by the ER diagram / schema design).

Note on the dataset:
  A synthetic-but-realistic dataset is generated here, modeled on the
  feature distributions commonly seen in publicly available student
  performance datasets (e.g., the UCI "Student Performance" dataset:
  study time, attendance, past grades, etc.). Generating it locally keeps
  the project fully reproducible and avoids any licensing/download
  dependency. To use a real dataset instead, simply replace
  `load_or_generate_data()` with a `pd.read_csv(<your_file>)` call while
  keeping the same column names defined in config.FEATURE_COLUMNS.
"""

import sqlite3
import numpy as np
import pandas as pd

from src.config import (
    RAW_DATA_PATH,
    CLEAN_DATA_PATH,
    DB_PATH,
    NUM_STUDENTS,
    RANDOM_SEED,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)
from src.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# 1. Data generation / loading
# ---------------------------------------------------------------------------
def load_or_generate_data() -> pd.DataFrame:
    """Load the raw dataset from disk if present, otherwise generate one."""
    import os

    if os.path.exists(RAW_DATA_PATH):
        logger.info("Loading existing raw dataset from %s", RAW_DATA_PATH)
        return pd.read_csv(RAW_DATA_PATH)

    logger.info("No raw dataset found. Generating a synthetic dataset (n=%d)", NUM_STUDENTS)
    df = _generate_synthetic_dataset(NUM_STUDENTS)
    df.to_csv(RAW_DATA_PATH, index=False)
    logger.info("Synthetic dataset saved to %s", RAW_DATA_PATH)
    return df


def _generate_synthetic_dataset(n: int) -> pd.DataFrame:
    """Create a realistic synthetic dataset of student features + outcome."""
    rng = np.random.default_rng(RANDOM_SEED)

    study_hours = np.clip(rng.normal(12, 5, n), 0, 40)
    attendance = np.clip(rng.normal(78, 15, n), 30, 100)
    previous_grade = np.clip(rng.normal(65, 15, n), 0, 100)
    assignments = np.clip(rng.normal(75, 18, n), 0, 100)
    sleep_hours = np.clip(rng.normal(6.5, 1.3, n), 3, 10)
    extracurricular = np.clip(rng.normal(4, 3, n), 0, 20)
    parental_support = rng.integers(1, 6, n)  # ordinal score 1-5

    # A weighted "true" score drives the label, with noise added so the
    # classification problem is realistic (not perfectly separable).
    weighted_score = (
        0.25 * study_hours
        + 0.30 * (attendance / 100 * 40)
        + 0.25 * (previous_grade / 100 * 40)
        + 0.10 * (assignments / 100 * 40)
        + 0.05 * (parental_support / 5 * 40)
        - 0.05 * np.abs(sleep_hours - 8) * 5
    )
    noise = rng.normal(0, 4, n)
    final_score = weighted_score + noise

    threshold = np.percentile(final_score, 35)  # ~35% fail rate baseline
    final_result = np.where(final_score >= threshold, "Pass", "Fail")

    df = pd.DataFrame(
        {
            "student_id": [f"S{1000 + i}" for i in range(n)],
            "study_hours_per_week": study_hours.round(1),
            "attendance_percent": attendance.round(1),
            "previous_grade": previous_grade.round(1),
            "assignments_completed_percent": assignments.round(1),
            "sleep_hours": sleep_hours.round(1),
            "extracurricular_hours": extracurricular.round(1),
            "parental_support_score": parental_support,
            TARGET_COLUMN: final_result,
        }
    )

    # Intentionally introduce a small amount of missing data to make the
    # cleaning step meaningful and demonstrate validation/error handling.
    missing_idx = rng.choice(df.index, size=int(0.03 * n), replace=False)
    df.loc[missing_idx, "sleep_hours"] = np.nan

    return df


# ---------------------------------------------------------------------------
# 2. Cleaning & validation
# ---------------------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate ranges, handle missing values, and drop duplicates."""
    logger.info("Cleaning dataset: %d rows before cleaning", len(df))
    df = df.drop_duplicates(subset="student_id").copy()

    # Fill missing numeric values with the column median (robust to outliers)
    for col in FEATURE_COLUMNS:
        if df[col].isna().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            logger.info("Filled %d missing values in '%s' with median=%.2f",
                        df[col].isna().sum(), col, median_val)

    # Range validation - clip any impossible values instead of crashing
    df["attendance_percent"] = df["attendance_percent"].clip(0, 100)
    df["previous_grade"] = df["previous_grade"].clip(0, 100)
    df["assignments_completed_percent"] = df["assignments_completed_percent"].clip(0, 100)
    df["study_hours_per_week"] = df["study_hours_per_week"].clip(0, 80)
    df["sleep_hours"] = df["sleep_hours"].clip(0, 14)

    df = df.dropna(subset=[TARGET_COLUMN])

    logger.info("Cleaning complete: %d rows after cleaning", len(df))
    df.to_csv(CLEAN_DATA_PATH, index=False)
    return df


# ---------------------------------------------------------------------------
# 3. Storage layer (SQLite)
# ---------------------------------------------------------------------------
def save_to_database(df: pd.DataFrame, db_path: str = DB_PATH) -> None:
    """Persist the cleaned dataset into a SQLite database."""
    logger.info("Writing %d records to database at %s", len(df), db_path)
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql("students", conn, if_exists="replace", index=False)

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                predicted_result TEXT,
                confidence REAL,
                predicted_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
    logger.info("Database write complete.")


def load_from_database(db_path: str = DB_PATH) -> pd.DataFrame:
    """Read the students table back from SQLite."""
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM students", conn)
    finally:
        conn.close()
    return df


def log_prediction(student_id: str, predicted_result: str, confidence: float,
                    db_path: str = DB_PATH) -> None:
    """Insert a single prediction record into the predictions table (CRUD - Create)."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO predictions (student_id, predicted_result, confidence) VALUES (?, ?, ?)",
            (student_id, predicted_result, confidence),
        )
        conn.commit()
    finally:
        conn.close()


def get_prediction_history(db_path: str = DB_PATH) -> pd.DataFrame:
    """Read all past predictions (CRUD - Read)."""
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM predictions ORDER BY predicted_at DESC", conn)
    finally:
        conn.close()
    return df


if __name__ == "__main__":
    raw_df = load_or_generate_data()
    clean_df = clean_data(raw_df)
    save_to_database(clean_df)
    print(clean_df.head())
    print(f"\nTotal records processed: {len(clean_df)}")
