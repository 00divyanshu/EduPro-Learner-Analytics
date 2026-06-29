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
from src.visualizations import (
    bar_count,
    category_level_heatmap,
    donut_chart,
    enrollment_trend,
    grouped_bar,
    revenue_by_category,
    top_courses,
)


st.set_page_config(
    page_title="EduPro Learner Analytics",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #111827;
            --muted: #6b7280;
            --panel: #ffffff;
            --line: #e5e7eb;
            --blue: #2563eb;
            --teal: #14b8a6;
            --coral: #f97316;
        }
        .stApp {
            background:
                linear-gradient(180deg, #f8fafc 0%, #eef6ff 42%, #fff7ed 100%);
        }
        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--line);
        }
        .hero {
            border: 1px solid rgba(37, 99, 235, 0.18);
            border-radius: 18px;
            padding: 28px 30px;
            background:
                linear-gradient(135deg, rgba(37,99,235,0.96), rgba(20,184,166,0.90) 58%, rgba(249,115,22,0.88));
            color: #ffffff;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.16);
            margin-bottom: 18px;
        }
        .hero h1 {
            margin: 0 0 8px 0;
            font-size: clamp(2rem, 4vw, 3.8rem);
            line-height: 1.05;
            letter-spacing: 0;
        }
        .hero p {
            margin: 0;
            max-width: 860px;
            font-size: 1.03rem;
            color: rgba(255,255,255,0.92);
        }
        .metric-card {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: rgba(255,255,255,0.88);
            padding: 16px 18px;
            min-height: 116px;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
        }
        .metric-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .metric-value {
            color: var(--ink);
            font-size: 1.65rem;
            font-weight: 800;
            margin-top: 6px;
            word-break: break-word;
        }
        .metric-note {
            color: var(--muted);
            font-size: 0.84rem;
            margin-top: 4px;
        }
        div[data-testid="stPlotlyChart"] {
            border: 1px solid var(--line);
            border-radius: 16px;
            background: rgba(255,255,255,0.86);
            padding: 8px;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.07);
        }
        .insight-box {
            border-left: 5px solid var(--teal);
            background: rgba(255,255,255,0.88);
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 10px;
            color: var(--ink);
        }
        .small-muted {
            color: var(--muted);
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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

    st.sidebar.title("EduPro Controls")
    st.sidebar.caption("Use filters to explore learner behavior across demographics, course type, and time.")
    genders = multiselect_filter("Gender", filtered, "Gender")
    age_groups = multiselect_filter("Age Group", filtered, "AgeGroup")
    categories = multiselect_filter("Course Category", filtered, "CourseCategory")
    levels = multiselect_filter("Course Level", filtered, "CourseLevel")
    course_types = multiselect_filter("Course Type", filtered, "CourseType")

    min_date = filtered["TransactionDate"].min().date()
    max_date = filtered["TransactionDate"].max().date()
    date_range = st.sidebar.date_input("Enrollment Date Range", value=(min_date, max_date))

    filtered = filtered[
        filtered["Gender"].isin(genders)
        & filtered["AgeGroup"].isin(age_groups)
        & filtered["CourseCategory"].isin(categories)
        & filtered["CourseLevel"].isin(levels)
        & filtered["CourseType"].isin(course_types)
    ]

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["TransactionDate"].dt.date >= start_date)
            & (filtered["TransactionDate"].dt.date <= end_date)
        ]

    return filtered


def metric_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(kpis: dict[str, object]) -> None:
    ratio = kpis["beginner_to_advanced_ratio"] or "N/A"
    cards = st.columns(4)
    with cards[0]:
        metric_card("Learners", f"{kpis['total_learners']:,}", "unique enrolled users")
    with cards[1]:
        metric_card("Enrollments", f"{kpis['total_enrollments']:,}", "transactions analyzed")
    with cards[2]:
        metric_card("Revenue", f"${kpis['total_revenue']:,.0f}", "paid enrollment amount")
    with cards[3]:
        metric_card("Paid Rate", f"{kpis['paid_enrollment_rate']}%", "share of paid enrollments")

    cards = st.columns(4)
    with cards[0]:
        metric_card("Top Category", str(kpis["most_popular_category"]), "highest enrollment share")
    with cards[1]:
        metric_card("Active Age Group", str(kpis["most_active_age_group"]), "most engaged segment")
    with cards[2]:
        metric_card("Avg Rating", f"{kpis['avg_course_rating']:.2f}", "course rating average")
    with cards[3]:
        metric_card("Beginner:Advanced", str(ratio), "level mix indicator")


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
            <h1>EduPro Learner Analytics</h1>
            <p>
                A deployment-ready learner intelligence dashboard for understanding who enrolls,
                what they choose, how course demand changes, and where EduPro can improve planning,
                engagement, and inclusivity.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


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
    inject_css()
    try:
        master_df = load_master_data()
    except Exception as exc:
        render_empty_state(exc)
        return

    render_hero()

    filtered_df = apply_filters(master_df)
    kpis = calculate_kpis(filtered_df)
    render_kpis(kpis)

    if filtered_df.empty:
        st.warning("No records match the current filters. Expand the filters to bring the dashboard back to life.")
        return

    overview_tab, demographic_tab, behavior_tab, revenue_tab, data_tab = st.tabs(
        ["Executive View", "Demographics", "Behavior", "Revenue", "Data Preview"]
    )

    with overview_tab:
        left, right = st.columns([1.15, 0.85])
        with left:
            st.plotly_chart(enrollment_trend(filtered_df), width="stretch")
            st.plotly_chart(top_courses(filtered_df), width="stretch")
        with right:
            st.plotly_chart(donut_chart(filtered_df, "CourseCategory", "Course Category Share"), width="stretch")

            st.subheader("Business Insights")
            for insight in generate_business_insights(filtered_df):
                st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

    with demographic_tab:
        left, right = st.columns(2)
        with left:
            st.plotly_chart(bar_count(filtered_df, "AgeGroup", "Enrollments by Age Group"), width="stretch")
            st.plotly_chart(grouped_bar(filtered_df, "Gender", "CourseType", "Course Type Preference by Gender"), width="stretch")
        with right:
            st.plotly_chart(grouped_bar(filtered_df, "CourseLevel", "Gender", "Course Level Preference by Gender"), width="stretch")
            st.plotly_chart(donut_chart(filtered_df, "Gender", "Gender Enrollment Share"), width="stretch")

    with behavior_tab:
        left, right = st.columns(2)
        with left:
            st.plotly_chart(grouped_bar(filtered_df, "AgeGroup", "CourseLevel", "Course Level by Age Group"), width="stretch")
            st.plotly_chart(bar_count(filtered_df, "DurationBand", "Course Duration Preference"), width="stretch")
        with right:
            st.plotly_chart(category_level_heatmap(filtered_df), width="stretch")
            st.plotly_chart(bar_count(filtered_df, "RatingBand", "Course Rating Mix"), width="stretch")

    with revenue_tab:
        left, right = st.columns(2)
        with left:
            st.plotly_chart(revenue_by_category(filtered_df), width="stretch")
            st.plotly_chart(bar_count(filtered_df, "RevenueBand", "Enrollment Revenue Band"), width="stretch")
        with right:
            st.subheader("Recommendations")
            for recommendation in generate_recommendations(filtered_df):
                st.markdown(f'<div class="insight-box">{recommendation}</div>', unsafe_allow_html=True)
            revenue_table = (
                filtered_df.groupby(["CourseCategory", "CourseType"], as_index=False)
                .agg(Enrollments=("TransactionID", "nunique"), Revenue=("Amount", "sum"))
                .sort_values(["Revenue", "Enrollments"], ascending=False)
            )
            st.dataframe(revenue_table, width="stretch", hide_index=True)

    with data_tab:
        st.markdown('<p class="small-muted">Filtered master table for validation, exploration, and interview walkthroughs.</p>', unsafe_allow_html=True)
        st.dataframe(filtered_df, width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
