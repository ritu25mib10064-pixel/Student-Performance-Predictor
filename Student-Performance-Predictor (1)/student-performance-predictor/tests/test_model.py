"""
test_model.py
-------------
Basic unit/validation tests for the data pipeline and ML model.
Run with:  pytest tests/  (from the project root)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.data_manager import _generate_synthetic_dataset, clean_data
from src.model import PerformanceModel
from src.config import FEATURE_COLUMNS, TARGET_COLUMN


def test_dataset_generation_shape():
    df = _generate_synthetic_dataset(100)
    assert len(df) == 100
    for col in FEATURE_COLUMNS:
        assert col in df.columns
    assert TARGET_COLUMN in df.columns


def test_dataset_target_values():
    df = _generate_synthetic_dataset(200)
    assert set(df[TARGET_COLUMN].unique()) <= {"Pass", "Fail"}


def test_clean_data_removes_missing_values():
    df = _generate_synthetic_dataset(300)
    cleaned = clean_data(df)
    assert cleaned[FEATURE_COLUMNS].isna().sum().sum() == 0


def test_clean_data_respects_value_ranges():
    df = _generate_synthetic_dataset(300)
    cleaned = clean_data(df)
    assert cleaned["attendance_percent"].between(0, 100).all()
    assert cleaned["previous_grade"].between(0, 100).all()


def test_model_trains_and_returns_metrics():
    df = clean_data(_generate_synthetic_dataset(400))
    model = PerformanceModel()
    metrics = model.train(df)

    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["precision"] <= 1.0
    assert 0.0 <= metrics["recall"] <= 1.0
    assert model.is_trained is True


def test_model_single_prediction_format():
    df = clean_data(_generate_synthetic_dataset(400))
    model = PerformanceModel()
    model.train(df)

    sample = {col: df[col].mean() for col in FEATURE_COLUMNS}
    result, confidence = model.predict_single(sample)

    assert result in ("Pass", "Fail")
    assert 0.0 <= confidence <= 1.0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
