"""Tests for the EduPro data pipeline."""

import pandas as pd

from src.data_cleaning import clean_courses, clean_transactions, clean_users
from src.data_merging import merge_datasets
from src.feature_engineering import assign_age_group, create_features
from src.kpi_metrics import calculate_kpis


def sample_data():
    users = pd.DataFrame(
        {
            "UserID": ["U1", "U2", "U3"],
            "UserName": ["Asha", "Rahul", "Meera"],
            "Age": [18, 27, 46],
            "Gender": ["F", "Male", "Female"],
        }
    )
    courses = pd.DataFrame(
        {
            "CourseID": ["C1", "C2"],
            "CourseName": ["Python Basics", "Advanced SQL"],
            "CourseCategory": ["Data Science", "Data Analytics"],
            "CourseType": ["Self Paced", "Live"],
            "CourseLevel": ["Beginner", "Advanced"],
        }
    )
    transactions = pd.DataFrame(
        {
            "TransactionID": ["T1", "T2", "T3"],
            "UserID": ["U1", "U2", "U3"],
            "CourseID": ["C1", "C1", "C2"],
            "TransactionDate": ["01/01/2026", "05/01/2026", "10/02/2026"],
            "Amount": [0, 120.0, 250.0],
        }
    )
    return users, courses, transactions


def test_cleaning_and_merging_pipeline():
    users, courses, transactions = sample_data()

    clean_u = clean_users(users)
    clean_c = clean_courses(courses)
    clean_t = clean_transactions(transactions)
    master = create_features(merge_datasets(clean_u, clean_c, clean_t))

    assert master.shape[0] == 3
    assert {"AgeGroup", "EnrollmentMonth", "LearnerSegment"}.issubset(master.columns)
    assert master["TransactionDate"].dtype.kind == "M"
    assert str(master["TransactionDate"].min().date()) == "2026-01-01"


def test_age_group_assignment():
    assert assign_age_group(18) == "Teen"
    assert assign_age_group(27) == "Young Adult"
    assert assign_age_group(46) == "Mid-Career Learner"
    assert assign_age_group(65) == "Senior Learner"


def test_kpi_metrics_have_expected_keys():
    users, courses, transactions = sample_data()
    master = create_features(
        merge_datasets(clean_users(users), clean_courses(courses), clean_transactions(transactions))
    )
    kpis = calculate_kpis(master)

    expected = {
        "total_learners",
        "total_courses",
        "total_enrollments",
        "most_popular_category",
        "most_active_age_group",
        "beginner_enrollments",
        "advanced_enrollments",
        "beginner_to_advanced_ratio",
        "total_revenue",
        "paid_enrollment_rate",
        "avg_enrollments_per_learner",
        "avg_course_rating",
    }
    assert expected.issubset(kpis.keys())
    assert kpis["total_enrollments"] == 3
    assert kpis["total_revenue"] == 370.0
