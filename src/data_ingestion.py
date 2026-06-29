"""Dataset loading and configuration utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.exception import DataLoadingError
from src.logger import get_logger


LOGGER = get_logger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

FALLBACK_DATASET_NAMES = {
    "users": [
        "users.csv",
        "EduPro Online Platform - Users.csv",
    ],
    "courses": [
        "courses.csv",
        "EduPro Online Platform - Courses.csv",
    ],
    "transactions": [
        "transactions.csv",
        "EduPro Online Platform - Transactions.csv",
    ],
}


def load_config(config_path: str | Path = "config/config.yaml") -> dict[str, Any]:
    """Load YAML configuration used by the pipeline and dashboard."""
    path = Path(config_path)
    if not path.exists():
        raise DataLoadingError(f"Configuration file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        content = file.read()

    try:
        import yaml

        return yaml.safe_load(content) or {}
    except ModuleNotFoundError:
        return _load_simple_yaml(content)


def _load_simple_yaml(content: str) -> dict[str, Any]:
    """Parse the simple two-level YAML structure used by this project."""
    config: dict[str, Any] = {}
    current_section: str | None = None

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if not line.startswith(" ") and line.endswith(":"):
            current_section = line[:-1].strip()
            config[current_section] = {}
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if current_section and raw_line.startswith(" "):
            config[current_section][key] = value
        else:
            current_section = None
            config[key] = value

    return config


def load_dataset(path: str | Path, sheet_name: str | int | None = None) -> pd.DataFrame:
    """Load a CSV or Excel dataset into a DataFrame."""
    file_path = Path(path)
    if not file_path.exists():
        raise DataLoadingError(f"Dataset not found: {file_path}")

    suffix = file_path.suffix.lower()
    LOGGER.info("Loading dataset from %s", file_path)

    try:
        if suffix == ".csv":
            return pd.read_csv(file_path)
        if suffix in {".xlsx", ".xls"}:
            return pd.read_excel(file_path, sheet_name=sheet_name or 0, engine="openpyxl")
    except Exception as exc:
        raise DataLoadingError(f"Unable to load dataset: {file_path}") from exc

    raise DataLoadingError(f"Unsupported file type: {suffix}. Use CSV or Excel files.")


def resolve_dataset_path(dataset_key: str, configured_path: str | Path) -> Path:
    """Resolve configured dataset paths and known EduPro raw-file names."""
    configured = Path(configured_path)
    candidates = [configured]

    if not configured.is_absolute():
        candidates.append(PROJECT_ROOT / configured)

    for filename in FALLBACK_DATASET_NAMES.get(dataset_key, []):
        candidates.append(PROJECT_ROOT / "data" / "raw" / filename)

    for candidate in candidates:
        if candidate.exists():
            return candidate

    searched = "\n".join(f"- {candidate}" for candidate in candidates)
    raise DataLoadingError(
        f"Could not find the {dataset_key} dataset. Searched:\n{searched}"
    )


def load_project_datasets(config: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load users, courses, and transactions using paths from configuration."""
    paths = config["data_paths"]
    users = load_dataset(resolve_dataset_path("users", paths["users"]))
    courses = load_dataset(resolve_dataset_path("courses", paths["courses"]))
    transactions = load_dataset(resolve_dataset_path("transactions", paths["transactions"]))
    return users, courses, transactions
