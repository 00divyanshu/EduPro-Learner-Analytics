# Learner Demographics and Course Enrollment Behavior Analysis on EduPro

## Abstract

Online learning platforms need clear learner intelligence to improve course planning, engagement, inclusivity, and business strategy. This project analyzes EduPro user, course, and enrollment transaction data using descriptive analytics. The study integrates learner demographics, course metadata, and enrollment behavior to identify active age groups, gender-based participation patterns, course category demand, course level preferences, paid/free behavior, and monthly enrollment trends. The final output is a modular Python analytics pipeline and an interactive Streamlit dashboard that supports business decision-making.

## Keywords

Learner analytics, descriptive analytics, online education, demographic analysis, course enrollment, Streamlit dashboard, business intelligence

## 1. Introduction

EduPro is an online learning platform that serves learners across multiple age groups, genders, subject interests, and learning goals. As course catalogs grow, platform teams need more than raw enrollment counts. They need to understand who is learning, which subjects attract demand, how beginner and advanced learners behave, and where targeted engagement strategies can improve outcomes.

This project is intentionally designed as a descriptive analytics system rather than a prediction-first machine learning project. The goal is to transform operational platform data into practical learner intelligence through clean data integration, reusable analytics code, and an interactive dashboard.

## 2. Problem Statement

EduPro needs a structured analytics solution to answer the following business questions:

- Which age groups are most active on the platform?
- How do enrollment patterns differ by gender?
- Which course categories and course levels are most popular?
- How do beginner, intermediate, and advanced learners differ in behavior?
- What paid/free enrollment patterns can support course planning and monetization?
- What insights can help EduPro make data-driven decisions?

## 3. Dataset Description

The project uses three related datasets:

- Users: learner identity, age, gender, username, and email fields.
- Courses: course identity, name, category, type, level, price, duration, and rating.
- Transactions: enrollment transaction identity, learner ID, course ID, transaction date, amount, payment method, and teacher ID.

The datasets are integrated using `UserID` and `CourseID`. The transaction table acts as the central fact table, while users and courses provide demographic and course-level context.

## 4. Methodology

The project follows an industry-style analytics workflow:

1. Data ingestion loads CSV or Excel files from configurable paths.
2. Data validation checks required columns and dataset availability.
3. Data cleaning standardizes identifiers, demographic labels, numeric fields, and transaction dates.
4. Data merging joins transactions with user and course metadata.
5. Feature engineering creates age groups, enrollment month, quarter, weekday, learner segment, revenue band, duration band, rating band, and paid enrollment indicators.
6. KPI generation calculates learner count, enrollment count, course count, revenue, paid enrollment rate, top category, most active age group, average rating, and beginner-to-advanced ratio.
7. Visualization and dashboarding present insights through Streamlit and Plotly.

## 5. Analytics Framework

The analysis focuses on five dimensions:

- Demographic behavior: age group and gender participation.
- Course demand: category, type, level, and top course enrollment.
- Engagement behavior: beginner versus advanced preference and course duration patterns.
- Revenue behavior: paid enrollments, total revenue, paid rate, and revenue by category.
- Time behavior: monthly enrollment trend and peak enrollment periods.

This framework keeps the project business-focused while still demonstrating reusable AI/ML project architecture.

## 6. Expected Business Insights

The dashboard is designed to surface insights such as:

- The most active learner demographic segment.
- Categories that drive the highest enrollment volume.
- Course levels preferred by different age and gender groups.
- Whether free courses dominate acquisition behavior.
- Which categories generate the strongest paid enrollment revenue.
- Seasonal or monthly periods where enrollment activity peaks.

These insights can support course catalog planning, learner onboarding, campaign timing, inclusivity analysis, and progression design from beginner to advanced courses.

## 7. System Architecture

The project is organized into reusable modules:

- `src/data_ingestion.py` handles configuration and dataset loading.
- `src/data_cleaning.py` validates and standardizes source data.
- `src/data_merging.py` integrates the three datasets.
- `src/feature_engineering.py` creates analysis-ready features and summary tables.
- `src/kpi_metrics.py` calculates dashboard KPIs.
- `src/visualizations.py` builds Plotly charts.
- `src/insights.py` generates plain-English business insights.
- `app/streamlit_app.py` provides the deployable dashboard interface.

This modular structure makes the project easier to test, debug, explain in interviews, and deploy.

## 8. Practical Implications

EduPro can use this analytics system to:

- Prioritize high-demand course categories.
- Improve learner journeys by matching course level to demographic behavior.
- Identify underrepresented learner groups for inclusivity initiatives.
- Use free courses as acquisition channels and paid courses as progression paths.
- Time marketing campaigns around periods of high enrollment activity.
- Monitor category-level performance through an interactive dashboard.

## 9. Limitations

This project does not infer causality or predict future enrollments. It describes historical behavior from the available datasets. Additional features such as course completion, session duration, satisfaction surveys, device type, geography, and marketing source would improve future learner intelligence.

## 10. Future Work

Future versions can include:

- Cohort analysis for learner retention.
- Funnel analysis from free to paid courses.
- Optional unsupervised learner segmentation.
- Course recommendation experiments.
- Completion and engagement tracking if activity logs become available.
- Automated scheduled reporting for EduPro decision-makers.

## 11. Conclusion

The EduPro learner analytics project demonstrates a professional descriptive analytics workflow from raw multi-table data to a deployment-ready Streamlit dashboard. It provides a practical way to understand learner demographics, course demand, enrollment behavior, and revenue patterns while maintaining clean, modular, and portfolio-ready engineering practices.
