"""Reusable Plotly chart builders."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


COLOR_SEQUENCE = ["#2563EB", "#14B8A6", "#F97316", "#E11D48", "#7C3AED", "#84CC16", "#0F766E"]


def _polish(fig: go.Figure, height: int = 360) -> go.Figure:
    """Apply a consistent dashboard style to Plotly figures."""
    fig.update_layout(
        height=height,
        template="plotly_white",
        margin={"l": 24, "r": 24, "t": 62, "b": 28},
        font={"family": "Inter, Segoe UI, Arial", "size": 13, "color": "#1F2937"},
        title={"font": {"size": 18, "color": "#111827"}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
    )
    return fig


def empty_figure(message: str = "No data available") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, x=0.5, y=0.5, font={"size": 16})
    fig.update_layout(height=320, xaxis={"visible": False}, yaxis={"visible": False})
    return _polish(fig, height=320)


def bar_count(df: pd.DataFrame, column: str, title: str) -> go.Figure:
    if df.empty or column not in df:
        return empty_figure()

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Enrollments"]
    fig = px.bar(
        counts,
        x=column,
        y="Enrollments",
        title=title,
        color=column,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Enrollments")
    return _polish(fig)


def grouped_bar(df: pd.DataFrame, x: str, color: str, title: str) -> go.Figure:
    if df.empty or x not in df or color not in df:
        return empty_figure()

    grouped = df.groupby([x, color])["TransactionID"].nunique().reset_index(name="Enrollments")
    fig = px.bar(
        grouped,
        x=x,
        y="Enrollments",
        color=color,
        barmode="group",
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(xaxis_title="", yaxis_title="Enrollments")
    return _polish(fig)


def enrollment_trend(df: pd.DataFrame) -> go.Figure:
    if df.empty or "EnrollmentMonth" not in df:
        return empty_figure()

    trend = df.groupby("EnrollmentMonth")["TransactionID"].nunique().reset_index(name="Enrollments")
    fig = px.line(
        trend,
        x="EnrollmentMonth",
        y="Enrollments",
        markers=True,
        title="Monthly Enrollment Trend",
    )
    fig.update_traces(line_color="#2563EB", marker_color="#14B8A6", line_width=3)
    fig.update_layout(xaxis_title="", yaxis_title="Enrollments")
    return _polish(fig)


def donut_chart(df: pd.DataFrame, column: str, title: str) -> go.Figure:
    if df.empty or column not in df:
        return empty_figure()

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Enrollments"]
    fig = px.pie(
        counts,
        names=column,
        values="Enrollments",
        hole=0.48,
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    return _polish(fig)


def top_courses(df: pd.DataFrame, limit: int = 10) -> go.Figure:
    """Show the most enrolled courses."""
    if df.empty or "CourseName" not in df:
        return empty_figure()

    courses = (
        df.groupby("CourseName")["TransactionID"]
        .nunique()
        .sort_values(ascending=False)
        .head(limit)
        .reset_index(name="Enrollments")
    )
    fig = px.bar(
        courses.sort_values("Enrollments"),
        x="Enrollments",
        y="CourseName",
        orientation="h",
        title=f"Top {limit} Courses by Enrollment",
        color="Enrollments",
        color_continuous_scale=["#DBEAFE", "#2563EB"],
    )
    fig.update_layout(xaxis_title="Enrollments", yaxis_title="", coloraxis_showscale=False)
    return _polish(fig, height=430)


def category_level_heatmap(df: pd.DataFrame) -> go.Figure:
    """Show category demand by course level."""
    if df.empty or not {"CourseCategory", "CourseLevel", "TransactionID"}.issubset(df.columns):
        return empty_figure()

    matrix = (
        df.groupby(["CourseCategory", "CourseLevel"])["TransactionID"]
        .nunique()
        .reset_index(name="Enrollments")
    )
    fig = px.density_heatmap(
        matrix,
        x="CourseLevel",
        y="CourseCategory",
        z="Enrollments",
        title="Course Category and Level Demand Map",
        color_continuous_scale=["#ECFEFF", "#14B8A6", "#0F766E"],
    )
    fig.update_layout(xaxis_title="", yaxis_title="", coloraxis_colorbar_title="Enrollments")
    return _polish(fig, height=470)


def revenue_by_category(df: pd.DataFrame) -> go.Figure:
    """Show revenue by course category."""
    if df.empty or not {"CourseCategory", "Amount"}.issubset(df.columns):
        return empty_figure()

    revenue = (
        df.groupby("CourseCategory")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index(name="Revenue")
    )
    fig = px.bar(
        revenue,
        x="CourseCategory",
        y="Revenue",
        title="Revenue by Course Category",
        color="CourseCategory",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue")
    return _polish(fig)
