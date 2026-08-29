import sys
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.utils.config import CLEANED_DATA_PATH
from src.data.load_data import load_csv_dataset
from src.analysis.statistical_analysis import calculate_region_distribution
from src.dashboard.components.chart_helpers import (
    create_density_map, create_multi_region_line_chart, DARK_LAYOUT
)
from src.dashboard.components.kpi_cards import render_kpi_grid
import plotly.express as px

css_path = ROOT_DIR / "src" / "dashboard" / "assets" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if not CLEANED_DATA_PATH.exists():
        return pd.DataFrame()
    return load_csv_dataset(CLEANED_DATA_PATH)

df = load_data()

st.markdown("## 🌍 Regional Intelligence & Spatial Threat Analysis")
st.caption("Aggregate regional breakdown, relative activity share, geographic density heatmaps, and temporal theater comparisons.")

if df.empty:
    st.error("Cleaned dataset not found.")
    st.stop()

all_regions = sorted(list(df["region_txt"].dropna().unique()))

# Top Section: Primary Focus Region Selector
selected_primary_region = st.selectbox("🎯 Select Primary Analytical Region Theater", ["All Regions"] + all_regions)

if selected_primary_region != "All Regions":
    df_reg = df[df["region_txt"] == selected_primary_region]
else:
    df_reg = df

total_global_events = len(df)
reg_events = len(df_reg)
reg_fatalities = int(df_reg["nkill"].sum()) if "nkill" in df_reg.columns else 0
reg_wounded = int(df_reg["nwound"].sum()) if "nwound" in df_reg.columns else 0
reg_casualties = reg_fatalities + reg_wounded
activity_share = (reg_events / total_global_events) * 100

kpis_reg = [
    {"label": "Regional Event Count", "value": f"{reg_events:,}", "subtext": f"Out of {total_global_events:,} global", "color": "#38bdf8"},
    {"label": "Regional Casualties", "value": f"{reg_casualties:,}", "subtext": f"{reg_fatalities:,} killed | {reg_wounded:,} wounded", "color": "#ef4444"},
    {"label": "Global Activity Share", "value": f"{activity_share:.1f}%", "subtext": "Share of total events", "color": "#f59e0b"},
    {"label": "Countries Analyzed", "value": f"{df_reg['country_txt'].nunique():,}", "subtext": "In selected theater", "color": "#10b981"}
]

render_kpi_grid(kpis_reg)

st.divider()

# --- RANKED REGIONAL TABLE ---
st.markdown("### 🏆 Ranked Regional Intelligence Summary")
reg_table = calculate_region_distribution(df)
if not reg_table.empty:
    reg_table["activity_share_pct"] = round((reg_table["event_count"] / total_global_events) * 100, 2)
    reg_table["rank"] = range(1, len(reg_table) + 1)
    
    display_table = reg_table[["rank", "region_txt", "event_count", "total_casualties", "total_killed", "total_wounded", "activity_share_pct"]].copy()
    display_table.columns = ["Rank", "Region Theater", "Total Events", "Total Casualties", "Fatalities", "Wounded", "Activity Share (%)"]

    st.dataframe(
        display_table.style.format({
            "Rank": "{:d}",
            "Total Events": "{:,.0f}",
            "Total Casualties": "{:,.0f}",
            "Fatalities": "{:,.0f}",
            "Wounded": "{:,.0f}",
            "Activity Share (%)": "{:.2f}%"
        }).background_gradient(subset=["Total Events"], cmap="Blues"),
        use_container_width=True
    )

st.divider()

# --- REGIONAL AGGREGATE MAP ---
st.markdown("### 🗺️ Aggregate Regional Density Map")
fig_reg_map = create_density_map(df_reg, max_points=3500)
st.plotly_chart(fig_reg_map, use_container_width=True)

st.divider()

# --- REGIONAL TREND COMPARISON CHART ---
st.markdown("### 📈 Multi-Region Temporal Comparison")
st.caption("Select two or more region theaters to compare historical activity trends side-by-side.")

selected_compare_regions = st.multiselect(
    "Select Regions to Compare",
    all_regions,
    default=all_regions[:3] if len(all_regions) >= 3 else all_regions
)

if selected_compare_regions:
    fig_comp = create_multi_region_line_chart(df, selected_compare_regions, title="Regional Activity Comparison Over Time")
    st.plotly_chart(fig_comp, use_container_width=True)
else:
    st.info("Please select at least one region to view comparison.")
