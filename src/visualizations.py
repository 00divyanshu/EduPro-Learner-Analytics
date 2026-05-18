"""Reusable Plotly chart builders."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


COLOR_SEQUENCE = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#7C3AED", "#0F766E"]


def empty_figure(message: str = "No data available") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, x=0.5, y=0.5, font={"size": 16})
    fig.update_layout(height=320, xaxis={"visible": False}, yaxis={"visible": False})
    return fig


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
    return fig


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
    return fig


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
    fig.update_traces(line_color="#2563EB", marker_color="#10B981")
    fig.update_layout(xaxis_title="", yaxis_title="Enrollments")
    return fig


def donut_chart(df: pd.DataFrame, column: str, title: str) -> go.Figure:
    if df.empty or column not in df:
        return empty_figure()

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Enrollments"]
    return px.pie(
        counts,
        names=column,
        values="Enrollments",
        hole=0.48,
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
    )

