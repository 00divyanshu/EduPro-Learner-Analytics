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
    df["CourseCategory"] = df["CourseCategory"].fillna("Unknown").astype(str).str.title()
    df["CourseType"] = df["CourseType"].fillna("Unknown").astype(str).str.title()
    df["LearnerSegment"] = df["AgeGroup"] + " | " + df["Gender"]
    for column in ["Amount", "CoursePrice", "CourseDuration", "CourseRating"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)
        else:
            df[column] = 0
    df["IsPaidEnrollment"] = df["Amount"] > 0
    df["RevenueBand"] = pd.cut(
        df["Amount"],
        bins=[-0.01, 0, 250, 500, float("inf")],
        labels=["Free", "Low Paid", "Mid Paid", "Premium"],
    ).astype(str)
    df["DurationBand"] = pd.cut(
        df["CourseDuration"],
        bins=[-0.01, 15, 30, 45, float("inf")],
        labels=["Short", "Medium", "Long", "Extended"],
    ).astype(str)
    df["RatingBand"] = pd.cut(
        df["CourseRating"],
        bins=[-0.01, 2.5, 3.5, 4.25, 5],
        labels=["Low Rated", "Developing", "Strong", "Excellent"],
    ).astype(str)
    return df


def build_learner_summary(master_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate behavior at learner level."""
    summary = (
        master_df.groupby(["UserID", "UserName", "AgeGroup", "Gender"], dropna=False)
        .agg(
            TotalEnrollments=("TransactionID", "nunique"),
            UniqueCategories=("CourseCategory", "nunique"),
            PaidEnrollments=("IsPaidEnrollment", "sum"),
            TotalSpend=("Amount", "sum"),
            FirstEnrollment=("TransactionDate", "min"),
            LastEnrollment=("TransactionDate", "max"),
        )
        .reset_index()
    )

    summary["LearningSpanDays"] = (
        summary["LastEnrollment"] - summary["FirstEnrollment"]
    ).dt.days.clip(lower=0)
    summary["EngagementTier"] = pd.cut(
        summary["TotalEnrollments"],
        bins=[0, 1, 3, 6, float("inf")],
        labels=["One-time", "Exploring", "Committed", "Power Learner"],
        include_lowest=True,
    ).astype(str)

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
            Revenue=("Amount", "sum"),
            AverageRating=("CourseRating", "mean"),
            AverageDuration=("CourseDuration", "mean"),
        )
        .reset_index()
        .sort_values("EnrollmentCount", ascending=False)
    )
