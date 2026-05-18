"""End-to-end pipeline helpers for EDA and dashboard use."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.data_cleaning import clean_courses, clean_transactions, clean_users
from src.data_ingestion import load_project_datasets
from src.data_merging import find_orphan_transactions, merge_datasets
from src.feature_engineering import build_course_summary, build_learner_summary, create_features
from src.logger import get_logger


LOGGER = get_logger(__name__)


def run_pipeline(config: dict[str, Any], save_outputs: bool = True) -> dict[str, pd.DataFrame | dict[str, int]]:
    """Run the full analytics pipeline from raw datasets to processed outputs."""
    users_raw, courses_raw, transactions_raw = load_project_datasets(config)

    users = clean_users(users_raw)
    courses = clean_courses(courses_raw)
    transactions = clean_transactions(transactions_raw)
    validation_summary = find_orphan_transactions(users, courses, transactions)

    master = merge_datasets(users, courses, transactions)
    master = create_features(master)
    learner_summary = build_learner_summary(master)
    course_summary = build_course_summary(master)

    outputs = {
        "users": users,
        "courses": courses,
        "transactions": transactions,
        "master": master,
        "learner_summary": learner_summary,
        "course_summary": course_summary,
        "validation_summary": validation_summary,
    }

    if save_outputs:
        processed_dir = Path(config.get("processed_dir", "data/processed"))
        processed_dir.mkdir(parents=True, exist_ok=True)
        for name, frame in outputs.items():
            if isinstance(frame, pd.DataFrame):
                frame.to_csv(processed_dir / f"{name}.csv", index=False)
        LOGGER.info("Processed datasets saved to %s", processed_dir)

    return outputs

