from pathlib import Path
from typing import Optional, List, Dict, Any

import pandas as pd

from src.utils.config import RAW_EXCEL_PATH, DEFAULT_SHEET_NAME, RELEVANT_COLUMNS
from src.utils.helper import setup_logger


logger = setup_logger("load_data")


def load_excel_dataset(
    file_path: Path = RAW_EXCEL_PATH,
    sheet_name: str = DEFAULT_SHEET_NAME,
    usecols: Optional[List[str]] = RELEVANT_COLUMNS,
    nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Loads Excel GTD dataset safely using pathlib.
    Configurable sheet name and usecols to optimize memory.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw Excel dataset not found at: {file_path}"
        )

    logger.info(
        f"Loading Excel dataset from {file_path.name} "
        f"(sheet: {sheet_name})..."
    )

    try:
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            usecols=usecols,
            nrows=nrows
        )

        logger.info(
            f"Successfully loaded dataset with shape: {df.shape}"
        )

        return df

    except Exception as e:
        logger.error(f"Error loading Excel file: {e}")
        raise


def load_csv_dataset(
    file_path: Path,
    usecols: Optional[List[str]] = None,
    nrows: Optional[int] = None
) -> pd.DataFrame:
    """Loads CSV dataset safely using pathlib."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV dataset not found at: {file_path}"
        )

    logger.info(
        f"Loading CSV dataset from {file_path.name}..."
    )

    try:
        df = pd.read_csv(
            file_path,
            usecols=usecols,
            nrows=nrows,
            low_memory=False
        )

        logger.info(
            f"Successfully loaded CSV with shape: {df.shape}"
        )

        return df

    except Exception as e:
        logger.error(f"Error loading CSV file: {e}")
        raise


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: List[str]
) -> bool:
    """Validates if all required columns are present in dataframe."""

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        logger.error(
            f"Dataset missing required columns: {missing}"
        )
        raise ValueError(
            f"Missing required columns in dataset: {missing}"
        )

    logger.info("All required columns present in dataset.")

    return True


def get_dataset_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Returns dataset summary statistics and column information."""

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_counts": df.isnull().sum().to_dict(),
        "memory_usage_mb": round(
            df.memory_usage(deep=True).sum() / (1024 * 1024),
            2
        )
    }


if __name__ == "__main__":

    df = load_excel_dataset(nrows=50)

    validate_required_columns(
        df,
        ["eventid", "iyear", "country_txt"]
    )

    info = get_dataset_info(df)

    print(
        "Dataset Info Preview:",
        info["rows"],
        "rows,",
        info["columns"],
        "columns"
    )