import json
from pathlib import Path
import pandas as pd

# Import analysis helpers
from src.analysis.statistical_analysis import (
    calculate_yearly_counts,
    calculate_country_distribution,
    calculate_region_distribution,
    calculate_attack_type_distribution,
    calculate_target_type_distribution,
    calculate_casualty_statistics,
    generate_dataset_summary,
)

# Project config for data and reports
from src.utils.config import CLEANED_DATA_PATH, REPORTS_DIR

def _ensure_report_dir() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def _save_dataframe(df: pd.DataFrame, name: str) -> None:
    csv_path = REPORTS_DIR / f"{name}.csv"
    json_path = REPORTS_DIR / f"{name}.json"
    df.to_csv(csv_path, index=False)
    json_path.write_text(df.to_json(orient="records", indent=2), encoding="utf-8")

def _save_summary(summary: dict, name: str) -> None:
    json_path = REPORTS_DIR / f"{name}.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

def main() -> None:
    if not CLEANED_DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Cleaned data not found at {CLEANED_DATA_PATH}. Run 'python run.py preprocess' first."
        )
    df = pd.read_csv(CLEANED_DATA_PATH)

    # Run all analysis helpers
    yearly = calculate_yearly_counts(df)
    countries = calculate_country_distribution(df, top_n=15)
    regions = calculate_region_distribution(df)
    attacks = calculate_attack_type_distribution(df)
    targets = calculate_target_type_distribution(df, top_n=10)
    casualty_stats = calculate_casualty_statistics(df)
    dataset_summary = generate_dataset_summary(df)

    # Persist results
    _ensure_report_dir()
    _save_dataframe(yearly, "yearly_counts")
    _save_dataframe(countries, "top_countries")
    _save_dataframe(regions, "region_distribution")
    _save_dataframe(attacks, "attack_type_distribution")
    _save_dataframe(targets, "target_type_distribution")
    _save_summary(casualty_stats, "casualty_statistics")
    _save_summary(dataset_summary, "dataset_summary")
    print(f"[INFO] Analysis completed – reports saved to {REPORTS_DIR}")

if __name__ == "__main__":
    main()
