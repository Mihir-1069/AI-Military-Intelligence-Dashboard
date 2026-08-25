import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.config import MODEL_METADATA_PATH, FIGURES_DIR
from src.utils.helper import load_json
from src.dashboard.components.kpi_cards import render_kpi_grid
from src.dashboard.components.chart_helpers import DARK_LAYOUT

st.set_page_config(page_title="Model Performance - Military Intelligence Dashboard", page_icon="🤖", layout="wide")

css_path = ROOT_DIR / "src" / "dashboard" / "assets" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def get_metadata():
    if not MODEL_METADATA_PATH.exists():
        return None
    return load_json(MODEL_METADATA_PATH)

metadata = get_metadata()

st.markdown("## 🤖 Machine Learning Model Performance & Evaluation")
st.caption("Quantitative classifier evaluation, confusion matrix breakdown, Gini feature importances, and model specifications.")

if metadata is None:
    st.error("Model metadata (`models/model_metadata.json`) not found. Please train model via `python run.py train`.")
    st.stop()

metrics = metadata.get("metrics", {})

# --- TOP METRIC KPI CARDS ---
kpis_perf = [
    {"label": "Accuracy", "value": f"{metrics.get('accuracy', 0.0):.2%}", "subtext": "Overall correct ratio", "color": "#38bdf8"},
    {"label": "Precision", "value": f"{metrics.get('precision', 0.0):.2%}", "subtext": "Positive predictive power", "color": "#10b981"},
    {"label": "Recall", "value": f"{metrics.get('recall', 0.0):.2%}", "subtext": "Sensitivity / Detection rate", "color": "#f59e0b"},
    {"label": "F1 Score", "value": f"{metrics.get('f1_score', 0.0):.2%}", "subtext": "Harmonic mean P & R", "color": "#3b82f6"},
    {"label": "ROC-AUC", "value": f"{metrics.get('roc_auc', 0.0):.2%}", "subtext": "Area under ROC curve", "color": "#a855f7"}
]

render_kpi_grid(kpis_perf)

st.divider()

col_cm, col_fi = st.columns(2)

# --- CONFUSION MATRIX ---
with col_cm:
    st.markdown("### 🔍 Confusion Matrix Heatmap")
    cm_path = FIGURES_DIR / "confusion_matrix.png"
    if cm_path.exists():
        st.image(str(cm_path), use_container_width=True)
    else:
        st.info("Confusion matrix figure not found.")

# --- FEATURE IMPORTANCE ---
with col_fi:
    st.markdown("### ⚡ Feature Importance Drivers")
    feat_names = metadata.get("feature_names", [])
    
    fi_path = FIGURES_DIR / "feature_importance.png"
    if fi_path.exists():
        st.image(str(fi_path), use_container_width=True)
    else:
        st.info("Feature importance figure not found.")
        
    st.caption("💡 **Note**: Feature importance indicates model feature reliance during decision splitting and does not imply causation.")

st.divider()

# --- MODEL SPECIFICATION INFORMATION CARD ---
st.markdown("### 📋 Model Specifications & Metadata")

spec1, spec2, spec3 = st.columns(3)

with spec1:
    st.markdown(f"""
    - **Model Architecture**: `{metadata.get('model_type', 'RandomForestClassifier')}`
    - **Model Version**: `{metadata.get('version', '1.0.0')}`
    - **Training Date**: `{metadata.get('training_date', 'N/A')}`
    """)

with spec2:
    st.markdown(f"""
    - **Target Variable**: `{metadata.get('target_name', 'high_severity_event')}`
    - **Training Samples**: `{metadata.get('n_samples_train', 0):,}` events
    - **Test Samples**: `{metadata.get('n_samples_test', 0):,}` events
    """)

with spec3:
    hp = metadata.get("hyperparameters", {})
    st.markdown(f"""
    - **Number of Estimators**: `{hp.get('n_estimators', 100)}`
    - **Max Tree Depth**: `{hp.get('max_depth', 15)}`
    - **Class Weighting**: `{hp.get('class_weight', 'balanced')}`
    """)
