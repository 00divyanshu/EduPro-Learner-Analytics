"""Dataset integration utilities."""

from __future__ import annotations

import pandas as pd


def merge_datasets(
    users: pd.DataFrame,
    courses: pd.DataFrame,
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """Merge transactions with user and course attributes."""
    user_transactions = transactions.merge(users, on="UserID", how="inner")
    master_df = user_transactions.merge(courses, on="CourseID", how="inner")
    return master_df.sort_values("TransactionDate").reset_index(drop=True)


def find_orphan_transactions(
    users: pd.DataFrame,
    courses: pd.DataFrame,
    transactions: pd.DataFrame,
) -> dict[str, int]:
    """Count transactions that cannot be matched to users or courses."""
    missing_users = ~transactions["UserID"].isin(users["UserID"])
    missing_courses = ~transactions["CourseID"].isin(courses["CourseID"])
    return {
        "transactions_with_missing_user": int(missing_users.sum()),
        "transactions_with_missing_course": int(missing_courses.sum()),
    }

