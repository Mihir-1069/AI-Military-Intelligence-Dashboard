import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
YEARLY_DATA_DIR = DATA_DIR / "yearly"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
SRC_DIR = BASE_DIR / "src"

# Data Files
RAW_EXCEL_FILENAME = "globalterrorismdb_0522dist.xlsx"
RAW_EXCEL_PATH = RAW_DATA_DIR / RAW_EXCEL_FILENAME
DEFAULT_SHEET_NAME = "Data"

CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "cleaned_data.csv"
ENGINEERED_FEATURES_PATH = PROCESSED_DATA_DIR / "engineered_features.csv"
PREDICTIONS_PATH = PROCESSED_DATA_DIR / "predictions.csv"

MODEL_FILE_PATH = MODELS_DIR / "threat_model.pkl"
MODEL_METADATA_PATH = MODELS_DIR / "model_metadata.json"

# Key Selected Columns (Out of 135)
RELEVANT_COLUMNS = [
    "eventid",
    "iyear",
    "imonth",
    "iday",
    "country",
    "country_txt",
    "region",
    "region_txt",
    "provstate",
    "city",
    "latitude",
    "longitude",
    "location",
    "summary",
    "multiple",
    "success",
    "suicide",
    "attacktype1",
    "attacktype1_txt",
    "targtype1",
    "targtype1_txt",
    "target1",
    "natlty1",
    "natlty1_txt",
    "gname",
    "weaptype1",
    "weaptype1_txt",
    "nkill",
    "nwound",
    "property",
    "propvalue",
    "ishostkid"
]

# Numeric & Categorical Column definitions
NUMERIC_COLUMNS = ["nkill", "nwound", "latitude", "longitude", "propvalue"]
CATEGORICAL_COLUMNS = ["region_txt", "country_txt", "attacktype1_txt", "targtype1_txt", "weaptype1_txt"]
BINARY_COLUMNS = ["multiple", "success", "suicide", "property", "ishostkid"]

# Model Hyperparameters & Target Definition
TARGET_COLUMN = "high_severity_event"
RANDOM_STATE = 42
TEST_SIZE = 0.2
MODEL_TYPE = "RandomForestClassifier"

# Ensure all directories exist
for directory in [
    RAW_DATA_DIR,
    YEARLY_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    NOTEBOOKS_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)
