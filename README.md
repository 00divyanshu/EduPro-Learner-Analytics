# EduPro Learner Analytics

Learner demographics and course enrollment behavior analysis for EduPro, an online learning platform. This is a descriptive analytics and learner intelligence project built with a professional Python pipeline and an interactive Streamlit dashboard.

## Project Objective

The project helps EduPro understand:

- which age groups are most active
- how enrollment behavior differs by gender
- which course categories, levels, and types attract demand
- how beginner, intermediate, and advanced learners behave
- how paid and free enrollments contribute to course strategy
- what business actions can improve planning, engagement, and inclusivity

## Live App Workflow

The Streamlit app runs from the repository data and automatically executes the analytics pipeline:

1. Load users, courses, and transactions from `data/raw/`
2. Clean and validate source data
3. Merge the three datasets into one master analytics table
4. Engineer learner, course, time, revenue, rating, and duration features
5. Calculate KPIs and generate business insights
6. Render an interactive dashboard with filters and Plotly charts

## Tech Stack

- Python
- Pandas and NumPy
- Plotly
- Streamlit
- Matplotlib and Seaborn
- OpenPyXL
- PyYAML
- Pytest

## Project Structure

```text
app/                  Streamlit dashboard
config/               Configurable project paths and settings
data/raw/             Deployment-ready EduPro source CSV files
data/processed/       Generated pipeline outputs, ignored by Git
data/outputs/         Optional generated exports, ignored by Git
notebooks/            EDA notebook
paper/                Research paper for the project
src/                  Reusable analytics modules
tests/                Unit tests for the data pipeline
```

## Dataset Files

The app expects these files:

```text
data/raw/users.csv
data/raw/courses.csv
data/raw/transactions.csv
```

The loader also recognizes the original EduPro export filenames if they are placed inside `data/raw/`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run Tests

```bash
python -m pytest -q
```

## Run Dashboard

```bash
streamlit run app/streamlit_app.py
```

## Streamlit Cloud Deployment

Use these settings when deploying from GitHub:

- Repository: `00divyanshu/EduPro-Learner-Analytics`
- Branch: `main`
- Main file path: `app/streamlit_app.py`
- Python dependencies: `requirements.txt`

Because the cleaned source CSV files are included in `data/raw/`, the app can run immediately after deployment.

## Dashboard Sections

- Executive View: KPIs, enrollment trends, top courses, insights
- Demographics: age group and gender enrollment behavior
- Behavior: course level, duration, rating, and category-level demand
- Revenue: paid/free behavior and revenue by category
- Data Preview: filtered master table for validation and explanation

## Portfolio Highlights

This project demonstrates:

- multi-table analytics pipeline design
- data cleaning and validation
- feature engineering for learner intelligence
- reusable modular Python code
- interactive dashboard development
- deployable Streamlit architecture
- business insight generation
- professional GitHub-ready documentation

## Research Paper

The project paper is available at:

```text
paper/research_paper.md
```

## Resume Summary

Built an end-to-end Streamlit learner analytics dashboard for EduPro using Python, Pandas, Plotly, and modular analytics pipelines to analyze 10,000 course enrollment transactions across learner demographics, course categories, course levels, and paid/free enrollment behavior.
