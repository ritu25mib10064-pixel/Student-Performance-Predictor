# 🎓 Student Performance Predictor

An end-to-end Machine Learning system that predicts whether a student is
likely to **Pass** or **Fail**, based on academic and behavioral features
such as study hours, attendance, previous grades, and more — built as a
VITyarthi "Build Your Own Project" submission for the AIML course.

---

## 📌 Overview

Teachers often only learn a student is struggling after final results are
out. This project uses a supervised ML model (Random Forest Classifier)
trained on student academic/behavioral data to flag at-risk students
**early**, enabling proactive support. The system covers the full ML
pipeline: data ingestion → cleaning → storage → training → evaluation →
visualization → real-time prediction, wrapped in an interactive CLI
dashboard.

See [`statement.md`](statement.md) for the full problem statement, scope,
target users, and feature list.

---

## ✨ Features

- **Data Management** — generates/loads a student dataset, cleans and
  validates it (missing values, range checks), and stores it in a SQLite
  database.
- **ML Model** — trains a Random Forest classifier; reports accuracy,
  precision, recall, F1-score, and a confusion matrix.
- **Real-time Prediction** — enter a new student's details and get an
  instant Pass/Fail prediction with a confidence score.
- **Visual Analytics** — auto-generates charts: class distribution,
  feature importance, confusion matrix heatmap, correlation heatmap.
- **Prediction History (CRUD)** — every prediction is logged to the
  database and can be viewed later.
- **Interactive CLI Dashboard** — a simple menu ties every module
  together into one guided workflow.
- **Unit Tests** — `pytest` tests covering data cleaning and model
  training/prediction.
- **Logging** — all pipeline steps are logged to console and to
  `outputs/app.log`.

---

## 🧱 Tech Stack / Tools Used

| Category            | Tools                                   |
|----------------------|------------------------------------------|
| Language              | Python 3.12                              |
| ML / Data             | scikit-learn, pandas, numpy              |
| Visualization          | matplotlib, seaborn                      |
| Storage                | SQLite (via `sqlite3`)                   |
| Testing                 | pytest                                   |
| Diagrams               | Graphviz                                 |
| Version Control        | Git / GitHub                             |

---

## 📂 Project Structure

```
student-performance-predictor/
├── main.py                     # Non-interactive, full pipeline runner
├── generate_report.py          # Builds outputs/Project_Report.pdf
├── requirements.txt
├── README.md
├── statement.md
├── src/
│   ├── config.py                # Central configuration
│   ├── logger.py                # Shared logger utility
│   ├── data_manager.py          # Module 1: Data ingestion, cleaning, storage
│   ├── model.py                 # Module 2: ML training, evaluation, prediction
│   ├── visualizer.py            # Module 3: Charts & visual reports
│   └── app.py                   # Interactive CLI dashboard (UI layer)
├── tests/
│   └── test_model.py            # Unit tests (pytest)
├── diagrams/
│   ├── gen_diagrams.py          # Generates architecture & workflow diagrams
│   ├── gen_uml.py               # Generates UML + ER diagrams
│   ├── architecture_diagram.png
│   ├── workflow_diagram.png
│   ├── usecase_diagram.png
│   ├── class_diagram.png
│   ├── sequence_diagram.png
│   └── er_diagram.png
├── data/                        # Generated CSV + SQLite DB (created at runtime)
└── outputs/                     # Generated charts + logs (created at runtime)
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd student-performance-predictor
   ```

2. **(Recommended) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ How to Run

### Option A — Full automated pipeline (recommended for a quick demo)
Runs data prep → training → evaluation → charts → one sample prediction:
```bash
python main.py
```

### Option B — Interactive CLI dashboard
```bash
python -m src.app
```
Then use the on-screen menu to load data, train the model, generate
charts, predict a new student's outcome, or view prediction history.

### Regenerating the diagrams
```bash
python diagrams/gen_diagrams.py
python diagrams/gen_uml.py
```

### Regenerating the project report
Rebuilds `outputs/Project_Report.pdf` from the current diagrams and charts:
```bash
python generate_report.py
```

---

## 🧪 Instructions for Testing

Run the unit test suite with:
```bash
pytest tests/ -v
```

This validates:
- Correct dataset shape/columns after generation
- Missing values are handled during cleaning
- Feature values respect valid ranges after cleaning
- The model trains successfully and returns valid metrics
- Single-student predictions return a valid label + confidence score

---

## 📊 Sample Results

On the generated dataset (800 synthetic student records, 80/20 train-test
split), the Random Forest model typically achieves:

| Metric     | Score (approx.) |
|------------|------------------|
| Accuracy    | ~0.68–0.75        |
| Precision   | ~0.74–0.80        |
| Recall      | ~0.76–0.85        |
| F1-Score    | ~0.75–0.80        |

*(Exact numbers vary slightly by run since the dataset is regenerated with
realistic noise. See `outputs/` after running `main.py` for the current
run's charts.)*

---

## 📸 Screenshots

Generated charts (found in `outputs/` after running the pipeline):
- `class_distribution.png` — Pass vs Fail split in the dataset
- `feature_importance.png` — Which features most influence predictions
- `confusion_matrix.png` — Model's prediction accuracy breakdown
- `correlation_heatmap.png` — Relationships between student features

Design diagrams (found in `diagrams/`):
- Architecture, Workflow, Use Case, Class, Sequence, and ER diagrams

---

## 📝 Notes on the Dataset

The dataset is synthetically generated (`src/data_manager.py`) with
feature distributions modeled on publicly known student-performance
datasets (e.g., UCI's Student Performance dataset), so the project is
fully reproducible without any external download. To use a **real**
dataset instead, replace `load_or_generate_data()` with a `pd.read_csv()`
call using the same column names defined in `src/config.py`.

---

## 👤 Author

Submitted as part of the VITyarthi "Build Your Own Project" — AIML course.
