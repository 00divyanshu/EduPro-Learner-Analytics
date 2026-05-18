"""Data cleaning functions for EduPro source datasets."""

from __future__ import annotations

import re

import pandas as pd

from src.exception import DataValidationError


REQUIRED_USERS_COLUMNS = {"UserID", "UserName", "Age", "Gender"}
REQUIRED_COURSES_COLUMNS = {"CourseID", "CourseName", "CourseCategory", "CourseType", "CourseLevel"}
REQUIRED_TRANSACTIONS_COLUMNS = {"TransactionID", "UserID", "CourseID", "TransactionDate"}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {
        column: re.sub(r"\s+", "", str(column).strip())
        for column in df.columns
    }
    return df.rename(columns=renamed)


def _validate_columns(df: pd.DataFrame, required_columns: set[str], dataset_name: str) -> None:
    missing = required_columns.difference(df.columns)
    if missing:
        raise DataValidationError(f"{dataset_name} is missing required columns: {sorted(missing)}")


def _clean_text(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)


def clean_gender(value: object) -> str:
    """Standardize common gender labels while preserving inclusive labels."""
    if pd.isna(value):
        return "Unknown"

    normalized = str(value).strip().lower()
    mapping = {
        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female",
        "nonbinary": "Non-binary",
        "non-binary": "Non-binary",
        "nb": "Non-binary",
        "other": "Other",
        "prefer not to say": "Prefer not to say",
    }
    return mapping.get(normalized, str(value).strip().title() or "Unknown")


def clean_users(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the users dataset."""
    users = _normalize_columns(df.copy())
    _validate_columns(users, REQUIRED_USERS_COLUMNS, "Users dataset")

    users = users.drop_duplicates(subset=["UserID"]).copy()
    users["UserID"] = _clean_text(users["UserID"])
    users["UserName"] = _clean_text(users["UserName"]).fillna("Unknown Learner")
    users["Age"] = pd.to_numeric(users["Age"], errors="coerce")
    users.loc[(users["Age"] < 5) | (users["Age"] > 100), "Age"] = pd.NA
    users["Gender"] = users["Gender"].apply(clean_gender)

    return users.dropna(subset=["UserID"]).reset_index(drop=True)


def clean_courses(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the courses dataset."""
    courses = _normalize_columns(df.copy())
    _validate_columns(courses, REQUIRED_COURSES_COLUMNS, "Courses dataset")

    courses = courses.drop_duplicates(subset=["CourseID"]).copy()
    courses["CourseID"] = _clean_text(courses["CourseID"])
    for column in ["CourseName", "CourseCategory", "CourseType", "CourseLevel"]:
        courses[column] = _clean_text(courses[column]).fillna("Unknown")
        courses[column] = courses[column].str.title()

    return courses.dropna(subset=["CourseID"]).reset_index(drop=True)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the transactions dataset."""
    transactions = _normalize_columns(df.copy())
    _validate_columns(transactions, REQUIRED_TRANSACTIONS_COLUMNS, "Transactions dataset")

    transactions = transactions.drop_duplicates(subset=["TransactionID"]).copy()
    transactions["TransactionID"] = _clean_text(transactions["TransactionID"])
    transactions["UserID"] = _clean_text(transactions["UserID"])
    transactions["CourseID"] = _clean_text(transactions["CourseID"])
    transactions["TransactionDate"] = pd.to_datetime(
        transactions["TransactionDate"],
        errors="coerce",
    )

    return transactions.dropna(
        subset=["TransactionID", "UserID", "CourseID", "TransactionDate"]
    ).reset_index(drop=True)
