# EduPro Learner Demographics and Enrollment Analytics

An end-to-end descriptive analytics project for understanding learner demographics and course enrollment behavior on EduPro, an online learning platform.

## Project Goal

The goal is to help EduPro answer business questions such as:

- Which age groups are most active?
- How do enrollment patterns differ by gender?
- Which course categories are most popular?
- Which course levels are preferred by different learner segments?
- What insights can improve course planning, learner engagement, and inclusivity?

## Tech Stack

- Python
- Pandas and NumPy
- Plotly
- Streamlit
- OpenPyXL
- PyYAML
- Pytest

## Folder Structure

```text
app/                  Streamlit dashboard
config/               Project configuration
data/raw/             Input datasets from Google Drive export
data/processed/       Pipeline-generated clean datasets
data/outputs/         Optional charts/reports/exports
docs/                 Reports, summaries, interview notes
notebooks/            EDA notebook
src/                  Reusable project modules
tests/                Pipeline tests
```

## Dataset Files

Place the exported Google Drive files in `data/raw/` with these names:

```text
data/raw/users.csv
data/raw/courses.csv
data/raw/transactions.csv
```

Expected columns:

- Users: `UserID`, `UserName`, `Age`, `Gender`
- Courses: `CourseID`, `CourseName`, `CourseCategory`, `CourseType`, `CourseLevel`
- Transactions: `TransactionID`, `UserID`, `CourseID`, `TransactionDate`

Excel files are supported by the loader, but the default config points to CSV files. Update `config/config.yaml` if your files are `.xlsx`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run Tests

```bash
pytest
```

## Run Dashboard

```bash
streamlit run app/streamlit_app.py
```

## Project Workflow

1. Load datasets from `data/raw/`
2. Validate required columns
3. Clean users, courses, and transactions
4. Merge all datasets into a master analytics table
5. Create demographic and enrollment features
6. Calculate KPIs
7. Generate charts and business insights
8. Present results in Streamlit and project reports

## Portfolio Value

This project demonstrates:

- data cleaning and preprocessing
- multi-table data integration
- feature engineering
- descriptive analytics
- dashboard development
- business insight generation
- professional Python project structuring

