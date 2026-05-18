"""KPI calculations for EduPro analytics."""

from __future__ import annotations

import pandas as pd


def _top_value(df: pd.DataFrame, column: str, fallback: str = "Not available") -> str:
    if df.empty or column not in df:
        return fallback
    counts = df[column].dropna().value_counts()
    return str(counts.index[0]) if not counts.empty else fallback


def calculate_kpis(master_df: pd.DataFrame) -> dict[str, object]:
    """Calculate dashboard-level business KPIs."""
    beginner_count = int((master_df["CourseLevel"].str.lower() == "beginner").sum()) if not master_df.empty else 0
    advanced_count = int((master_df["CourseLevel"].str.lower() == "advanced").sum()) if not master_df.empty else 0

    return {
        "total_learners": int(master_df["UserID"].nunique()) if not master_df.empty else 0,
        "total_courses": int(master_df["CourseID"].nunique()) if not master_df.empty else 0,
        "total_enrollments": int(master_df["TransactionID"].nunique()) if not master_df.empty else 0,
        "most_popular_category": _top_value(master_df, "CourseCategory"),
        "most_active_age_group": _top_value(master_df, "AgeGroup"),
        "beginner_enrollments": beginner_count,
        "advanced_enrollments": advanced_count,
        "beginner_to_advanced_ratio": round(beginner_count / advanced_count, 2) if advanced_count else None,
    }

