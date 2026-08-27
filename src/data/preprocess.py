import sys
from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


from src.data.load_data import load_excel_dataset
from src.utils.config import (
    RAW_EXCEL_PATH,
    CLEANED_DATA_PATH,
    RELEVANT_COLUMNS,
    NUMERIC_COLUMNS,
    BINARY_COLUMNS,
)
from src.utils.helper import setup_logger


logger = setup_logger("preprocess")


def select_relevant_columns(
    df: pd.DataFrame,
    columns: Optional[list] = None
) -> pd.DataFrame:
    """
    Selects specified relevant columns present in dataframe.
    """
    target_cols = columns if columns else RELEVANT_COLUMNS
    existing_cols = [col for col in target_cols if col in df.columns]

    logger.info(
        f"Selected {len(existing_cols)} relevant columns."
    )

    return df[existing_cols].copy()


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate rows based on eventid or full row matching.
    """
    initial_count = len(df)

    if "eventid" in df.columns:
        df = df.drop_duplicates(
            subset=["eventid"],
            keep="first"
        )
    else:
        df = df.drop_duplicates(keep="first")

    removed = initial_count - len(df)

    logger.info(
        f"Removed {removed} duplicate rows. Remaining: {len(df):,} rows."
    )

    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts data types for numeric, year, date, and categorical columns.
    """
    df = df.copy()

    # Years & Dates
    for col in [
        "iyear",
        "imonth",
        "iday",
        "country",
        "region",
        "attacktype1",
        "targtype1",
        "weaptype1",
    ]:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(df[col], errors="coerce")
                .fillna(0)
                .astype(int)
            )

    # Numeric casualties & property values
    for col in ["nkill", "nwound", "propextent"]:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(df[col], errors="coerce")
                .fillna(0.0)
            )

    # Coordinates
    for col in ["latitude", "longitude"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Binary flags
    for col in BINARY_COLUMNS:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(df[col], errors="coerce")
                .fillna(0)
                .astype(int)
            )

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing values, replaces invalid coordinate sentinels (-99),
    normalizes text.
    """
    df = df.copy()

    # Clean text columns
    string_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

        df[col] = df[col].replace(
            ["nan", "Unknown", "unknown", "", "Unknown"],
            np.nan
        )

    # Coordinate validation (-99 is sentinel for missing in GTD)
    if "latitude" in df.columns:
        df["latitude"] = df["latitude"].replace(
            [-99, -99.0],
            np.nan
        )

        df.loc[
            (df["latitude"] < -90)
            | (df["latitude"] > 90),
            "latitude"
        ] = np.nan

    if "longitude" in df.columns:
        df["longitude"] = df["longitude"].replace(
            [-99, -99.0],
            np.nan
        )

        df.loc[
            (df["longitude"] < -180)
            | (df["longitude"] > 180),
            "longitude"
        ] = np.nan

    # Fill missing text placeholders
    text_defaults = {
        "country_txt": "Unknown",
        "region_txt": "Unknown",
        "attacktype1_txt": "Unknown",
        "targtype1_txt": "Unknown",
        "weaptype1_txt": "Unknown",
        "gname": "Unknown Group",
        "city": "Unknown City",
        "provstate": "Unknown State",
    }

    for col, default_val in text_defaults.items():
        if col in df.columns:
            df[col] = df[col].fillna(default_val)

    return df


def clean_dataset(
    df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Main preprocessing pipeline:
    Loads -> Selects Columns -> Converts Types -> Removes Duplicates ->
    Cleans Missing -> Validates Years.
    """
    if df is None:
        logger.info(
            "Loading raw Excel dataset for cleaning..."
        )

        df = load_excel_dataset(
            RAW_EXCEL_PATH,
            usecols=RELEVANT_COLUMNS
        )

    logger.info(
        f"Starting data preprocessing on shape {df.shape}..."
    )

    df = select_relevant_columns(df)
    df = convert_data_types(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)

    # Filter invalid years (e.g. iyear == 0)
    if "iyear" in df.columns:
        df = df[df["iyear"] >= 1970].copy()

    logger.info(
        f"Preprocessing completed. Cleaned dataset shape: {df.shape}"
    )

    return df


def save_cleaned_data(
    df: pd.DataFrame,
    output_path: Path = CLEANED_DATA_PATH
) -> Path:
    """
    Saves cleaned DataFrame to CSV file.
    """
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    logger.info(
        f"Cleaned dataset saved to {output_path} ({len(df):,} rows)"
    )

    return output_path


if __name__ == "__main__":
    cleaned_df = clean_dataset()
    save_cleaned_data(cleaned_df)