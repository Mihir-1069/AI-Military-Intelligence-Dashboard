import sys
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

def plot_event_map(df: pd.DataFrame, max_points: int = 5000):
    """Plots interactive geographic scatter map of historical events."""
    if df.empty or "latitude" not in df.columns or "longitude" not in df.columns:
        return None

    valid_coords = df.dropna(subset=["latitude", "longitude"]).copy()
    if len(valid_coords) > max_points:
        valid_coords = valid_coords.sample(n=max_points, random_state=42)

    country_col = "country_txt" if "country_txt" in valid_coords.columns else "country"
    attack_col = "attacktype1_txt" if "attacktype1_txt" in valid_coords.columns else "attacktype"

    fig = px.scatter_geo(
        valid_coords,
        lat="latitude",
        lon="longitude",
        color=attack_col if attack_col in valid_coords.columns else None,
        hover_name=country_col if country_col in valid_coords.columns else None,
        hover_data=["iyear", "nkill", "nwound"] if "nkill" in valid_coords.columns else None,
        title=f"Historical Aggregate Event Map (Sampled {len(valid_coords):,} Events)",
        opacity=0.6,
        projection="natural earth"
    )
    fig.update_layout(template="plotly_dark", legend_title="Attack Type")
    return fig

def plot_regional_activity_map(df: pd.DataFrame):
    """Plots aggregate country-level choropleth event density map."""
    country_col = "country_txt" if "country_txt" in df.columns else "country"
    if df.empty or country_col not in df.columns:
        return None

    country_counts = df.groupby(country_col).size().reset_index(name="event_count")

    fig = px.choropleth(
        country_counts,
        locations=country_col,
        locationmode="country names",
        color="event_count",
        hover_name=country_col,
        color_continuous_scale="Reds",
        title="Aggregate Regional Activity Density (Choropleth Heatmap)",
        labels={"event_count": "Total Events"}
    )
    fig.update_layout(template="plotly_dark")
    return fig

def plot_aggregate_hotspots(df: pd.DataFrame):
    """Plots density heatmap of regional threat hotspots with multi-version fallback."""
    if df.empty or "latitude" not in df.columns or "longitude" not in df.columns:
        return None

    valid_coords = df.dropna(subset=["latitude", "longitude"]).copy()
    if len(valid_coords) > 10000:
        valid_coords = valid_coords.sample(n=10000, random_state=42)

    try:
        if hasattr(px, "density_map"):
            fig = px.density_map(
                valid_coords,
                lat="latitude",
                lon="longitude",
                z="nkill" if "nkill" in valid_coords.columns else None,
                radius=10,
                center=dict(lat=20, lon=0),
                zoom=1,
                map_style="carto-darkmatter",
                title="Aggregate Historical Fatalities Density Hotspots"
            )
        elif hasattr(px, "density_mapbox"):
            fig = px.density_mapbox(
                valid_coords,
                lat="latitude",
                lon="longitude",
                z="nkill" if "nkill" in valid_coords.columns else None,
                radius=10,
                center=dict(lat=20, lon=0),
                zoom=1,
                mapbox_style="carto-darkmatter",
                title="Aggregate Historical Fatalities Density Hotspots"
            )
        else:
            fig = plot_event_map(valid_coords)
            return fig
    except Exception:
        fig = plot_event_map(valid_coords)
        return fig

    fig.update_layout(template="plotly_dark")
    return fig
