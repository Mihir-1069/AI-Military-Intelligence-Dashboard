import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DARK_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 23, 42, 0.6)",
    font=dict(family="Inter, sans-serif", color="#e2e8f0", size=12),
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(gridcolor="#1e293b", zerolinecolor="#334155"),
    yaxis=dict(gridcolor="#1e293b", zerolinecolor="#334155")
)

def create_timeline_chart(trend_df: pd.DataFrame, title: str = "Event Activity Over Time") -> go.Figure:
    """Creates a high-contrast dark timeline trend chart with range selector slider."""
    if trend_df.empty or "iyear" not in trend_df.columns:
        return go.Figure()

    fig = px.line(
        trend_df, x="iyear", y="event_count",
        title=title,
        labels={"iyear": "Year", "event_count": "Total Events"},
        markers=True,
        color_discrete_sequence=["#38bdf8"]
    )
    
    if "total_casualties" in trend_df.columns:
        fig.add_trace(go.Scatter(
            x=trend_df["iyear"], y=trend_df["total_casualties"],
            mode="lines+markers", name="Total Casualties",
            line=dict(color="#ef4444", width=2, dash="dash")
        ))

    fig.update_layout(**DARK_LAYOUT)
    fig.update_xaxes(rangeslider_visible=True)
    return fig

def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str, color_hex: str = "#3b82f6", orientation: str = "h") -> go.Figure:
    """Creates a standardized horizontal/vertical Plotly bar chart."""
    if df.empty:
        return go.Figure()

    fig = px.bar(
        df, x=x_col, y=y_col,
        orientation=orientation,
        title=title,
        color_discrete_sequence=[color_hex]
    )
    fig.update_layout(**DARK_LAYOUT)
    if orientation == "h":
        fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig

def create_multi_region_line_chart(df: pd.DataFrame, regions: list, title: str = "Regional Comparison Over Time") -> go.Figure:
    """Creates a multi-line temporal trend chart comparing selected regions."""
    if df.empty or "iyear" not in df.columns or "region_txt" not in df.columns:
        return go.Figure()

    filtered = df[df["region_txt"].isin(regions)]
    regional_trend = filtered.groupby(["iyear", "region_txt"]).size().reset_index(name="event_count")

    fig = px.line(
        regional_trend, x="iyear", y="event_count", color="region_txt",
        title=title,
        labels={"iyear": "Year", "event_count": "Total Events", "region_txt": "Region"},
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig.update_layout(**DARK_LAYOUT)
    return fig

def create_density_map(df: pd.DataFrame, max_points: int = 5000) -> go.Figure:
    """Creates an aggregate density heat map using Plotly scatter mapbox / density mapbox."""
    if df.empty or "latitude" not in df.columns or "longitude" not in df.columns:
        return go.Figure()

    valid = df.dropna(subset=["latitude", "longitude"]).copy()
    if len(valid) > max_points:
        valid = valid.sample(n=max_points, random_state=42)

    fig = px.density_mapbox(
        valid, lat="latitude", lon="longitude",
        z="nkill" if "nkill" in valid.columns else None,
        radius=8,
        center=dict(lat=20, lon=0),
        zoom=1,
        mapbox_style="carto-darkmatter",
        title=f"Aggregate Historical Density Hotspots (Sampled {len(valid):,} Events)"
    )
    fig.update_layout(**DARK_LAYOUT)
    return fig
