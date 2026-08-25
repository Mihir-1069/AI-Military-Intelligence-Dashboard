import sys
from pathlib import Path
from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gg
import matplotlib.pyplot as plt
import seaborn as sns

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.helper import save_figure

def plot_yearly_trend(trend_df: pd.DataFrame, use_plotly: bool = True):
    """Plots temporal event & casualty trends."""
    if trend_df.empty or "iyear" not in trend_df.columns:
        return None

    if use_plotly:
        fig = px.line(
            trend_df, x="iyear", y=["event_count", "total_casualties"],
            title="Historical Event & Casualty Trends (1970 - Present)",
            labels={"iyear": "Year", "value": "Count", "variable": "Metric"},
            markers=True,
            color_discrete_map={"event_count": "#1f77b4", "total_casualties": "#d62728"}
        )
        fig.update_layout(template="plotly_dark", hovermode="x unified", legend_title="")
        return fig

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    
    ax1.plot(trend_df["iyear"], trend_df["event_count"], color="navy", label="Event Count", linewidth=2)
    if "total_casualties" in trend_df.columns:
        ax2.plot(trend_df["iyear"], trend_df["total_casualties"], color="crimson", label="Total Casualties", linestyle="--", linewidth=2)
        ax2.set_ylabel("Casualties", color="crimson")
    
    ax1.set_title("Historical Terrorism Event & Casualty Trends", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Events", color="navy")
    ax1.grid(True, linestyle=":", alpha=0.6)
    
    save_figure(fig, "yearly_trend.png")
    return fig

def plot_country_distribution(country_df: pd.DataFrame, use_plotly: bool = True):
    """Plots top countries by event frequency."""
    if country_df.empty:
        return None

    country_col = "country_txt" if "country_txt" in country_df.columns else "country"
    if use_plotly:
        fig = px.bar(
            country_df.head(15), x="event_count", y=country_col,
            orientation="h",
            title="Top 15 High-Activity Countries (Historical Total)",
            labels={"event_count": "Total Events", country_col: "Country"},
            color="event_count", color_continuous_scale="Viridis"
        )
        fig.update_layout(template="plotly_dark", yaxis=dict(autorange="reversed"))
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=country_df.head(15), x="event_count", y=country_col, palette="mako", ax=ax)
    ax.set_title("Top High-Activity Countries", fontsize=12, fontweight="bold")
    ax.set_xlabel("Total Events")
    ax.set_ylabel("Country")
    save_figure(fig, "country_distribution.png")
    return fig

def plot_region_distribution(region_df: pd.DataFrame, use_plotly: bool = True):
    """Plots regional distribution of events."""
    if region_df.empty:
        return None

    region_col = "region_txt" if "region_txt" in region_df.columns else "region"
    if use_plotly:
        fig = px.pie(
            region_df, names=region_col, values="event_count",
            title="Aggregate Regional Distribution of Events",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Dark24
        )
        fig.update_layout(template="plotly_dark")
        return fig

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=region_df, x="event_count", y=region_col, palette="viridis", ax=ax)
    ax.set_title("Regional Activity Breakdown", fontsize=12, fontweight="bold")
    ax.set_xlabel("Events")
    ax.set_ylabel("Region")
    save_figure(fig, "regional_distribution.png")
    return fig

def plot_attack_type_distribution(attack_df: pd.DataFrame, use_plotly: bool = True):
    """Plots distribution across attack tactics/types."""
    if attack_df.empty:
        return None

    attack_col = "attacktype1_txt" if "attacktype1_txt" in attack_df.columns else "attacktype1"
    if use_plotly:
        fig = px.bar(
            attack_df, x="event_count", y=attack_col, orientation="h",
            title="Tactical Breakdown: Distribution by Attack Type",
            labels={"event_count": "Total Events", attack_col: "Attack Type"},
            color="event_count", color_continuous_scale="Teal"
        )
        fig.update_layout(template="plotly_dark", yaxis=dict(autorange="reversed"))
        return fig

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=attack_df, x="event_count", y=attack_col, palette="rocket", ax=ax)
    ax.set_title("Distribution by Attack Type", fontsize=12, fontweight="bold")
    ax.set_xlabel("Total Events")
    ax.set_ylabel("Attack Type")
    save_figure(fig, "attack_type_distribution.png")
    return fig

def plot_casualty_distribution(df: pd.DataFrame, use_plotly: bool = True):
    """Plots casualty distribution analysis."""
    if df.empty or "nkill" not in df.columns:
        return None

    cas_data = df[(df["nkill"] > 0) & (df["nkill"] < 100)]
    if use_plotly:
        fig = px.histogram(
            cas_data, x="nkill", nbins=50,
            title="Casualty Distribution (Killed per Event, <100)",
            labels={"nkill": "Fatalities per Event"},
            color_discrete_sequence=["#e74c3c"]
        )
        fig.update_layout(template="plotly_dark")
        return fig

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(cas_data["nkill"], bins=50, kde=True, color="darkred", ax=ax)
    ax.set_title("Fatalities Distribution per Event (< 100)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Fatalities")
    ax.set_ylabel("Event Count")
    save_figure(fig, "casualty_analysis.png")
    return fig

def plot_model_performance(metrics: dict, use_plotly: bool = True):
    """Plots model evaluation metric performance summary."""
    metric_names = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
    vals = [metrics.get(m, 0.0) for m in metric_names]
    m_df = pd.DataFrame({"Metric": [m.upper() for m in metric_names], "Score": vals})

    if use_plotly:
        fig = px.bar(
            m_df, x="Metric", y="Score", text="Score",
            title="Threat Model Metric Evaluation Performance",
            range_y=[0, 1.05],
            color="Score", color_continuous_scale="Blues"
        )
        fig.update_layout(template="plotly_dark")
        return fig

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=m_df, x="Metric", y="Score", palette="Blues_d", ax=ax)
    ax.set_ylim(0, 1.05)
    ax.set_title("Model Evaluation Metrics", fontsize=12, fontweight="bold")
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.3f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    save_figure(fig, "model_performance.png")
    return fig
