import sys
import argparse
from pathlib import Path

# Ensure root directory in python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.helper import setup_logger
from src.utils.config import CLEANED_DATA_PATH, ENGINEERED_FEATURES_PATH, MODEL_FILE_PATH

logger = setup_logger("cli")

def run_split():
    logger.info("--- Stage 1: Splitting Dataset by Year ---")
    from src.data.split_by_year import split_dataset_by_year
    split_dataset_by_year()

def run_preprocess():
    logger.info("--- Stage 2: Data Preprocessing & Cleaning ---")
    from src.data.preprocess import clean_dataset, save_cleaned_data
    df = clean_dataset()
    save_cleaned_data(df)

def run_features():
    logger.info("--- Stage 3: Feature Engineering ---")
    if not CLEANED_DATA_PATH.exists():
        logger.error("Cleaned dataset not found. Please run preprocessing stage first.")
        sys.exit(1)
    from src.features.feature_engineering import engineer_features, save_engineered_features
    df = engineer_features()
    save_engineered_features(df)

def run_train():
    logger.info("--- Stage 4: Machine Learning Model Training ---")
    if not ENGINEERED_FEATURES_PATH.exists():
        logger.error("Engineered features dataset not found. Please run features stage first.")
        sys.exit(1)
    from src.models.train import train_model, save_model
    model, metadata, X_test, y_test = train_model()
    save_model(model, metadata)

def run_evaluate():
    logger.info("--- Stage 5: Model Evaluation ---")
    if not MODEL_FILE_PATH.exists():
        logger.error("Trained model artifact not found. Please run train stage first.")
        sys.exit(1)
    from src.models.evaluate import evaluate_model
    evaluate_model()

def run_predict():
    logger.info("--- Stage 6: Prediction Generation ---")
    if not MODEL_FILE_PATH.exists():
        logger.error("Trained model artifact not found. Please run train stage first.")
        sys.exit(1)
    from src.models.predict import generate_predictions, save_predictions
    preds_df = generate_predictions()
    save_predictions(preds_df)

def run_dashboard():
    logger.info("--- Launching Streamlit Dashboard ---")
    import subprocess, sys
    app_path = ROOT_DIR / "src" / "dashboard" / "app.py"
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to launch Streamlit dashboard: {e}")

def run_all():
    logger.info("=== Executing Full End-to-End Pipeline ===")
    run_split()
    run_preprocess()
    run_features()
    run_train()
    run_evaluate()
    run_predict()
    logger.info("=== Pipeline Execution Finished Successfully ===")

def main():
    parser = argparse.ArgumentParser(
        description="AI-Military-Intelligence-Dashboard Command Line Execution Interface"
    )
    parser.add_argument(
        "stage",
        choices=["split", "preprocess", "features", "train", "evaluate", "predict", "dashboard", "analysis", "all"],
        help="Pipeline execution stage"
    )
    args = parser.parse_args()


    from src.analysis.run_analysis import main as run_analysis
    stage_map = {
        "split": run_split,
        "preprocess": run_preprocess,
        "features": run_features,
        "train": run_train,
        "evaluate": run_evaluate,
        "predict": run_predict,
        "dashboard": run_dashboard,
        "analysis": run_analysis,
        "all": run_all
    }

    stage_map[args.stage]()

if __name__ == "__main__":
    main()
