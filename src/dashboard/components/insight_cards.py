from typing import List
import pandas as pd
import streamlit as st

def generate_dynamic_insights(df: pd.DataFrame) -> List[str]:
    """Generates automated analytical insights formatted with pure HTML tags."""
    insights = []
    if df.empty:
        return ["No data available for current filter selection."]

    total_events = len(df)
    
    # 1. Dominant Region Share
    if "region_txt" in df.columns:
        reg_counts = df["region_txt"].value_counts()
        top_reg = reg_counts.index[0]
        top_reg_pct = (reg_counts.iloc[0] / total_events) * 100
        insights.append(f"<strong>Dominant Regional Theater:</strong> <strong>{top_reg}</strong> accounts for <strong>{top_reg_pct:.1f}%</strong> ({reg_counts.iloc[0]:,} events) of filtered historical activity.")

    # 2. Dominant Attack Tactic
    if "attacktype1_txt" in df.columns:
        atk_counts = df["attacktype1_txt"].value_counts()
        top_atk = atk_counts.index[0]
        top_atk_pct = (atk_counts.iloc[0] / total_events) * 100
        insights.append(f"<strong>Primary Attack Tactic:</strong> <strong>{top_atk}</strong> represents <strong>{top_atk_pct:.1f}%</strong> of all recorded incidents.")

    # 3. Lethality Ratio
    if "nkill" in df.columns and "nwound" in df.columns:
        total_k = df["nkill"].sum()
        total_w = df["nwound"].sum()
        total_cas = total_k + total_w
        if total_cas > 0:
            fatality_rate = (total_k / total_cas) * 100
            insights.append(f"<strong>Casualty Fatality Ratio:</strong> Fatalities constitute <strong>{fatality_rate:.1f}%</strong> ({int(total_k):,} killed) of total casualties ({int(total_cas):,} total).")

    # 4. Recent YoY Trend
    if "iyear" in df.columns:
        yearly = df.groupby("iyear").size().sort_index()
        if len(yearly) >= 2:
            last_yr, prev_yr = yearly.iloc[-1], yearly.iloc[-2]
            yr_curr, yr_prev = yearly.index[-1], yearly.index[-2]
            pct_chg = ((last_yr - prev_yr) / prev_yr) * 100 if prev_yr > 0 else 0.0
            direction = "increased" if pct_chg > 0 else "decreased"
            insights.append(f"<strong>Recent Temporal Shift:</strong> Recorded events <strong>{direction} by {abs(pct_chg):.1f}%</strong> between {yr_prev} ({prev_yr:,} events) and {yr_curr} ({last_yr:,} events).")

    return insights

def render_insight_cards(insights: List[str]) -> None:
    """Renders styled analytical insight cards with valid DOM structure."""
    st.subheader("💡 Dynamic Analytical Insights")
    for insight in insights:
        html_code = f'<div class="insight-card">{insight}</div>'
        st.markdown(html_code, unsafe_allow_html=True)
