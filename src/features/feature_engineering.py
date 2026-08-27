import sys
from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.load_data import load_csv_dataset
from src.utils.config import CLEANED_DATA_PATH, ENGINEERED_FEATURES_PATH, TARGET_COLUMN
from src.utils.helper import setup_logger

logger = setup_logger("feature_engineering")

def create_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Creates domain-specific derived features from cleaned data."""
    df = df.copy()

    # Total casualties
    nkill = df["nkill"].fillna(0.0) if "nkill" in df.columns else 0.0
    nwound = df["nwound"].fillna(0.0) if "nwound" in df.columns else 0.0
    df["total_casualties"] = nkill + nwound

    # Casualty indicator flag
    df["has_casualties"] = (df["total_casualties"] > 0).astype(int)

    # Lethality ratio
    df["lethality_ratio"] = np.where(
        df["total_casualties"] > 0,
        df["nkill"] / df["total_casualties"],
        0.0
    )

    # Target Formulation: High Severity Aggregate Threat Event
    # High severity defined as total_casualties >= 1 OR suicide == 1 OR success == 1 with nkill >= 1
    suicide = df["suicide"].fillna(0) if "suicide" in df.columns else 0
    success = df["success"].fillna(0) if "success" in df.columns else 0
    
    df[TARGET_COLUMN] = (
        (df["total_casualties"] >= 1) | (suicide == 1)
    ).astype(int)

    logger.info(f"Created derived features & target '{TARGET_COLUMN}'. Positive target ratio: {df[TARGET_COLUMN].mean():.2%}")
    return df

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encodes categorical columns for Machine Learning compatibility."""
    df = df.copy()

    categorical_cols = [
        "region_txt", "country_txt", "attacktype1_txt",
        "targtype1_txt", "weaptype1_txt"
    ]

    for col in categorical_cols:
        if col in df.columns:
            # Frequency encoding for high-cardinality country & categorical text
            freq_map = df[col].value_counts(normalize=True).to_dict()
            df[f"{col}_freq"] = df[col].map(freq_map).fillna(0.0)
            
            # Code integer category ID
            df[f"{col}_code"] = df[col].astype("category").cat.codes

    return df

def engineer_features(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Main Feature Engineering Pipeline:
    Loads Cleaned Data -> Creates Derived Features & Target -> Encodes Categoricals -> Saves Features.
    """
    if df is None:
        logger.info("Loading cleaned dataset for feature engineering...")
        df = load_csv_dataset(CLEANED_DATA_PATH)

    logger.info(f"Engineering features on initial shape {df.shape}...")
    df = create_derived_features(df)
    df = encode_categorical_features(df)

    logger.info(f"Feature engineering completed. Final shape: {df.shape}")
    return df

def save_engineered_features(df: pd.DataFrame, output_path: Path = ENGINEERED_FEATURES_PATH) -> Path:
    """Saves engineered features to CSV."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Engineered features saved to {output_path} ({len(df):,} rows)")
    return output_path

if __name__ == "__main__":
    features_df = engineer_features()
    save_engineered_features(features_df)