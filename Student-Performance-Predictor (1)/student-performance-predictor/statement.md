# Problem Statement

## Problem Statement

Educational institutions often identify students at risk of failing only
after formal exam results are declared — at which point it is too late to
intervene. Teachers rarely have an early, data-driven way to flag students
who need academic support based on ongoing indicators such as attendance,
study habits, and assignment completion.

**Student Performance Predictor** addresses this gap by using a machine
learning classification model to predict whether a student is likely to
**Pass** or **Fail**, based on measurable academic and behavioral factors.
This allows timely, proactive intervention rather than reactive
remediation after the fact.

## Scope of the Project

The project covers:
- Generation/ingestion and cleaning of student academic data
- Persistent storage of student records in a relational (SQLite) database
- Training and evaluating a supervised ML classification model
- A command-line dashboard for data loading, model training, visualization,
  and real-time single-student prediction
- Logging and retrieval of prediction history

The scope **excludes**: a production web front-end, multi-user
authentication, and integration with a live institutional student
information system — these are noted as future enhancements.

## Target Users

- **Teachers / Academic Mentors** — to identify at-risk students early and
  plan interventions (extra classes, counselling, parental engagement).
- **Academic Administrators** — to get an aggregate view of class
  performance trends via the generated analytics/reports.
- **Students** (indirectly, via a mentor) — to understand which factors
  most influence their likely outcome.

## High-Level Features

1. **Data Management Module** — loads/generates a student dataset, cleans
   and validates it, and stores it in a SQLite database.
2. **ML Model Module** — trains a Random Forest classifier on student
   features, evaluates it (accuracy, precision, recall, F1, confusion
   matrix), and predicts outcomes for new students in real time.
3. **Visualization & Reporting Module** — produces charts (class
   distribution, feature importance, confusion matrix, correlation
   heatmap) summarizing the data and model performance.
4. **Interactive CLI Dashboard** — ties the above modules together into a
   menu-driven workflow, including prediction history tracking (CRUD).
