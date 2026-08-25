import sys
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.config import MODEL_FILE_PATH, MODEL_METADATA_PATH, CLEANED_DATA_PATH
from src.data.load_data import load_csv_dataset
from src.models.predict import load_trained_model, prepare_prediction_input
from src.dashboard.components.risk_card import render_risk_assessment_card
from src.dashboard.components.chart_helpers import create_timeline_chart
from src.analysis.trend_analysis import calculate_yearly_trend

st.set_page_config(page_title="Risk Assessment - Military Intelligence Dashboard", page_icon="⚠️", layout="wide")

css_path = ROOT_DIR / "src" / "dashboard" / "assets" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_resource
def get_model():
    if not MODEL_FILE_PATH.exists():
        return None, None
    return load_trained_model(MODEL_FILE_PATH, MODEL_METADATA_PATH)

@st.cache_data
def load_data():
    if not CLEANED_DATA_PATH.exists():
        return pd.DataFrame()
    return load_csv_dataset(CLEANED_DATA_PATH)

model, metadata = get_model()
df_clean = load_data()

st.markdown("## ⚠️ Machine Learning Aggregate Risk Assessment")
st.caption("Structured threat classification evaluation using trained RandomForest model (Predicting Aggregate Severity Category).")

disclaimer_html = (
    '<div class="disclaimer-banner">'
    '<strong>ANALYTICAL MODEL SCOPE:</strong> This Machine Learning risk assessment tool provides aggregate statistical classification based on historical event patterns. Outputs represent probabilistic model evaluation and <strong>MUST NOT</strong> be used for operational targeting or tactical military decisions.'
    '</div>'
)
st.markdown(disclaimer_html, unsafe_allow_html=True)

if model is None or df_clean.empty:
    st.error("Trained ML model (`threat_model.pkl`) or dataset missing. Please execute `python run.py train`.")
    st.stop()

# --- INPUT PANEL & SELECTION ---
st.markdown("### ⚙️ Analytical Input Attributes")

regions = sorted(list(df_clean["region_txt"].dropna().unique()))
attacks = sorted(list(df_clean["attacktype1_txt"].dropna().unique()))
targets = sorted(list(df_clean["targtype1_txt"].dropna().unique()))
weapons = sorted(list(df_clean["weaptype1_txt"].dropna().unique()))

col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    sel_region = st.selectbox("Region Theater", regions, index=0)
    sel_attack = st.selectbox("Tactical Attack Type", attacks, index=0)

with col_in2:
    sel_target = st.selectbox("Target Category", targets, index=0)
    sel_weapon = st.selectbox("Weapon Category", weapons, index=0)

with col_in3:
    sel_suicide = st.radio("Suicide Tactical Flag", ["No (0)", "Yes (1)"], horizontal=True)
    sel_success = st.radio("Attack Success Flag", ["Yes (1)", "No (0)"], horizontal=True)

# Build Feature Vector
reg_code = regions.index(sel_region) if sel_region in regions else 0
atk_code = attacks.index(sel_attack) if sel_attack in attacks else 0
targ_code = targets.index(sel_target) if sel_target in targets else 0
weap_code = weapons.index(sel_weapon) if sel_weapon in weapons else 0

input_dict = {
    "iyear": 2020,
    "imonth": 6,
    "iday": 15,
    "region_txt_code": reg_code,
    "country_txt_code": 0,
    "attacktype1_txt_code": atk_code,
    "targtype1_txt_code": targ_code,
    "weaptype1_txt_code": weap_code,
    "region_txt_freq": 0.1,
    "country_txt_freq": 0.05,
    "attacktype1_txt_freq": 0.4,
    "targtype1_txt_freq": 0.2,
    "weaptype1_txt_freq": 0.5,
    "multiple": 0,
    "success": 1 if "Yes" in sel_success else 0,
    "suicide": 1 if "Yes" in sel_suicide else 0,
    "property": 1,
    "ishostkid": 0,
    "latitude": 33.3,
    "longitude": 44.3
}

feature_names = metadata.get("feature_names", list(input_dict.keys()))
X_input = prepare_prediction_input(pd.DataFrame([input_dict]), feature_names)

# Generate Model Prediction
prob = float(model.predict_proba(X_input)[0][1]) if hasattr(model, "predict_proba") else float(model.predict(X_input)[0])

if prob >= 0.65:
    risk_cat = "HIGH"
elif prob >= 0.35:
    risk_cat = "MODERATE"
else:
    risk_cat = "LOW"

confidence = "HIGH" if abs(prob - 0.5) > 0.2 else "MODERATE"

st.divider()

# --- STRUCTURED RISK CARD ---
st.markdown("### 🎯 Model Risk Assessment Output")

supporting_signals = {
    "Region Theater": sel_region,
    "Attack Type": sel_attack,
    "Target Category": sel_target,
    "Suicide Flag": sel_suicide,
    "Success Flag": sel_success
}

render_risk_assessment_card(
    risk_category=risk_cat,
    probability=prob,
    confidence_level=confidence,
    supporting_signals=supporting_signals,
    model_name=metadata.get("model_type", "RandomForestClassifier")
)

st.progress(prob)

st.caption("Note: Supporting feature signals reflect model feature reliance for statistical classification and do not imply direct causation.")

st.divider()

# --- HISTORICAL RISK TREND FOR SELECTED REGION ---
st.markdown(f"### 📈 Historical Threat Volume Trend for `{sel_region}`")
df_sub = df_clean[df_clean["region_txt"] == sel_region]
if not df_sub.empty:
    sub_trend = calculate_yearly_trend(df_sub)
    fig_sub = create_timeline_chart(sub_trend, title=f"Annual Events in {sel_region}")
    st.plotly_chart(fig_sub, use_container_width=True)
else:
    st.info(f"No historical trend data available for region {sel_region}.")
