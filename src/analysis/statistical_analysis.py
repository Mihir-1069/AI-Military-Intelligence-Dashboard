from typing import Dict,Any
import pandas as pd
import numpy as np


def calculate_yearly_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates aggregate event counts per year."""
    if "iyear" not in df.columns:
        return pd.DataFrame()
    yearly = df.groupby("iyear").size().reset_index(name="event_count")
    return yearly.sort_values("iyear")


def calculate_country_distribution(df: pd.DataFrame,top_n: int = 15) -> pd.DataFrame:
    """Calculates top countries by total events and casualties."""
    country_col = "country_txt" if "country_txt" in df.columns else "country"
    if country_col not in df.columns:
        return pd.DataFrame()

    agg_dict = {"eventid": "count"}
    if "nkill" in df.columns:
        agg_dict["nkill"] = "sum"
    if "nwound" in df.columns:
        agg_dict["nwound"] = "sum"

    country_df = df.groupby(country_col).agg(agg_dict).reset_index()
    country_df.rename(columns={"eventid": "event_count","nkill": "total_killed","nwound": "total_wounded"},inplace=True)

    if "total_killed" in country_df.columns and "total_wounded" in country_df.columns:
        country_df["total_casualties"] = country_df["total_killed"] + country_df["total_wounded"]

    return country_df.sort_values(by="event_count",ascending=False).head(top_n)


def calculate_region_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates aggregate regional distribution of events and casualties."""
    region_col = "region_txt" if "region_txt" in df.columns else "region"
    if region_col not in df.columns:
        return pd.DataFrame()

    agg_dict = {"eventid": "count"}
    if "nkill" in df.columns:
        agg_dict["nkill"] = "sum"
    if "nwound" in df.columns:
        agg_dict["nwound"] = "sum"

    region_df = df.groupby(region_col).agg(agg_dict).reset_index()
    region_df.rename(columns={"eventid": "event_count","nkill": "total_killed","nwound": "total_wounded"},inplace=True)

    if "total_killed" in region_df.columns and "total_wounded" in region_df.columns:
        region_df["total_casualties"] = region_df["total_killed"] + region_df["total_wounded"]

    return region_df.sort_values(by="event_count",ascending=False)


def calculate_attack_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates distribution across attack types."""
    attack_col = "attacktype1_txt" if "attacktype1_txt" in df.columns else "attacktype1"
    if attack_col not in df.columns:
        return pd.DataFrame()

    attack_df = df.groupby(attack_col).agg(
        event_count=("eventid","count"),
        total_killed=("nkill","sum") if "nkill" in df.columns else ("eventid","count"),
        total_wounded=("nwound","sum") if "nwound" in df.columns else ("eventid","count")
    ).reset_index()
    return attack_df.sort_values(by="event_count",ascending=False)


def calculate_target_type_distribution(df: pd.DataFrame,top_n: int = 10) -> pd.DataFrame:
    """Calculates distribution across target types."""
    targ_col = "targtype1_txt" if "targtype1_txt" in df.columns else "targtype1"
    if targ_col not in df.columns:
        return pd.DataFrame()

    targ_df = df.groupby(targ_col).size().reset_index(name="event_count")
    return targ_df.sort_values(by="event_count",ascending=False).head(top_n)


def calculate_casualty_statistics(df: pd.DataFrame) -> Dict[str,float]:
    """Calculates descriptive casualty statistics."""
    nkill = df["nkill"].fillna(0) if "nkill" in df.columns else pd.Series([0])
    nwound = df["nwound"].fillna(0) if "nwound" in df.columns else pd.Series([0])
    total_cas = nkill + nwound

    return {
        "total_killed": float(nkill.sum()),
        "total_wounded": float(nwound.sum()),
        "total_casualties": float(total_cas.sum()),
        "mean_killed_per_event": float(round(nkill.mean(),2)),
        "mean_wounded_per_event": float(round(nwound.mean(),2)),
        "max_killed_single_event": float(nkill.max()),
        "max_wounded_single_event": float(nwound.max())
    }


def generate_dataset_summary(df: pd.DataFrame) -> Dict[str,Any]:
    """Generates overall aggregate historical dataset summary statistics."""
    years = df["iyear"].dropna().astype(int) if "iyear" in df.columns else pd.Series([])
    countries = df["country_txt"].nunique() if "country_txt" in df.columns else 0
    regions = df["region_txt"].nunique() if "region_txt" in df.columns else 0
    cas_stats = calculate_casualty_statistics(df)

    return {
        "total_events": len(df),
        "start_year": int(years.min()) if len(years) > 0 else 0,
        "end_year": int(years.max()) if len(years) > 0 else 0,
        "unique_countries": countries,
        "unique_regions": regions,
        "casualty_statistics": cas_stats
    }
