"""Feature engineering for learner behavior analytics."""

from __future__ import annotations

import pandas as pd


def assign_age_group(age: float | int | None) -> str:
    """Convert age into learner-friendly demographic bands."""
    if pd.isna(age):
        return "Unknown"
    if age <= 19:
        return "Teen"
    if age <= 29:
        return "Young Adult"
    if age <= 44:
        return "Adult"
    if age <= 59:
        return "Mid-Career Learner"
    return "Senior Learner"


def create_features(master_df: pd.DataFrame) -> pd.DataFrame:
    """Create analysis-ready features from the merged dataset."""
    df = master_df.copy()
    df["AgeGroup"] = df["Age"].apply(assign_age_group)
    df["EnrollmentYear"] = df["TransactionDate"].dt.year
    df["EnrollmentMonth"] = df["TransactionDate"].dt.to_period("M").astype(str)
    df["EnrollmentMonthName"] = df["TransactionDate"].dt.month_name()
    df["EnrollmentWeekday"] = df["TransactionDate"].dt.day_name()
    df["EnrollmentQuarter"] = df["TransactionDate"].dt.to_period("Q").astype(str)
    df["CourseLevel"] = df["CourseLevel"].fillna("Unknown").astype(str).str.title()
    df["LearnerSegment"] = df["AgeGroup"] + " | " + df["Gender"]
    return df


def build_learner_summary(master_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate behavior at learner level."""
    summary = (
        master_df.groupby(["UserID", "UserName", "AgeGroup", "Gender"], dropna=False)
        .agg(
            TotalEnrollments=("TransactionID", "nunique"),
            UniqueCategories=("CourseCategory", "nunique"),
            FirstEnrollment=("TransactionDate", "min"),
            LastEnrollment=("TransactionDate", "max"),
        )
        .reset_index()
    )

    preferred_level = (
        master_df.groupby(["UserID", "CourseLevel"])
        .size()
        .reset_index(name="Enrollments")
        .sort_values(["UserID", "Enrollments"], ascending=[True, False])
        .drop_duplicates("UserID")
        .rename(columns={"CourseLevel": "PreferredCourseLevel"})
    )

    return summary.merge(preferred_level[["UserID", "PreferredCourseLevel"]], on="UserID", how="left")


def build_course_summary(master_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate behavior at course level."""
    return (
        master_df.groupby(["CourseID", "CourseName", "CourseCategory", "CourseType", "CourseLevel"])
        .agg(
            EnrollmentCount=("TransactionID", "nunique"),
            UniqueLearners=("UserID", "nunique"),
        )
        .reset_index()
        .sort_values("EnrollmentCount", ascending=False)
    )

