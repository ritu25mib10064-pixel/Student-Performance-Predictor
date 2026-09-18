"""
main.py
-------
Entry point that runs the full pipeline end-to-end, non-interactively:
  1. Load/generate + clean data
  2. Store in SQLite
  3. Train the model
  4. Generate evaluation charts
  5. Run one sample prediction

Use this for a quick, automated demo. For the interactive menu-driven
experience, run `python -m src.app` instead.
"""

from src.data_manager import (
    load_or_generate_data,
    clean_data,
    save_to_database,
    log_prediction,
)
from src.model import PerformanceModel
from src.visualizer import generate_all_visuals
from src.logger import get_logger

logger = get_logger("main")


def main():
    logger.info("=== Student Performance Predictor: pipeline start ===")

    # 1 & 2: Data preparation + storage
    raw_df = load_or_generate_data()
    df = clean_data(raw_df)
    save_to_database(df)
    logger.info("Step 1/4 complete: dataset ready (%d records)", len(df))

    # 3: Train model
    model = PerformanceModel()
    metrics = model.train(df)
    model.save()
    logger.info("Step 2/4 complete: model trained (accuracy=%.3f)", metrics["accuracy"])

    # 4: Visualizations
    chart_paths = generate_all_visuals(df, metrics)
    logger.info("Step 3/4 complete: %d charts generated", len(chart_paths))

    # 5: Sample prediction
    sample_student = {
        "study_hours_per_week": 6,
        "attendance_percent": 60,
        "previous_grade": 50,
        "assignments_completed_percent": 55,
        "sleep_hours": 5.5,
        "extracurricular_hours": 2,
        "parental_support_score": 2,
    }
    result, confidence = model.predict_single(sample_student)
    log_prediction("S_DEMO", result, confidence)
    logger.info("Step 4/4 complete: sample prediction -> %s (confidence=%.2f)", result, confidence)

    print("\n================ PIPELINE SUMMARY ================")
    print(f"Records processed      : {len(df)}")
    print(f"Model test accuracy    : {metrics['accuracy']:.3f}")
    print(f"Model precision        : {metrics['precision']:.3f}")
    print(f"Model recall           : {metrics['recall']:.3f}")
    print(f"Model F1-score         : {metrics['f1_score']:.3f}")
    print(f"Charts saved to        : outputs/")
    print(f"Sample prediction      : {result} (confidence {confidence*100:.1f}%)")
    print("====================================================")


if __name__ == "__main__":
    main()
