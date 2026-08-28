import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any

# Ensure project root is in sys.path for relative imports
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.load_data import load_excel_dataset
from src.utils.config import RAW_EXCEL_PATH, RELEVANT_COLUMNS, NUMERIC_COLUMNS, YEARLY_DATA_DIR
from src.utils.helper import setup_logger

logger = setup_logger("split_by_year")

def split_dataset_by_year() -> None:
    """Split the raw GTD dataset into separate CSV files for each year.

    Files are saved under the YEARLY_DATA_DIR directory as <year>.csv.
    """
    df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)
    YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for year, group in df.groupby("iyear"):
        out_path = YEARLY_DATA_DIR / f"{year}.csv"
        group.to_csv(out_path, index=False)
        logger.info(f"Saved {len(group)} records for year {year} to {out_path}")

def get_basic_statistics(
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """Calculates basic statistical information for the dataset.

    Includes:
    - Total rows and columns
    - Missing values
    - Numeric statistics
    - Unique values
    """
    if df is None:
        logger.info("No DataFrame provided. Loading dataset...")
        df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)

    results = {}
    # Dataset shape
    results["total_rows"] = len(df)
    results["total_columns"] = len(df.columns)
    # Missing values
    results["missing_values"] = df.isnull().sum().to_dict()
    # Unique values
    results["unique_values"] = df.nunique().to_dict()
    # Numeric statistics
    available_numeric_columns = [col for col in NUMERIC_COLUMNS if col in df.columns]
    if available_numeric_columns:
        results["numeric_statistics"] = (
            df[available_numeric_columns].describe().to_dict()
        )
    else:
        results["numeric_statistics"] = {}
    logger.info(
        f"Calculated statistics for {results['total_rows']} rows "
        f"and {results['total_columns']} columns."
    )
    return results

def get_attack_type_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """Calculates frequency statistics for attack types."""
    if "attacktype1_txt" not in df.columns:
        logger.warning("Column 'attacktype1_txt' not found.")
        return pd.DataFrame()
    attack_stats = (
        df["attacktype1_txt"].value_counts(dropna=False).reset_index()
    )
    attack_stats.columns = ["attack_type", "count"]
    attack_stats["percentage"] = (attack_stats["count"] / attack_stats["count"].sum() * 100).round(2)
    logger.info(f"Calculated statistics for {len(attack_stats)} attack types.")
    return attack_stats

def get_country_statistics(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """Returns the top countries based on number of incidents."""
    if "country_txt" not in df.columns:
        logger.warning("Column 'country_txt' not found.")
        return pd.DataFrame()
    country_stats = (
        df["country_txt"].value_counts().head(top_n).reset_index()
    )
    country_stats.columns = ["country", "incident_count"]
    logger.info(f"Calculated top {len(country_stats)} country statistics.")
    return country_stats

def get_yearly_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """Calculates the number of incidents for each year."""
    if "iyear" not in df.columns:
        logger.warning("Column 'iyear' not found.")
        return pd.DataFrame()
    yearly_stats = (
        df.groupby("iyear").size().reset_index(name="incident_count").sort_values("iyear")
    )
    logger.info(f"Calculated yearly statistics for {len(yearly_stats)} years.")
    return yearly_stats

def get_summary_report(
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """Creates a complete statistical summary report."""
    if df is None:
        logger.info("Loading dataset for summary report...")
        df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)
    report = {
        "basic_statistics": get_basic_statistics(df),
        "top_attack_types": get_attack_type_statistics(df),
        "top_countries": get_country_statistics(df),
        "yearly_statistics": get_yearly_statistics(df)
    }
    logger.info("Statistical summary report created successfully.")
    return report

if __name__ == "__main__":
    split_dataset_by_year()

from pathlib import Path
import pandas as pd
import numpy as np

# Ensure project root is in sys.path for relative imports
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.load_data import load_excel_dataset
from src.utils.config import RAW_EXCEL_PATH, RELEVANT_COLUMNS, NUMERIC_COLUMNS, YEARLY_DATA_DIR
from src.utils.helper import setup_logger

logger = setup_logger("split_by_year")

def split_dataset_by_year() -> None:
    """Split the raw GTD dataset into separate CSV files for each year.

    Files are saved under the YEARLY_DATA_DIR directory as <year>.csv.
    """
    df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)
    YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for year, group in df.groupby("iyear"):
        out_path = YEARLY_DATA_DIR / f"{year}.csv"
        group.to_csv(out_path, index=False)
        logger.info(f"Saved {len(group)} records for year {year} to {out_path}")

def get_basic_statistics(
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Calculates basic statistical information for the dataset.

    Includes:
    - Total rows and columns
    - Missing values
    - Numeric statistics
    - Unique values
    """
    if df is None:
        logger.info("No DataFrame provided. Loading dataset...")
        df = load_excel_dataset(
            RAW_EXCEL_PATH,
            usecols=RELEVANT_COLUMNS
        )

    results = {}

    # Dataset shape
    results["total_rows"] = len(df)
    results["total_columns"] = len(df.columns)

    # Missing values
    results["missing_values"] = df.isnull().sum().to_dict()

    # Unique values
    results["unique_values"] = df.nunique().to_dict()

    # Numeric statistics
    available_numeric_columns = [
        col for col in NUMERIC_COLUMNS
        if col in df.columns
    ]

    if available_numeric_columns:
        results["numeric_statistics"] = (
            df[available_numeric_columns]
            .describe()
            .to_dict()
        )
    else:
        results["numeric_statistics"] = {}

    logger.info(
        f"Calculated statistics for {results['total_rows']} rows "
        f"and {results['total_columns']} columns."
    )

    return results

def get_attack_type_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates frequency statistics for attack types.
    """
    if "attacktype1_txt" not in df.columns:
        logger.warning("Column 'attacktype1_txt' not found.")
        return pd.DataFrame()

    attack_stats = (
        df["attacktype1_txt"]
        .value_counts(dropna=False)
        .reset_index()
    )

    attack_stats.columns = [
        "attack_type",
        "count"
    ]

    attack_stats["percentage"] = (
        attack_stats["count"]
        / attack_stats["count"].sum()
        * 100
    ).round(2)

    logger.info(
        f"Calculated statistics for "
        f"{len(attack_stats)} attack types."
    )

    return attack_stats

def get_country_statistics(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Returns the top countries based on number of incidents.
    """
    if "country_txt" not in df.columns:
        logger.warning("Column 'country_txt' not found.")
        return pd.DataFrame()

    country_stats = (
        df["country_txt"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    country_stats.columns = [
        "country",
        "incident_count"
    ]

    logger.info(
        f"Calculated top {len(country_stats)} country statistics."
    )

    return country_stats

def get_yearly_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates the number of incidents for each year.
    """
    if "iyear" not in df.columns:
        logger.warning("Column 'iyear' not found.")
        return pd.DataFrame()

    yearly_stats = (
        df.groupby("iyear")
        .size()
        .reset_index(name="incident_count")
        .sort_values("iyear")
    )

    logger.info(
        f"Calculated yearly statistics for "
        f"{len(yearly_stats)} years."
    )

    return yearly_stats

def get_summary_report(
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Creates a complete statistical summary report.
    """
    if df is None:
        logger.info("Loading dataset for summary report...")
        df = load_excel_dataset(
            RAW_EXCEL_PATH,
            usecols=RELEVANT_COLUMNS
        )

    report = {
        "basic_statistics": get_basic_statistics(df),
        "top_attack_types": get_attack_type_statistics(df),
        "top_countries": get_country_statistics(df),
        "yearly_statistics": get_yearly_statistics(df)
    }

    logger.info("Statistical summary report created successfully.")

    return report

if __name__ == "__main__":
    split_dataset_by_year()

from pathlib import Path
import pandas as pd

# Ensure project root is in sys.path for relative imports
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.load_data import load_excel_dataset
from src.utils.config import RAW_EXCEL_PATH, RELEVANT_COLUMNS, YEARLY_DATA_DIR
from src.utils.helper import setup_logger

logger = setup_logger("split_by_year")

def split_dataset_by_year() -> None:
    """Split the raw GTD dataset into separate CSV files for each year.

    Files are saved under the YEARLY_DATA_DIR directory as <year>.csv.
    """
    df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)
    YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for year, group in df.groupby("iyear"):
        out_path = YEARLY_DATA_DIR / f"{year}.csv"
        group.to_csv(out_path, index=False)
        logger.info(f"Saved {len(group)} records for year {year} to {out_path}")

if __name__ == "__main__":
    split_dataset_by_year()
from pathlib import Path
import pandas as pd

# Ensure project root is in sys.path for relative imports
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.load_data import load_excel_dataset
from src.utils.config import RAW_EXCEL_PATH, RELEVANT_COLUMNS, YEARLY_DATA_DIR
from src.utils.helper import setup_logger

logger = setup_logger("split_by_year")

def split_dataset_by_year() -> None:
    """Split the raw GTD dataset into separate CSV files for each year.

    Files are saved under the YEARLY_DATA_DIR directory as <year>.csv.
    """
    # Load the full dataset
    df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)
    # Ensure the output directory exists
    YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Group by year and save each group
    for year, group in df.groupby("iyear"):
        out_path = YEARLY_DATA_DIR / f"{year}.csv"
        group.to_csv(out_path, index=False)
        logger.info(f"Saved {len(group)} records for year {year} to {out_path}")

if __name__ == "__main__":
    split_dataset_by_year()

from pathlib import Path
import pandas as pd

from src.data.load_data import load_excel_dataset
from src.utils.config import RAW_EXCEL_PATH, RELEVANT_COLUMNS, YEARLY_DATA_DIR
from src.utils.helper import setup_logger

logger = setup_logger("split_by_year")

def split_dataset_by_year() -> None:
    """Split the raw GTD dataset into separate CSV files for each year.

    Files are saved under the ``YEARLY_DATA_DIR`` directory as ``<year>.csv``.
    """
    # Load the full dataset
    df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)
    # Ensure the output directory exists
    YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Group by year and save each group
    for year, group in df.groupby("iyear"):
        out_path = YEARLY_DATA_DIR / f"{year}.csv"
        group.to_csv(out_path, index=False)
        logger.info(f"Saved {len(group)} records for year {year} to {out_path}")

from pathlib import Path
import pandas as pd

from src.data.load_data import load_excel_dataset
from src.utils.config import RAW_EXCEL_PATH, RELEVANT_COLUMNS, YEARLY_DATA_DIR
from src.utils.helper import setup_logger

logger = setup_logger("split_by_year")

def split_dataset_by_year() -> None:
    """Split the raw GTD dataset into separate CSV files for each year.

    Files are saved under the ``YEARLY_DATA_DIR`` directory as ``<year>.csv``.
    """
    # Load the full dataset
    df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)
    # Ensure the output directory exists
    YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Group by year and save each group
    for year, group in df.groupby("iyear"):
        out_path = YEARLY_DATA_DIR / f"{year}.csv"
        group.to_csv(out_path, index=False)
        logger.info(f"Saved {len(group)} records for year {year} to {out_path}")

from pathlib import Path
import pandas as pd

from src.data.load_data import load_excel_dataset
from src.utils.config import RAW_EXCEL_PATH, RELEVANT_COLUMNS, YEARLY_DATA_DIR
from src.utils.helper import setup_logger

logger = setup_logger("split_by_year")

def split_dataset_by_year() -> None:
    """Split the raw GTD dataset into separate CSV files for each year.

    Files are saved under the ``YEARLY_DATA_DIR`` directory as ``<year>.csv``.
    """
    # Load the full dataset
    df = load_excel_dataset(RAW_EXCEL_PATH, usecols=RELEVANT_COLUMNS)
    # Ensure the output directory exists
    YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Group by year and save each group
    for year, group in df.groupby("iyear"):
        out_path = YEARLY_DATA_DIR / f"{year}.csv"
        group.to_csv(out_path, index=False)
        logger.info(f"Saved {len(group)} records for year {year} to {out_path}")

from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
import numpy as np


# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


from src.data.load_data import load_excel_dataset
from src.utils.config import RAW_EXCEL_PATH, RELEVANT_COLUMNS, NUMERIC_COLUMNS, YEARLY_DATA_DIR, YEARLY_DATA_DIR
from src.utils.helper import setup_logger


logger = setup_logger("statistical_analysis")


def get_basic_statistics(
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Calculates basic statistical information for the dataset.

    Includes:
    - Total rows and columns
    - Missing values
    - Numeric statistics
    - Unique values
    """

    if df is None:
        logger.info("No DataFrame provided. Loading dataset...")
        df = load_excel_dataset(
            RAW_EXCEL_PATH,
            usecols=RELEVANT_COLUMNS
        )

    results = {}

    # Dataset shape
    results["total_rows"] = len(df)
    results["total_columns"] = len(df.columns)

    # Missing values
    results["missing_values"] = df.isnull().sum().to_dict()

    # Unique values
    results["unique_values"] = df.nunique().to_dict()

    # Numeric statistics
    available_numeric_columns = [
        col for col in NUMERIC_COLUMNS
        if col in df.columns
    ]

    if available_numeric_columns:
        results["numeric_statistics"] = (
            df[available_numeric_columns]
            .describe()
            .to_dict()
        )
    else:
        results["numeric_statistics"] = {}

    logger.info(
        f"Calculated statistics for {results['total_rows']} rows "
        f"and {results['total_columns']} columns."
    )

    return results


def get_attack_type_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates frequency statistics for attack types.
    """

    if "attacktype1_txt" not in df.columns:
        logger.warning("Column 'attacktype1_txt' not found.")
        return pd.DataFrame()

    attack_stats = (
        df["attacktype1_txt"]
        .value_counts(dropna=False)
        .reset_index()
    )

    attack_stats.columns = [
        "attack_type",
        "count"
    ]

    attack_stats["percentage"] = (
        attack_stats["count"]
        / attack_stats["count"].sum()
        * 100
    ).round(2)

    logger.info(
        f"Calculated statistics for "
        f"{len(attack_stats)} attack types."
    )

    return attack_stats


def get_country_statistics(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Returns the top countries based on number of incidents.
    """

    if "country_txt" not in df.columns:
        logger.warning("Column 'country_txt' not found.")
        return pd.DataFrame()

    country_stats = (
        df["country_txt"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    country_stats.columns = [
        "country",
        "incident_count"
    ]

    logger.info(
        f"Calculated top {len(country_stats)} country statistics."
    )

    return country_stats


def get_yearly_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates the number of incidents for each year.
    """

    if "iyear" not in df.columns:
        logger.warning("Column 'iyear' not found.")
        return pd.DataFrame()

    yearly_stats = (
        df.groupby("iyear")
        .size()
        .reset_index(name="incident_count")
        .sort_values("iyear")
    )

    logger.info(
        f"Calculated yearly statistics for "
        f"{len(yearly_stats)} years."
    )

    return yearly_stats


def get_summary_report(
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Creates a complete statistical summary report.
    """

    if df is None:
        logger.info("Loading dataset for summary report...")
        df = load_excel_dataset(
            RAW_EXCEL_PATH,
            usecols=RELEVANT_COLUMNS
        )

    report = {
        "basic_statistics": get_basic_statistics(df),
        "top_attack_types": get_attack_type_statistics(df),
        "top_countries": get_country_statistics(df),
        "yearly_statistics": get_yearly_statistics(df)
    }

    logger.info("Statistical summary report created successfully.")

    return report


if __name__ == "__main__":

    logger.info("Running statistical analysis...")

    df = load_excel_dataset(
        RAW_EXCEL_PATH,
        usecols=RELEVANT_COLUMNS
    )

    basic_stats = get_basic_statistics(df)

    print("\n===== BASIC STATISTICS =====")
    print(f"Total Rows: {basic_stats['total_rows']}")
    print(f"Total Columns: {basic_stats['total_columns']}")

    print("\n===== TOP ATTACK TYPES =====")
    print(get_attack_type_statistics(df).head(10))

    print("\n===== TOP COUNTRIES =====")
    print(get_country_statistics(df, top_n=10))

    print("\n===== YEARLY STATISTICS =====")
    print(get_yearly_statistics(df).head(10))