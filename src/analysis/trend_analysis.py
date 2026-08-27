from typing import Dict, Any
import pandas as pd
import numpy as np

def calculate_yearly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates yearly aggregate event and casualty trends."""
    if "iyear" not in df.columns:
        return pd.DataFrame()

    trend = df.groupby("iyear").agg(
        event_count=("eventid", "count"),
        total_killed=("nkill", "sum") if "nkill" in df.columns else ("eventid", "count"),
        total_wounded=("nwound", "sum") if "nwound" in df.columns else ("eventid", "count")
    ).reset_index()

    trend["total_casualties"] = trend["total_killed"] + trend["total_wounded"]
    return trend.sort_values("iyear")

def calculate_year_over_year_change(trend_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates Year-over-Year (YoY) percentage change for events and casualties."""
    trend_df = trend_df.copy()
    if "event_count" in trend_df.columns:
        trend_df["event_yoy_pct"] = trend_df["event_count"].pct_change() * 100
    if "total_casualties" in trend_df.columns:
        trend_df["casualty_yoy_pct"] = trend_df["total_casualties"].pct_change() * 100
    return trend_df

def calculate_rolling_average(trend_df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """Calculates rolling averages (e.g. 3-year or 5-year) for temporal trends."""
    trend_df = trend_df.copy()
    if "event_count" in trend_df.columns:
        trend_df[f"event_rolling_{window}yr"] = trend_df["event_count"].rolling(window=window, min_periods=1).mean()
    if "total_casualties" in trend_df.columns:
        trend_df[f"casualty_rolling_{window}yr"] = trend_df["total_casualties"].rolling(window=window, min_periods=1).mean()
    return trend_df

def detect_activity_spikes(trend_df: pd.DataFrame, z_threshold: float = 1.5) -> pd.DataFrame:
    """Detects historical anomaly/activity spikes using z-score threshold on event counts."""
    trend_df = trend_df.copy()
    if "event_count" not in trend_df.columns or len(trend_df) < 3:
        trend_df["is_spike"] = False
        return trend_df

    mean_events = trend_df["event_count"].mean()
    std_events = trend_df["event_count"].std()

    if std_events > 0:
        trend_df["z_score"] = (trend_df["event_count"] - mean_events) / std_events
    else:
        trend_df["z_score"] = 0.0

    trend_df["is_spike"] = trend_df["z_score"] > z_threshold
    return trend_df

def summarize_trends(df: pd.DataFrame) -> Dict[str, Any]:
    """Provides analytical summary of temporal trends and detected activity spikes."""
    trend = calculate_yearly_trend(df)
    trend = calculate_year_over_year_change(trend)
    trend = detect_activity_spikes(trend)

    peak_year_row = trend.loc[trend["event_count"].idxmax()] if len(trend) > 0 else None
    spikes = trend[trend["is_spike"]]["iyear"].tolist()

    return {
        "peak_year": int(peak_year_row["iyear"]) if peak_year_row is not None else 0,
        "peak_events": int(peak_year_row["event_count"]) if peak_year_row is not None else 0,
        "detected_spike_years": spikes,
        "latest_year": int(trend["iyear"].max()) if len(trend) > 0 else 0,
        "latest_year_events": int(trend.iloc[-1]["event_count"]) if len(trend) > 0 else 0
    }
