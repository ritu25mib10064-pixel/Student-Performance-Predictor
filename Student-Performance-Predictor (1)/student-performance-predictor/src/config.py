"""
config.py
----------
Central configuration for the Student Performance Predictor system.
Keeping all paths, constants, and tunable parameters in one place makes
the project easier to maintain and extend (Maintainability - NFR).
"""

import os

# ---------------------------------------------------------------------------
# Directory paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

RAW_DATA_PATH = os.path.join(DATA_DIR, "students_raw.csv")
CLEAN_DATA_PATH = os.path.join(DATA_DIR, "students_clean.csv")
DB_PATH = os.path.join(DATA_DIR, "students.db")

MODEL_PATH = os.path.join(MODELS_DIR, "performance_model.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")

LOG_PATH = os.path.join(OUTPUTS_DIR, "app.log")

# ---------------------------------------------------------------------------
# Dataset generation parameters
# ---------------------------------------------------------------------------
NUM_STUDENTS = 800
RANDOM_SEED = 42

FEATURE_COLUMNS = [
    "study_hours_per_week",
    "attendance_percent",
    "previous_grade",
    "assignments_completed_percent",
    "sleep_hours",
    "extracurricular_hours",
    "parental_support_score",
]

TARGET_COLUMN = "final_result"  # Pass / Fail (classification target)

# ---------------------------------------------------------------------------
# Model parameters
# ---------------------------------------------------------------------------
TEST_SIZE = 0.2
N_ESTIMATORS = 150
MAX_DEPTH = 8

# ---------------------------------------------------------------------------
# Ensure required directories exist at import time
# ---------------------------------------------------------------------------
for _dir in (DATA_DIR, MODELS_DIR, OUTPUTS_DIR):
    os.makedirs(_dir, exist_ok=True)
