import sys
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.config import CLEANED_DATA_PATH
from src.data.load_data import load_csv_dataset
from src.analysis.trend_analysis import (
    calculate_yearly_trend, calculate_year_over_year_change,
    calculate_rolling_average, detect_activity_spikes
)
from src.analysis.statistical_analysis import (
    calculate_attack_type_distribution, calculate_target_type_distribution
)
from src.dashboard.components.chart_helpers import create_timeline_chart, create_bar_chart
from src.dashboard.components.kpi_cards import render_kpi_grid

st.set_page_config(page_title="Threat Analysis - Military Intelligence Dashboard", page_icon="📊", layout="wide")

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

st.markdown("## 📊 Temporal & Tactical Threat Analysis")
st.caption("Deep-dive historical temporal trend shifts, YoY activity deltas, activity spikes, and tactical breakdowns.")

if df.empty:
    st.error("Cleaned dataset not found.")
    st.stop()

# Trend & YoY calculations
trend_df = calculate_yearly_trend(df)
trend_df = calculate_year_over_year_change(trend_df)
trend_df = calculate_rolling_average(trend_df, window=3)
trend_df = detect_activity_spikes(trend_df, z_threshold=1.5)

# --- SECTION A & B: YEARLY ACTIVITY & YOY DIRECTION ---
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### A. Historical Activity Trend (3-Year Rolling Average)")
    fig_line = create_timeline_chart(trend_df, title="Annual Incident & Casualty Volume")
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.markdown("### B. Recent YoY Shift")
    if len(trend_df) >= 2:
        latest = trend_df.iloc[-1]
        prev = trend_df.iloc[-2]
        yoy_pct = latest.get("event_yoy_pct", 0.0)
        
        if yoy_pct > 2.0:
            indicator = "↑ INCREASING"
            color = "#ef4444"
        elif yoy_pct < -2.0:
            indicator = "↓ DECREASING"
            color = "#10b981"
        else:
            indicator = "→ STABLE"
            color = "#f59e0b"

        yoy_html = (
            f'<div class="kpi-card" style="border-left: 4px solid {color}; margin-top: 10px;">'
            f'<div class="kpi-label">YoY Direction ({int(latest["iyear"])})</div>'
            f'<div class="kpi-value" style="color: {color}; font-size: 1.5rem;">{indicator}</div>'
            f'<div class="kpi-subtext">Change vs {int(prev["iyear"])}: <strong>{yoy_pct:+.1f}%</strong></div>'
            f'</div>'
        )
        st.markdown(yoy_html, unsafe_allow_html=True)
        
        st.metric("Latest Year Events", f"{int(latest['event_count']):,}")
        st.metric("Previous Year Events", f"{int(prev['event_count']):,}")

st.divider()

# --- SECTION C: ACTIVITY SPIKES ---
st.markdown("### C. Detected Historical Activity Spikes (Z-Score > 1.5)")
spikes_df = trend_df[trend_df["is_spike"]].copy()

if not spikes_df.empty:
    mean_baseline = trend_df["event_count"].mean()
    spikes_df["historical_baseline"] = round(mean_baseline, 1)
    spikes_df["deviation_pct"] = round(((spikes_df["event_count"] - mean_baseline) / mean_baseline) * 100, 1)
    
    display_spikes = spikes_df[["iyear", "event_count", "historical_baseline", "deviation_pct", "z_score"]].copy()
    display_spikes.columns = ["Year", "Observed Events", "Historical Baseline", "Deviation (%)", "Z-Score"]
    
    st.dataframe(display_spikes.style.format({
        "Year": "{:d}",
        "Observed Events": "{:,.0f}",
        "Historical Baseline": "{:,.1f}",
        "Deviation (%)": "{:+.1f}%",
        "Z-Score": "{:.2f}"
    }), use_container_width=True)
else:
    st.info("No activity spikes detected for current selection.")

st.divider()

# --- SECTION D: ATTACK PATTERN ANALYSIS ---
st.markdown("### D. Tactical Attack & Target Category Breakdown")
tab_attack, tab_target, tab_weapon = st.tabs(["Attack Tactics", "Target Types", "Weapon Categories"])

with tab_attack:
    atk_df = calculate_attack_type_distribution(df)
    fig_atk = create_bar_chart(atk_df, x_col="event_count", y_col="attacktype1_txt", title="Distribution by Tactical Attack Type", color_hex="#3b82f6", orientation="h")
    st.plotly_chart(fig_atk, use_container_width=True)

with tab_target:
    targ_df = calculate_target_type_distribution(df, top_n=15)
    fig_targ = create_bar_chart(targ_df, x_col="event_count", y_col="targtype1_txt", title="Top Target Categories", color_hex="#f59e0b", orientation="h")
    st.plotly_chart(fig_targ, use_container_width=True)

with tab_weapon:
    if "weaptype1_txt" in df.columns:
        weap_df = df["weaptype1_txt"].value_counts().head(12).reset_index()
        weap_df.columns = ["weaptype1_txt", "event_count"]
        fig_weap = create_bar_chart(weap_df, x_col="event_count", y_col="weaptype1_txt", title="Weapon Categories Used", color_hex="#10b981", orientation="h")
        st.plotly_chart(fig_weap, use_container_width=True)

st.divider()

# --- SECTION E: CASUALTY ANALYSIS ---
st.markdown("### E. Casualty Statistics & Severity Profile")
tot_k = int(df["nkill"].sum()) if "nkill" in df.columns else 0
tot_w = int(df["nwound"].sum()) if "nwound" in df.columns else 0
tot_c = tot_k + tot_w
fatality_rate = (tot_k / tot_c * 100) if tot_c > 0 else 0.0

kpi_cas = [
    {"label": "Total Fatalities (Killed)", "value": f"{tot_k:,}", "subtext": "Historical total", "color": "#ef4444"},
    {"label": "Total Wounded", "value": f"{tot_w:,}", "subtext": "Historical total", "color": "#f59e0b"},
    {"label": "Combined Casualties", "value": f"{tot_c:,}", "subtext": "Fatalities + Wounded", "color": "#38bdf8"},
    {"label": "Fatality Ratio", "value": f"{fatality_rate:.1f}%", "subtext": "Fatalities / Casualties", "color": "#10b981"}
]

render_kpi_grid(kpi_cas)
