"""
app.py
------
User Interface Module (CLI Dashboard)

Provides a simple, menu-driven command-line interface that ties together
the Data, Model, and Visualization modules into one workflow a user can
interact with, matching the "logical workflow" requirement.

Run with:  python -m src.app
"""

import sys
import pandas as pd

from src.config import FEATURE_COLUMNS
from src.data_manager import (
    load_or_generate_data,
    clean_data,
    save_to_database,
    load_from_database,
    log_prediction,
    get_prediction_history,
)
from src.model import PerformanceModel
from src.visualizer import generate_all_visuals
from src.logger import get_logger

logger = get_logger(__name__)

MENU = """
==========================================================
   STUDENT PERFORMANCE PREDICTOR - Main Menu
==========================================================
 1. Load & prepare dataset (generate + clean + store in DB)
 2. Train the ML model
 3. Generate visual reports (charts)
 4. Predict outcome for a new student
 5. View prediction history
 6. Exit
==========================================================
"""


def prompt_float(label: str, default: float) -> float:
    raw = input(f"  {label} [default={default}]: ").strip()
    try:
        return float(raw) if raw else default
    except ValueError:
        print("  Invalid number, using default.")
        return default


def run():
    model = None
    df = None

    while True:
        print(MENU)
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            raw_df = load_or_generate_data()
            df = clean_data(raw_df)
            save_to_database(df)
            print(f"\n[OK] Dataset ready: {len(df)} records loaded and stored in the database.")

        elif choice == "2":
            if df is None:
                df = load_from_database()
                if df.empty:
                    print("\n[!] Please load the dataset first (option 1).")
                    continue
            model = PerformanceModel()
            metrics = model.train(df)
            model.save()
            print(f"\n[OK] Model trained. Accuracy={metrics['accuracy']:.3f}  "
                  f"Precision={metrics['precision']:.3f}  Recall={metrics['recall']:.3f}  "
                  f"F1={metrics['f1_score']:.3f}")

        elif choice == "3":
            if df is None or model is None:
                print("\n[!] Please load data and train the model first (options 1 & 2).")
                continue
            metrics = model.train(df)  # re-derive metrics for chart generation
            paths = generate_all_visuals(df, metrics)
            print("\n[OK] Charts generated:")
            for p in paths:
                print("   -", p)

        elif choice == "4":
            if model is None or not model.is_trained:
                print("\n[!] Please train the model first (option 2).")
                continue
            print("\nEnter student details:")
            features = {}
            defaults = {
                "study_hours_per_week": 10,
                "attendance_percent": 75,
                "previous_grade": 60,
                "assignments_completed_percent": 70,
                "sleep_hours": 7,
                "extracurricular_hours": 3,
                "parental_support_score": 3,
            }
            for col in FEATURE_COLUMNS:
                features[col] = prompt_float(col.replace("_", " ").title(), defaults[col])

            student_id = input("  Student ID (for record keeping) [S_NEW]: ").strip() or "S_NEW"
            result, confidence = model.predict_single(features)
            log_prediction(student_id, result, confidence)

            print(f"\n[PREDICTION] Student {student_id} -> {result}  "
                  f"(confidence: {confidence * 100:.1f}%)")

        elif choice == "5":
            history = get_prediction_history()
            if history.empty:
                print("\n[!] No predictions recorded yet.")
            else:
                print("\nPrediction History:")
                print(history.to_string(index=False))

        elif choice == "6":
            print("\nExiting. Goodbye!")
            sys.exit(0)

        else:
            print("\n[!] Invalid choice, please select 1-6.")


if __name__ == "__main__":
    run()
