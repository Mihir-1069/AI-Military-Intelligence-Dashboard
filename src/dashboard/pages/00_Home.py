import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Setup Root Directory Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.config import CLEANED_DATA_PATH
from src.data.load_data import load_csv_dataset
from src.dashboard.components.kpi_cards import render_kpi_grid
from src.dashboard.components.insight_cards import generate_dynamic_insights, render_insight_cards
from src.dashboard.components.chart_helpers import (
    create_timeline_chart, create_bar_chart, create_density_map
)
from src.analysis.trend_analysis import calculate_yearly_trend
from src.analysis.statistical_analysis import (
    calculate_region_distribution, calculate_attack_type_distribution
)

# Page Config
st.set_page_config(
    page_title="Home - AI Military Intelligence Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS Theme
css_path = ROOT_DIR / "src" / "dashboard" / "assets" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Data Loading with Cache
@st.cache_data
def get_cleaned_data():
    if not CLEANED_DATA_PATH.exists():
        return pd.DataFrame()
    return load_csv_dataset(CLEANED_DATA_PATH)

df_raw = get_cleaned_data()

if df_raw.empty:
    st.error("Cleaned dataset not found (`cleaned_data.csv`). Please run `python run.py preprocess`.")
    st.stop()

# Initialize Session State Filters
if "filter_years" not in st.session_state:
    st.session_state.filter_years = (int(df_raw["iyear"].min()), int(df_raw["iyear"].max()))
if "filter_regions" not in st.session_state:
    st.session_state.filter_regions = []
if "filter_countries" not in st.session_state:
    st.session_state.filter_countries = []
if "filter_attacks" not in st.session_state:
    st.session_state.filter_attacks = []

# --- SIDEBAR GLOBAL FILTERS ---
st.sidebar.markdown("### 🛡️ NAVIGATION & FILTERS")
st.sidebar.caption("Global Intelligence Dashboard Controls")
st.sidebar.markdown("#### ⚙️ Global Filters")

min_yr, max_yr = int(df_raw["iyear"].min()), int(df_raw["iyear"].max())
selected_years = st.sidebar.slider("Dataset Year Range", min_yr, max_yr, st.session_state.filter_years)

available_regions = sorted(list(df_raw["region_txt"].dropna().unique()))
selected_regions = st.sidebar.multiselect("Region Theater", available_regions, default=st.session_state.filter_regions)

# Dynamic country list based on region filter
if selected_regions:
    filtered_countries = sorted(list(df_raw[df_raw["region_txt"].isin(selected_regions)]["country_txt"].dropna().unique()))
else:
    filtered_countries = sorted(list(df_raw["country_txt"].dropna().unique()))

selected_countries = st.sidebar.multiselect("Country / Territory", filtered_countries, default=[c for c in st.session_state.filter_countries if c in filtered_countries])

available_attacks = sorted(list(df_raw["attacktype1_txt"].dropna().unique()))
selected_attacks = st.sidebar.multiselect("Attack Tactics", available_attacks, default=st.session_state.filter_attacks)

col_reset, col_apply = st.sidebar.columns(2)
if col_reset.button("Reset Filters"):
    st.session_state.filter_years = (min_yr, max_yr)
    st.session_state.filter_regions = []
    st.session_state.filter_countries = []
    st.session_state.filter_attacks = []
    st.rerun()

# Apply Filters Logic
df_filtered = df_raw[(df_raw["iyear"] >= selected_years[0]) & (df_raw["iyear"] <= selected_years[1])]

if selected_regions:
    df_filtered = df_filtered[df_filtered["region_txt"].isin(selected_regions)]

if selected_countries:
    df_filtered = df_filtered[df_filtered["country_txt"].isin(selected_countries)]

if selected_attacks:
    df_filtered = df_filtered[df_filtered["attacktype1_txt"].isin(selected_attacks)]

# --- HEADER BANNER ---
header_html = (
    f'<div class="header-banner">'
    f'<h1>AI-Powered Military Intelligence Dashboard</h1>'
    f'<p>Historical Terrorism Analysis & Aggregate Risk Assessment Platform &nbsp;|&nbsp; Dataset Period: {min_yr} - {max_yr} &nbsp;|&nbsp; Total Analyzed Events: {len(df_raw):,}</p>'
    f'</div>'
    f'<div class="disclaimer-banner">'
    f'<strong>ACADEMIC DEFENSIVE ANALYTICS DISCLAIMER:</strong> All analytical metrics, maps, and predictive Machine Learning scores in this platform are generated strictly for academic defense research and historical trend analysis. Tactical attack planning, individual targeting, and operational deployment recommendations are strictly prohibited.'
    f'</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("⚠️ No records match your selected filter criteria. Please adjust or reset filters.")
    st.stop()

# --- KPI CARDS GRID ---
total_events = len(df_filtered)
total_fatalities = int(df_filtered["nkill"].sum()) if "nkill" in df_filtered.columns else 0
total_wounded = int(df_filtered["nwound"].sum()) if "nwound" in df_filtered.columns else 0
total_casualties = total_fatalities + total_wounded
countries_count = df_filtered["country_txt"].nunique()
regions_count = df_filtered["region_txt"].nunique()
years_count = df_filtered["iyear"].nunique()

kpi_data = [
    {"label": "Total Events", "value": f"{total_events:,}", "subtext": f"Across {years_count} active years", "color": "#38bdf8"},
    {"label": "Total Casualties", "value": f"{total_casualties:,}", "subtext": f"{total_fatalities:,} killed | {total_wounded:,} wounded", "color": "#ef4444"},
    {"label": "Countries Affected", "value": f"{countries_count:,}", "subtext": "Sovereign territories", "color": "#3b82f6"},
    {"label": "Regions Affected", "value": f"{regions_count:,}", "subtext": "Geographic theaters", "color": "#f59e0b"},
    {"label": "Years Covered", "value": f"{years_count:,}", "subtext": f"{selected_years[0]} - {selected_years[1]}", "color": "#10b981"}
]

render_kpi_grid(kpi_data)

st.divider()

# --- MAIN TEMPORAL TREND ---
st.markdown("### 📈 Historical Threat Activity Over Time")
trend_df = calculate_yearly_trend(df_filtered)
fig_trend = create_timeline_chart(trend_df, title="Terrorist Events & Casualties Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

# --- SECONDARY ANALYSIS GRID ---
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🌍 Events by Regional Theater")
    region_df = calculate_region_distribution(df_filtered)
    fig_region = create_bar_chart(region_df.head(10), x_col="event_count", y_col="region_txt", title="Top Affected Regions", color_hex="#3b82f6", orientation="h")
    st.plotly_chart(fig_region, use_container_width=True)

with col_right:
    st.markdown("### ⚔️ Events by Attack Tactics")
    attack_df = calculate_attack_type_distribution(df_filtered)
    fig_attack = create_bar_chart(attack_df.head(10), x_col="event_count", y_col="attacktype1_txt", title="Top Tactical Attack Types", color_hex="#f59e0b", orientation="h")
    st.plotly_chart(fig_attack, use_container_width=True)

# --- GEOGRAPHIC OVERVIEW ---
st.markdown("### 🗺️ Geographic Activity Density Overview")
fig_map = create_density_map(df_filtered, max_points=4000)
st.plotly_chart(fig_map, use_container_width=True)

# --- DYNAMIC INSIGHT CARDS ---
insights = generate_dynamic_insights(df_filtered)
render_insight_cards(insights)
