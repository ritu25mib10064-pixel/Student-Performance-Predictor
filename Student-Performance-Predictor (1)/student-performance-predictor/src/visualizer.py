"""
visualizer.py
-------------
Module 3: Reporting & Visualization

Generates the charts used in the dashboard / final report:
  - Class distribution (Pass vs Fail)
  - Feature importance bar chart
  - Confusion matrix heatmap
  - Correlation heatmap of features
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless rendering, no display needed
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import OUTPUTS_DIR, FEATURE_COLUMNS, TARGET_COLUMN
from src.logger import get_logger

logger = get_logger(__name__)
sns.set_theme(style="whitegrid")


def plot_class_distribution(df: pd.DataFrame, save_as: str = "class_distribution.png") -> str:
    fig, ax = plt.subplots(figsize=(5, 4))
    counts = df[TARGET_COLUMN].value_counts()
    colors = ["#4C9F70", "#D9534F"]
    ax.bar(counts.index, counts.values, color=colors[: len(counts)])
    ax.set_title("Class Distribution: Pass vs Fail")
    ax.set_ylabel("Number of Students")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 2, str(v), ha="center", fontweight="bold")
    path = os.path.join(OUTPUTS_DIR, save_as)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logger.info("Saved chart: %s", path)
    return path


def plot_feature_importance(importances: dict, save_as: str = "feature_importance.png") -> str:
    items = sorted(importances.items(), key=lambda x: x[1])
    labels = [i[0].replace("_", " ").title() for i in items]
    values = [i[1] for i in items]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(labels, values, color="#4472C4")
    ax.set_title("Feature Importance (Random Forest)")
    ax.set_xlabel("Importance Score")
    path = os.path.join(OUTPUTS_DIR, save_as)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logger.info("Saved chart: %s", path)
    return path


def plot_confusion_matrix(cm: list, labels=("Pass", "Fail"), save_as: str = "confusion_matrix.png") -> str:
    cm = np.array(cm)
    fig, ax = plt.subplots(figsize=(4.5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels,
                yticklabels=labels, ax=ax, cbar=False)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    path = os.path.join(OUTPUTS_DIR, save_as)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logger.info("Saved chart: %s", path)
    return path


def plot_correlation_heatmap(df: pd.DataFrame, save_as: str = "correlation_heatmap.png") -> str:
    corr = df[FEATURE_COLUMNS].corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Feature Correlation Heatmap")
    path = os.path.join(OUTPUTS_DIR, save_as)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logger.info("Saved chart: %s", path)
    return path


def generate_all_visuals(df: pd.DataFrame, metrics: dict) -> list:
    """Convenience function to generate every chart in one call."""
    paths = [
        plot_class_distribution(df),
        plot_feature_importance(metrics["feature_importances"]),
        plot_confusion_matrix(metrics["confusion_matrix"]),
        plot_correlation_heatmap(df),
    ]
    return paths


if __name__ == "__main__":
    from src.data_manager import load_or_generate_data, clean_data
    from src.model import PerformanceModel

    df = clean_data(load_or_generate_data())
    model = PerformanceModel()
    metrics = model.train(df)
    generate_all_visuals(df, metrics)
    print("All visuals generated in:", OUTPUTS_DIR)
