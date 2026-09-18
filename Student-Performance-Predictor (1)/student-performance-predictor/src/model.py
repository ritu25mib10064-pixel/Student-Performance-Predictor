"""
model.py
--------
Module 2: ML Model Training & Prediction

Responsibilities:
  1. Split data into train/test sets.
  2. Train a classification model (Random Forest) to predict Pass/Fail.
  3. Evaluate the model (accuracy, precision, recall, F1, confusion matrix).
  4. Persist the trained model + scaler for later use (predict.py / app.py).
  5. Provide a `predict_single()` helper for real-time, single-student
     predictions (used by the CLI/dashboard module).
"""

import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from src.config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    MODEL_PATH,
    SCALER_PATH,
    TEST_SIZE,
    N_ESTIMATORS,
    MAX_DEPTH,
    RANDOM_SEED,
)
from src.logger import get_logger

logger = get_logger(__name__)


class PerformanceModel:
    """Wraps a scikit-learn classifier with scaling, training and evaluation logic."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.clf = RandomForestClassifier(
            n_estimators=N_ESTIMATORS,
            max_depth=MAX_DEPTH,
            random_state=RANDOM_SEED,
            class_weight="balanced",
        )
        self.is_trained = False

    # -----------------------------------------------------------------
    def train(self, df: pd.DataFrame) -> dict:
        """Train the model on the given DataFrame and return evaluation metrics."""
        X = df[FEATURE_COLUMNS].values
        y = df[TARGET_COLUMN].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        logger.info("Training RandomForestClassifier on %d samples...", len(X_train))
        self.clf.fit(X_train_scaled, y_train)
        self.is_trained = True

        y_pred = self.clf.predict(X_test_scaled)

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, pos_label="Pass"),
            "recall": recall_score(y_test, y_pred, pos_label="Pass"),
            "f1_score": f1_score(y_test, y_pred, pos_label="Pass"),
            "confusion_matrix": confusion_matrix(y_test, y_pred, labels=["Pass", "Fail"]).tolist(),
            "classification_report": classification_report(y_test, y_pred),
            "feature_importances": dict(
                zip(FEATURE_COLUMNS, self.clf.feature_importances_.round(4))
            ),
        }

        logger.info("Training complete. Test accuracy: %.4f", metrics["accuracy"])
        return metrics

    # -----------------------------------------------------------------
    def predict_single(self, features: dict) -> tuple[str, float]:
        """Predict Pass/Fail for a single student, given a dict of feature values."""
        if not self.is_trained:
            raise RuntimeError("Model has not been trained or loaded yet.")

        x = np.array([[features[col] for col in FEATURE_COLUMNS]])
        x_scaled = self.scaler.transform(x)

        pred = self.clf.predict(x_scaled)[0]
        proba = self.clf.predict_proba(x_scaled)[0]
        confidence = float(max(proba))

        return pred, confidence

    # -----------------------------------------------------------------
    def save(self, model_path: str = MODEL_PATH, scaler_path: str = SCALER_PATH) -> None:
        with open(model_path, "wb") as f:
            pickle.dump(self.clf, f)
        with open(scaler_path, "wb") as f:
            pickle.dump(self.scaler, f)
        logger.info("Model saved to %s, scaler saved to %s", model_path, scaler_path)

    @classmethod
    def load(cls, model_path: str = MODEL_PATH, scaler_path: str = SCALER_PATH) -> "PerformanceModel":
        instance = cls()
        with open(model_path, "rb") as f:
            instance.clf = pickle.load(f)
        with open(scaler_path, "rb") as f:
            instance.scaler = pickle.load(f)
        instance.is_trained = True
        return instance


if __name__ == "__main__":
    from src.data_manager import load_or_generate_data, clean_data

    df = clean_data(load_or_generate_data())
    model = PerformanceModel()
    results = model.train(df)
    model.save()

    print("Accuracy :", round(results["accuracy"], 4))
    print("Precision:", round(results["precision"], 4))
    print("Recall   :", round(results["recall"], 4))
    print("F1 Score :", round(results["f1_score"], 4))
