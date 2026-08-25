import logging
import json
from pathlib import Path
import pandas as pd
from src.utils.config import FIGURES_DIR

def setup_logger(name: str = "military_intel") -> logging.Logger:
    """Setup and return standard logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def save_json(data: dict, file_path: Path) -> None:
    """Save dictionary to a JSON file safely."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_json(file_path: Path) -> dict:
    """Load JSON file safely."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_number(val: float or int) -> str:
    """Format numbers into readable strings with commas."""
    if pd.isna(val):
        return "N/A"
    if isinstance(val, float):
        return f"{val:,.2f}"
    return f"{val:,}"

def save_figure(fig, filename: str) -> Path:
    """Save matplotlib or seaborn figure safely."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURES_DIR / filename
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    return out_path
