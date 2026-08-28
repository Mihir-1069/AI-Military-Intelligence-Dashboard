import sys
import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Any,Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.load_data import load_csv_dataset
from src.utils.config import (
    ENGINEERED_FEATURES_PATH, MODEL_FILE_PATH, MODEL_METADATA_PATH,
    TARGET_COLUMN, RANDOM_STATE, TEST_SIZE, MODEL_TYPE
)
from src.utils.helper import setup_logger, save_json

logger = setup_logger("train_model")

# Selected Non-Leaking Predictor Features
PREDICTOR_FEATURES = [
    "iyear", "imonth", "iday",
    "region_txt_code", "country_txt_code",
    "attacktype1_txt_code", "targtype1_txt_code", "weaptype1_txt_code",
    "region_txt_freq", "country_txt_freq",
    "attacktype1_txt_freq", "targtype1_txt_freq", "weaptype1_txt_freq",
    "multiple", "success", "suicide", "property", "ishostkid",
    "latitude", "longitude"
]

def prepare_training_data(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN,
    feature_cols: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """Filters valid features and target, imputing missing values safely."""
    df = df.copy()
    if feature_cols is None:
        feature_cols = [c for c in PREDICTOR_FEATURES if c in df.columns]

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    # Impute missing coordinates & numeric features with median/0
    X["latitude"] = X["latitude"].fillna(X["latitude"].median() if not X["latitude"].dropna().empty else 0.0)
    X["longitude"] = X["longitude"].fillna(X["longitude"].median() if not X["longitude"].dropna().empty else 0.0)
    X = X.fillna(0)

    logger.info(f"Prepared training dataset: {X.shape[0]:,} rows, {X.shape[1]} features.")
    return X, y, feature_cols

def build_model(
    n_estimators: int = 100,
    max_depth: int = 15,
    random_state: int = RANDOM_STATE
) -> RandomForestClassifier:
    """Instantiates RandomForestClassifier baseline model."""
    logger.info(f"Building RandomForestClassifier (n_estimators={n_estimators}, max_depth={max_depth})...")
    return RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1
    )

def train_model(
    df: Optional[pd.DataFrame] = None
) -> Tuple[RandomForestClassifier, Dict[str, Any], pd.DataFrame, pd.Series]:
    """
    Main training routine:
    Loads features -> Prepares X, y -> Split train/test -> Trains RandomForest -> Returns model & stats.
    """
    if df is None:
        logger.info("Loading engineered features dataset...")
        df = load_csv_dataset(ENGINEERED_FEATURES_PATH)

    X, y, feature_cols = prepare_training_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    logger.info(f"Train set shape: {X_train.shape}, Test set shape: {X_test.shape}")
    
    model = build_model()
    model.fit(X_train, y_train)
    logger.info("Model training complete.")

    training_metadata = {
        "model_type": MODEL_TYPE,
        "version": "1.0.0",
        "training_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_name": TARGET_COLUMN,
        "feature_names": feature_cols,
        "n_samples_train": int(len(X_train)),
        "n_samples_test": int(len(X_test)),
        "hyperparameters": {
            "n_estimators": model.n_estimators,
            "max_depth": model.max_depth,
            "class_weight": model.class_weight,
            "random_state": RANDOM_STATE
        }
    }

    return model, training_metadata, X_test, y_test

def save_model(
    model: RandomForestClassifier,
    metadata: Dict[str, Any],
    model_path: Path = MODEL_FILE_PATH,
    metadata_path: Path = MODEL_METADATA_PATH
) -> None:
    """Saves trained model with joblib and writes JSON metadata."""
    model_path = Path(model_path)
    metadata_path = Path(metadata_path)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)
    logger.info(f"Model persisted to {model_path}")

    save_json(metadata, metadata_path)
    logger.info(f"Model metadata persisted to {metadata_path}")

if __name__ == "__main__":
    model, metadata, X_test, y_test = train_model()
    save_model(model, metadata)