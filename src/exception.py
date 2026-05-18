"""Custom exceptions for the EduPro analytics project."""


class EduProAnalyticsError(Exception):
    """Base exception for project-specific errors."""


class DataValidationError(EduProAnalyticsError):
    """Raised when input data does not match the expected schema."""


class DataLoadingError(EduProAnalyticsError):
    """Raised when a dataset cannot be loaded from disk."""

