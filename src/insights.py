"""Business insight generation for the EduPro dashboard and reports."""

from __future__ import annotations

import pandas as pd


def _safe_top_label(df: pd.DataFrame, column: str) -> str | None:
    if df.empty or column not in df:
        return None
    values = df[column].dropna().value_counts()
    return str(values.index[0]) if not values.empty else None


def generate_business_insights(master_df: pd.DataFrame) -> list[str]:
    """Generate plain-English insights from the filtered analytics dataset."""
    if master_df.empty:
        return ["No records are available for the selected filters."]

    insights: list[str] = []
    top_age = _safe_top_label(master_df, "AgeGroup")
    top_category = _safe_top_label(master_df, "CourseCategory")
    top_level = _safe_top_label(master_df, "CourseLevel")
    top_gender = _safe_top_label(master_df, "Gender")

    if top_age:
        insights.append(f"{top_age} learners are the most active demographic segment in the selected data.")
    if top_category:
        insights.append(f"{top_category} is the strongest course category by enrollment volume.")
    if top_level:
        insights.append(f"{top_level} courses show the highest learner preference in this view.")
    if top_gender:
        insights.append(f"{top_gender} learners represent the largest share of enrollments for the current filters.")

    monthly = master_df.groupby("EnrollmentMonth")["TransactionID"].nunique()
    if len(monthly) > 1:
        peak_month = monthly.idxmax()
        insights.append(f"Enrollment activity peaks in {peak_month}, which can guide campaign timing.")

    if "Amount" in master_df:
        revenue_by_category = master_df.groupby("CourseCategory")["Amount"].sum().sort_values(ascending=False)
        if not revenue_by_category.empty and revenue_by_category.iloc[0] > 0:
            insights.append(
                f"{revenue_by_category.index[0]} contributes the highest revenue in the selected view."
            )

    return insights


def generate_recommendations(master_df: pd.DataFrame) -> list[str]:
    """Generate decision-oriented recommendations."""
    if master_df.empty:
        return ["Upload or select valid EduPro datasets to generate recommendations."]

    recommendations = [
        "Prioritize course planning around high-enrollment categories while monitoring underrepresented categories for growth potential.",
        "Use age-group and course-level patterns to personalize learner communication and onboarding journeys.",
        "Track beginner-to-advanced movement over time to understand whether learners are progressing across difficulty levels.",
    ]

    if "Gender" in master_df:
        gender_counts = master_df["Gender"].value_counts(normalize=True)
        if not gender_counts.empty and gender_counts.max() > 0.65:
            recommendations.append(
                "Investigate inclusivity opportunities because one gender group dominates the current enrollment mix."
            )

    if "IsPaidEnrollment" in master_df:
        paid_rate = master_df["IsPaidEnrollment"].mean()
        if paid_rate < 0.4:
            recommendations.append(
                "Use free courses as acquisition paths and add clear progression routes toward paid intermediate or advanced courses."
            )

    return recommendations
