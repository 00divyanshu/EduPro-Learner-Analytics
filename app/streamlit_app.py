"""Streamlit dashboard for EduPro learner analytics."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_ingestion import DataLoadingError, load_config
from src.eda import run_pipeline
from src.insights import generate_business_insights, generate_recommendations
from src.kpi_metrics import calculate_kpis
from src.visualizations import bar_count, donut_chart, enrollment_trend, grouped_bar


st.set_page_config(page_title="EduPro Learner Analytics", page_icon="bar_chart", layout="wide")


@st.cache_data(show_spinner=False)
def load_master_data() -> pd.DataFrame:
    config = load_config(ROOT_DIR / "config" / "config.yaml")
    outputs = run_pipeline(config, save_outputs=True)
    return outputs["master"]


def multiselect_filter(label: str, df: pd.DataFrame, column: str) -> list[str]:
    values = sorted(df[column].dropna().astype(str).unique().tolist())
    return st.sidebar.multiselect(label, values, default=values)


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()

    st.sidebar.header("Filters")
    genders = multiselect_filter("Gender", filtered, "Gender")
    age_groups = multiselect_filter("Age Group", filtered, "AgeGroup")
    categories = multiselect_filter("Course Category", filtered, "CourseCategory")
    levels = multiselect_filter("Course Level", filtered, "CourseLevel")

    min_date = filtered["TransactionDate"].min().date()
    max_date = filtered["TransactionDate"].max().date()
    date_range = st.sidebar.date_input("Enrollment Date Range", value=(min_date, max_date))

    filtered = filtered[
        filtered["Gender"].isin(genders)
        & filtered["AgeGroup"].isin(age_groups)
        & filtered["CourseCategory"].isin(categories)
        & filtered["CourseLevel"].isin(levels)
    ]

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["TransactionDate"].dt.date >= start_date)
            & (filtered["TransactionDate"].dt.date <= end_date)
        ]

    return filtered


def render_kpis(kpis: dict[str, object]) -> None:
    cards = st.columns(4)
    cards[0].metric("Total Learners", f"{kpis['total_learners']:,}")
    cards[1].metric("Total Courses", f"{kpis['total_courses']:,}")
    cards[2].metric("Total Enrollments", f"{kpis['total_enrollments']:,}")
    cards[3].metric("Top Category", str(kpis["most_popular_category"]))

    cards = st.columns(4)
    cards[0].metric("Most Active Age Group", str(kpis["most_active_age_group"]))
    cards[1].metric("Beginner Enrollments", f"{kpis['beginner_enrollments']:,}")
    cards[2].metric("Advanced Enrollments", f"{kpis['advanced_enrollments']:,}")
    ratio = kpis["beginner_to_advanced_ratio"] or "N/A"
    cards[3].metric("Beginner:Advanced Ratio", ratio)


def render_empty_state(error: Exception) -> None:
    st.title("EduPro Learner Analytics")
    st.info(
        "Add your Google Drive-exported datasets to data/raw as users.csv, courses.csv, "
        "and transactions.csv, then rerun the app."
    )
    st.code(
        "data/raw/users.csv\n"
        "data/raw/courses.csv\n"
        "data/raw/transactions.csv",
        language="text",
    )
    st.caption(f"Current loading message: {error}")


def main() -> None:
    try:
        master_df = load_master_data()
    except Exception as exc:
        render_empty_state(exc)
        return

    st.title("EduPro Learner Demographics and Enrollment Analytics")
    st.caption("A descriptive learner intelligence dashboard for course planning and engagement strategy.")

    filtered_df = apply_filters(master_df)
    kpis = calculate_kpis(filtered_df)
    render_kpis(kpis)

    st.divider()

    left, right = st.columns(2)
    with left:
        st.plotly_chart(bar_count(filtered_df, "AgeGroup", "Enrollments by Age Group"), use_container_width=True)
        st.plotly_chart(grouped_bar(filtered_df, "CourseLevel", "Gender", "Course Level Preference by Gender"), use_container_width=True)
    with right:
        st.plotly_chart(donut_chart(filtered_df, "CourseCategory", "Course Category Share"), use_container_width=True)
        st.plotly_chart(enrollment_trend(filtered_df), use_container_width=True)

    st.subheader("Behavioral Analytics")
    left, right = st.columns(2)
    with left:
        st.plotly_chart(grouped_bar(filtered_df, "AgeGroup", "CourseLevel", "Course Level by Age Group"), use_container_width=True)
    with right:
        st.plotly_chart(bar_count(filtered_df, "CourseType", "Course Type Preference"), use_container_width=True)

    st.subheader("Business Insights")
    for insight in generate_business_insights(filtered_df):
        st.write(f"- {insight}")

    st.subheader("Recommendations")
    for recommendation in generate_recommendations(filtered_df):
        st.write(f"- {recommendation}")

    with st.expander("Preview Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)


if __name__ == "__main__":
    main()
