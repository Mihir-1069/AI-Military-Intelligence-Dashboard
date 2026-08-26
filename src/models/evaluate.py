import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.config import FIGURES_DIR, MODEL_METADATA_PATH, MODEL_FILE_PATH
from src.utils.helper import setup_logger, save_json, save_figure, load_json
from src.models.train import train_model

logger = setup_logger("evaluate_model")

def calculate_metrics(y_true: pd.Series, y_pred: np.ndarray, y_prob: Optional[np.ndarray] = None) -> Dict[str, float]:
    """Calculates accuracy, precision, recall, f1, and roc_auc metrics."""
    metrics = {
        "accuracy": float(round(accuracy_score(y_true, y_pred), 4)),
        "precision": float(round(precision_score(y_true, y_pred, zero_division=0), 4)),
        "recall": float(round(recall_score(y_true, y_pred, zero_division=0), 4)),
        "f1_score": float(round(f1_score(y_true, y_pred, zero_division=0), 4))
    }
    if y_prob is not None:
        try:
            metrics["roc_auc"] = float(round(roc_auc_score(y_true, y_prob), 4))
        except Exception:
            metrics["roc_auc"] = 0.0
    return metrics

def generate_confusion_matrix(y_true: pd.Series, y_pred: np.ndarray, save_fig: bool = True) -> np.ndarray:
    """Generates and plots confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                xticklabels=["Low/Moderate Risk", "High Risk"],
                yticklabels=["Low/Moderate Risk", "High Risk"])
    ax.set_title("Threat Classifier Confusion Matrix", fontsize=12, fontweight="bold")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")

    if save_fig:
        save_figure(fig, "confusion_matrix.png")
        plt.close(fig)
    return cm

def plot_feature_importance(model, feature_names: list, top_n: int = 15, save_fig: bool = True):
    """Plots top feature importances for Random Forest classifier."""
    if not hasattr(model, "feature_importances_"):
        return None

    importances = model.feature_importances_
    feat_df = pd.DataFrame({"feature": feature_names, "importance": importances})
    feat_df = feat_df.sort_values(by="importance", ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=feat_df, x="importance", y="feature", palette="viridis", ax=ax)
    ax.set_title("Model Feature Importance (Top Contributing Drivers)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Feature Importance (Gini Impurity Reduction)")
    ax.set_ylabel("Feature")

    if save_fig:
        save_figure(fig, "feature_importance.png")
        plt.close(fig)
    return feat_df

def evaluate_model(model=None, X_test=None, y_test=None) -> Dict[str, Any]:
    """
    Main evaluation pipeline:
    Calculates metrics -> Plots Confusion Matrix -> Plots Feature Importance -> Updates Metadata.
    """
    if model is None or X_test is None or y_test is None:
        logger.info("No model provided, running fresh training and evaluation...")
        model, metadata, X_test, y_test = train_model()
    else:
        metadata = load_json(MODEL_METADATA_PATH) if MODEL_METADATA_PATH.exists() else {}

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    metrics = calculate_metrics(y_test, y_pred, y_prob)
    logger.info(f"Evaluation Metrics: {metrics}")

    generate_confusion_matrix(y_test, y_pred)
    
    feature_names = metadata.get("feature_names", list(X_test.columns))
    plot_feature_importance(model, feature_names)

    # Update metadata with metrics
    metadata["metrics"] = metrics
    if MODEL_METADATA_PATH.exists():
        save_json(metadata, MODEL_METADATA_PATH)

    return metrics

if __name__ == "__main__":
    evaluate_model()