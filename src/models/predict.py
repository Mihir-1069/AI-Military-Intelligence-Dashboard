import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import pandas as pd
import numpy as np
import joblib

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.load_data import load_csv_dataset
from src.utils.config import (
    MODEL_FILE_PATH, MODEL_METADATA_PATH, ENGINEERED_FEATURES_PATH, PREDICTIONS_PATH
)
from src.utils.helper import setup_logger, load_json

logger = setup_logger("predict")

def load_trained_model(model_path: Path = MODEL_FILE_PATH, metadata_path: Path = MODEL_METADATA_PATH) -> Tuple[Any, Dict[str, Any]]:
    """Loads joblib model artifact and JSON metadata."""
    model_path = Path(model_path)
    metadata_path = Path(metadata_path)

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}. Run training first.")
    
    model = joblib.load(model_path)
    metadata = load_json(metadata_path) if metadata_path.exists() else {}
    logger.info(f"Loaded trained model artifact from {model_path.name}")
    return model, metadata

def prepare_prediction_input(df: pd.DataFrame, feature_names: list) -> pd.DataFrame:
    """Prepares and aligns input feature matrix with training feature schema."""
    X = pd.DataFrame()
    for col in feature_names:
        if col in df.columns:
            X[col] = df[col]
        else:
            X[col] = 0.0
    
    # Impute missing coordinates & values
    X = X.fillna(0.0)
    return X

def generate_predictions(
    df: Optional[pd.DataFrame] = None,
    model_path: Path = MODEL_FILE_PATH,
    metadata_path: Path = MODEL_METADATA_PATH
) -> pd.DataFrame:
    """
    Generates aggregate risk predictions for given event dataset.
    Returns DataFrame containing original events along with predicted threat severity & probability.
    """
    model, metadata = load_trained_model(model_path, metadata_path)
    feature_names = metadata.get("feature_names", [])

    if df is None:
        logger.info("Loading engineered features dataset for inference...")
        df = load_csv_dataset(ENGINEERED_FEATURES_PATH)

    X_input = prepare_prediction_input(df, feature_names)

    # Generate model predictions & probabilities
    preds = model.predict(X_input)
    probs = model.predict_proba(X_input)[:, 1] if hasattr(model, "predict_proba") else preds.astype(float)

    # Attach prediction outputs to DataFrame
    output_df = df.copy()
    output_df["predicted_high_severity"] = preds
    output_df["threat_probability"] = np.round(probs, 4)
    output_df["aggregate_risk_category"] = np.where(probs >= 0.7, "High Risk", np.where(probs >= 0.4, "Moderate Risk", "Low Risk"))

    logger.info(f"Generated predictions for {len(output_df):,} events.")
    return output_df

def save_predictions(df: pd.DataFrame, output_path: Path = PREDICTIONS_PATH) -> Path:
    """Saves predictions DataFrame to CSV."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Predictions saved to {output_path}")
    return output_path

if __name__ == "__main__":
    preds_df = generate_predictions()
    save_predictions(preds_df)