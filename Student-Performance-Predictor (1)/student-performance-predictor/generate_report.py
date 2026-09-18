"""
generate_report.py
-------------------
Builds the final Project Report PDF (for portal submission) covering all
15 required sections, embedding the diagrams and charts already generated
in diagrams/ and outputs/.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle,
    ListFlowable, ListItem,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

BASE = os.path.dirname(os.path.abspath(__file__))
DIAG = os.path.join(BASE, "diagrams")
OUT = os.path.join(BASE, "outputs")
REPORT_PATH = os.path.join(BASE, "outputs", "Project_Report.pdf")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1Custom", fontSize=20, leading=25, spaceBefore=6, spaceAfter=16,
                           textColor=colors.HexColor("#1F3864"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="H2Custom", fontSize=15, leading=19, spaceBefore=18, spaceAfter=10,
                           textColor=colors.HexColor("#2E5395"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="BodyCustom", fontSize=12, leading=18, alignment=TA_JUSTIFY,
                           spaceAfter=12))
styles.add(ParagraphStyle(name="CoverTitle", fontSize=30, leading=36, alignment=TA_CENTER,
                           textColor=colors.HexColor("#1F3864"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CoverSub", fontSize=15, leading=22, alignment=TA_CENTER,
                           textColor=colors.HexColor("#444444")))
styles.add(ParagraphStyle(name="CoverUni", fontSize=22, leading=26, alignment=TA_CENTER,
                           textColor=colors.HexColor("#1F3864"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CoverUniSub", fontSize=12, leading=16, alignment=TA_CENTER,
                           textColor=colors.HexColor("#666666")))
styles.add(ParagraphStyle(name="CoverInfo", fontSize=13, leading=20, alignment=TA_CENTER,
                           textColor=colors.HexColor("#222222")))
styles.add(ParagraphStyle(name="CoverInfoBold", fontSize=14, leading=20, alignment=TA_CENTER,
                           textColor=colors.HexColor("#1F3864"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Caption", fontSize=10.5, leading=14, alignment=TA_CENTER,
                           textColor=colors.HexColor("#555555"), fontName="Helvetica-Oblique",
                           spaceBefore=6))

story = []


def h1(text):
    story.append(Paragraph(text, styles["H1Custom"]))


def h2(text):
    story.append(Paragraph(text, styles["H2Custom"]))


def body(text):
    story.append(Paragraph(text, styles["BodyCustom"]))


def bullets(items):
    story.append(ListFlowable(
        [ListItem(Paragraph(i, styles["BodyCustom"]), leftIndent=12, spaceAfter=8) for i in items],
        bulletType="bullet", start="circle"
    ))
    story.append(Spacer(1, 10))


def figure(path, caption, width=15.5 * cm, max_height=20 * cm):
    if not os.path.exists(path):
        return
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        w_px, h_px = im.size
    aspect = h_px / w_px
    height = width * aspect
    if height > max_height:
        height = max_height
        width = height / aspect
    img = Image(path, width=width, height=height)
    img.hAlign = "CENTER"
    story.append(img)
    story.append(Paragraph(caption, styles["Caption"]))
    story.append(Spacer(1, 18))


# ===========================================================================
# 1. COVER PAGE
# ===========================================================================
# Top accent bar
bar = Table([[""]], colWidths=[17 * cm], rowHeights=[0.35 * cm])
bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1F3864"))]))
story.append(bar)
story.append(Spacer(1, 1.2 * cm))

story.append(Paragraph("VIT BHOPAL UNIVERSITY", styles["CoverUni"]))
story.append(Spacer(1, 0.15 * cm))
story.append(Paragraph("School of Computing Science and Engineering", styles["CoverUniSub"]))
story.append(Spacer(1, 0.6 * cm))

# Thin divider
divider = Table([[""]], colWidths=[8 * cm], rowHeights=[0.04 * cm])
divider.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#C7A857"))]))
divider.hAlign = "CENTER"
story.append(divider)

story.append(Spacer(1, 2.8 * cm))
story.append(Paragraph("Student Performance Predictor", styles["CoverTitle"]))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("An AI/ML-based System to Predict Student Academic Outcomes",
                        styles["CoverSub"]))

story.append(Spacer(1, 2.5 * cm))
story.append(Paragraph("PROJECT REPORT", styles["CoverInfoBold"]))
story.append(Paragraph("Submitted for: VITyarthi — Build Your Own Project (AIML)",
                        styles["CoverInfo"]))

story.append(Spacer(1, 2.8 * cm))

# Details box
details = Table(
    [
        ["Course", "Artificial Intelligence & Machine Learning"],
        ["Submission Type", "Individual Project"],
        ["Submitted by", "Ritu Yadav"],
        ["Registration No.", "25MIB10064"],
    ],
    colWidths=[5.5 * cm, 8.5 * cm],
)
details.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 12.5),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1F3864")),
    ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#222222")),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#DDDDDD")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
details.hAlign = "CENTER"
story.append(details)

story.append(Spacer(1, 2.5 * cm))
bar2 = Table([[""]], colWidths=[17 * cm], rowHeights=[0.35 * cm])
bar2.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1F3864"))]))
story.append(bar2)

story.append(PageBreak())

# ===========================================================================
# 2. INTRODUCTION
# ===========================================================================
h1("2. Introduction")
body("""Academic institutions generate a large amount of data about student behaviour and
performance -- attendance records, assignment completion, study patterns, and past grades.
This project, <b>Student Performance Predictor</b>, applies supervised machine learning to this
kind of data to forecast whether a student is likely to Pass or Fail, well before formal exam
results are declared. The system was built end-to-end: from data preparation and storage,
through model training and evaluation, to an interactive interface for real-time predictions.""")
body("""The project directly applies core AIML course concepts: data preprocessing, feature
engineering, supervised classification (Random Forest), model evaluation metrics, and
data visualization, while also demonstrating good software engineering practice through
modular code, a persistent data layer, logging, and automated tests.""")

# ===========================================================================
# 3. PROBLEM STATEMENT
# ===========================================================================
h1("3. Problem Statement")
body("""Teachers and academic mentors typically identify struggling students only after formal
assessments -- at which point corrective action is delayed. There is a need for an early-warning
system that uses ongoing, measurable indicators (study hours, attendance, assignment completion,
past grades, sleep, extracurricular load, and parental support) to flag at-risk students
proactively, so timely academic support can be offered.""")

# ===========================================================================
# 4. FUNCTIONAL REQUIREMENTS
# ===========================================================================
h1("4. Functional Requirements")
body("The system implements three major functional modules, each with a clear input/output structure:")
bullets([
    "<b>Data Management Module</b> -- Input: raw student records (generated or CSV). "
    "Output: a cleaned dataset persisted to a SQLite database.",
    "<b>ML Model Module</b> -- Input: cleaned feature set. Output: a trained classifier, "
    "evaluation metrics (accuracy, precision, recall, F1), and Pass/Fail predictions with "
    "a confidence score for new students.",
    "<b>Visualization &amp; Reporting Module</b> -- Input: dataset + trained model metrics. "
    "Output: charts (class distribution, feature importance, confusion matrix, correlation "
    "heatmap) saved to disk.",
    "<b>CRUD on predictions</b> -- every prediction made is <i>created</i> (inserted) into the "
    "database and can be <i>read</i> back via the prediction-history view.",
])

# ===========================================================================
# 5. NON-FUNCTIONAL REQUIREMENTS
# ===========================================================================
h1("5. Non-Functional Requirements")
nfr_data = [
    ["Requirement", "How it is addressed"],
    ["Performance", "Random Forest training on 800 records completes in well under a "
                     "second; predictions are near-instant."],
    ["Reliability", "Data cleaning clips out-of-range values and fills missing data instead "
                     "of crashing; stratified train/test split keeps evaluation stable."],
    ["Security", "No external network calls at runtime; all data stays local in the SQLite "
                  "file, reducing exposure of student data."],
    ["Usability", "A simple numbered CLI menu guides the user through the entire workflow "
                  "with sensible input defaults."],
    ["Scalability", "The modular pipeline can scale to a larger dataset or be swapped to a "
                     "different model with minimal code change (single Config file)."],
    ["Maintainability", "Code is split into single-responsibility modules (config, logger, "
                         "data, model, visualizer, app) with docstrings throughout."],
    ["Error Handling", "try/except blocks guard file and DB operations; invalid menu input "
                        "is handled gracefully without crashing the app."],
    ["Logging/Monitoring", "A shared logger (src/logger.py) records every pipeline step to "
                            "console and to outputs/app.log with timestamps."],
]
t = Table(nfr_data, colWidths=[3.5 * cm, 11.5 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E5395")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F5FA")]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(PageBreak())

# ===========================================================================
# 6. SYSTEM ARCHITECTURE
# ===========================================================================
h1("6. System Architecture")
body("""The system follows a layered architecture with a clear separation between the
presentation (CLI), application/logic, and data layers, as shown below.""")
figure(os.path.join(DIAG, "architecture_diagram.png"), "Figure 1: System Architecture Diagram",
       width=16.5 * cm)

# ===========================================================================
# 7. DESIGN DIAGRAMS
# ===========================================================================
story.append(PageBreak())
h1("7. Design Diagrams")

h2("7.1 Use Case Diagram")
body("Two actors interact with the system: the Admin/Teacher (data prep, training, reports) "
     "and the Student/User (requesting a prediction, viewing history).")
figure(os.path.join(DIAG, "usecase_diagram.png"), "Figure 2: Use Case Diagram", width=15 * cm)

story.append(PageBreak())
h2("7.2 Process Flow / Workflow Diagram")
body("The end-to-end pipeline from raw data to a logged prediction is shown below.")
figure(os.path.join(DIAG, "workflow_diagram.png"), "Figure 3: Process Flow / Workflow Diagram", width=14*cm)

story.append(PageBreak())
h2("7.3 Sequence Diagram")
body("This diagram illustrates the runtime sequence of a single prediction request, from user "
     "input to the logged database record.")
figure(os.path.join(DIAG, "sequence_diagram.png"), "Figure 4: Sequence Diagram - Predict Outcome Flow",
       width=16.5 * cm)

story.append(PageBreak())
h2("7.4 Class Diagram")
body("The core classes/modules and their relationships are shown below.")
figure(os.path.join(DIAG, "class_diagram.png"), "Figure 5: Class Diagram", width=16.5 * cm)

story.append(PageBreak())
h2("7.5 ER Diagram (Database Schema)")
body("The SQLite database has two tables: <b>students</b> (the training dataset) and "
     "<b>predictions</b> (a log of every prediction made, related to students by student_id).")
figure(os.path.join(DIAG, "er_diagram.png"), "Figure 6: Entity-Relationship Diagram", width=16 * cm)

story.append(PageBreak())

# ===========================================================================
# 8. DESIGN DECISIONS & RATIONALE
# ===========================================================================
h1("8. Design Decisions & Rationale")
bullets([
    "<b>Random Forest Classifier</b> was chosen over a single Decision Tree or Logistic "
    "Regression because it handles non-linear feature interactions well, is robust to "
    "outliers, and provides built-in feature-importance scores useful for explainability.",
    "<b>SQLite</b> was chosen as the storage layer because it requires no separate server "
    "process, keeps the project easy to run anywhere, and is sufficient for the dataset "
    "sizes involved, while still demonstrating real relational storage and CRUD operations.",
    "<b>StandardScaler</b> is applied before classification since Random Forest performance "
    "and, more importantly, comparability of feature magnitudes benefits from standardized "
    "inputs, and it keeps the pipeline ready for swapping in scale-sensitive models later.",
    "<b>A synthetic-but-realistic dataset</b> generator was used (rather than a bundled real "
    "dataset) to keep the project fully reproducible without external downloads, while the "
    "feature set and distributions were deliberately modeled on well-known, publicly "
    "documented student-performance datasets.",
    "<b>A CLI dashboard</b> (instead of a full web app) was chosen to keep the project focused "
    "on the AIML pipeline itself and easy to run/test in any environment without extra "
    "infrastructure, while still satisfying the 'clear user workflow' requirement.",
])

# ===========================================================================
# 9. IMPLEMENTATION DETAILS
# ===========================================================================
h1("9. Implementation Details")
body("The project is implemented in Python 3, organized into the following modules:")
impl_data = [
    ["File", "Responsibility"],
    ["src/config.py", "Central configuration: paths, feature list, model hyperparameters."],
    ["src/logger.py", "Shared logger writing to console and outputs/app.log."],
    ["src/data_manager.py", "Dataset generation, cleaning/validation, SQLite storage, CRUD "
                             "for predictions."],
    ["src/model.py", "PerformanceModel class: scaling, training, evaluation, single-student "
                      "prediction, save/load."],
    ["src/visualizer.py", "Generates all evaluation/analytics charts (matplotlib/seaborn)."],
    ["src/app.py", "Interactive CLI dashboard tying all modules together."],
    ["main.py", "Non-interactive script that runs the entire pipeline end-to-end."],
    ["tests/test_model.py", "Automated unit tests (pytest) for data cleaning and model "
                             "behaviour."],
    ["diagrams/gen_diagrams.py, gen_uml.py", "Scripts that generate all design diagrams "
                                              "programmatically using Graphviz."],
]
t2 = Table(impl_data, colWidths=[5 * cm, 10 * cm])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E5395")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F5FA")]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t2)
story.append(Spacer(1, 8))
body("""<b>Dataset:</b> 800 synthetic student records with 7 numeric/ordinal features
(study_hours_per_week, attendance_percent, previous_grade, assignments_completed_percent,
sleep_hours, extracurricular_hours, parental_support_score) and a binary target
(final_result: Pass/Fail). ~3% of records had a missing value intentionally introduced to
exercise the cleaning logic.""")
body("""<b>Model selection rationale:</b> Random Forest was compared conceptually against
Logistic Regression and a single Decision Tree; Random Forest was selected for its balance of
accuracy, robustness to noisy/correlated features, and interpretable feature-importance output,
all relevant to an educational-intervention use case where explaining *why* a prediction was
made matters.""")
body("""<b>Evaluation methodology:</b> An 80/20 stratified train-test split preserves the
Pass/Fail class ratio in both sets. The model is scored on accuracy, precision, recall, and
F1-score (with "Pass" as the positive class), plus a confusion matrix for error-type analysis.""")

story.append(PageBreak())

# ===========================================================================
# 10. SCREENSHOTS / RESULTS
# ===========================================================================
h1("10. Screenshots / Results")
figure(os.path.join(OUT, "class_distribution.png"), "Figure 7: Class Distribution (Pass vs Fail)", width=13*cm)
story.append(PageBreak())
figure(os.path.join(OUT, "feature_importance.png"), "Figure 8: Feature Importance", width=15*cm)
story.append(PageBreak())
figure(os.path.join(OUT, "confusion_matrix.png"), "Figure 9: Confusion Matrix", width=13*cm)
story.append(PageBreak())
figure(os.path.join(OUT, "correlation_heatmap.png"), "Figure 10: Feature Correlation Heatmap", width=15*cm)
story.append(PageBreak())

# ===========================================================================
# 11. TESTING APPROACH
# ===========================================================================
h1("11. Testing Approach")
body("Automated unit tests were written using <b>pytest</b> and cover both the data pipeline "
     "and the ML model:")
bullets([
    "Dataset generation produces the expected shape and required columns.",
    "Generated target values are restricted to the valid label set (Pass/Fail).",
    "Cleaning removes all missing values from the feature columns.",
    "Cleaning enforces valid value ranges (e.g., percentages within 0-100).",
    "The model trains successfully and returns metrics within valid bounds (0-1).",
    "Single-student prediction returns a valid label and a confidence score in [0, 1].",
])
body("All 6 tests pass consistently (<i>pytest tests/ -v</i>). Manual end-to-end testing was "
     "also performed by running <i>main.py</i> and the interactive <i>src/app.py</i> dashboard "
     "through every menu option.")

# ===========================================================================
# 12. CHALLENGES FACED
# ===========================================================================
h1("12. Challenges Faced")
bullets([
    "<b>Balancing dataset realism vs. separability</b> -- an early version of the synthetic "
    "data generator produced an almost perfectly separable Pass/Fail boundary, giving "
    "unrealistically high (~99%) accuracy. Noise was added to the underlying scoring formula "
    "to make the classification problem more realistic and representative of real-world data.",
    "<b>Keeping the diagrams reproducible</b> -- rather than hand-drawing UML diagrams in an "
    "external tool (which would be hard to version-control and regenerate), all six diagrams "
    "were generated programmatically with Graphviz, so they stay in sync with the code.",
    "<b>Designing a clean CRUD flow</b> for predictions without over-engineering the storage "
    "layer -- solved by adding a lightweight <i>predictions</i> table alongside the main "
    "<i>students</i> table in the same SQLite database.",
])

# ===========================================================================
# 13. LEARNINGS & KEY TAKEAWAYS
# ===========================================================================
h1("13. Learnings & Key Takeaways")
bullets([
    "Hands-on experience with the full supervised ML lifecycle: data cleaning, feature "
    "scaling, model training, evaluation metrics, and deploying a model for real-time "
    "single-record inference.",
    "Practical understanding of why realistic (noisy) data is essential to building and "
    "evaluating a meaningful classifier, rather than an artificially perfect one.",
    "Experience integrating an ML pipeline with a persistent relational data layer (SQLite) "
    "and CRUD operations, not just a one-off notebook.",
    "Reinforced good software engineering habits -- modular design, logging, configuration "
    "management, and automated testing -- applied specifically to an ML project.",
])

# ===========================================================================
# 14. FUTURE ENHANCEMENTS
# ===========================================================================
h1("14. Future Enhancements")
bullets([
    "Replace the synthetic dataset with a real, anonymized institutional dataset (with "
    "appropriate consent/privacy safeguards).",
    "Add a web-based dashboard (e.g., Flask/Streamlit) for a richer, multi-user interface.",
    "Experiment with additional models (Gradient Boosting, XGBoost, Neural Networks) and "
    "hyperparameter tuning to further improve accuracy.",
    "Add authentication and role-based access so teachers and students see appropriately "
    "scoped views.",
    "Extend the target from binary Pass/Fail to a multi-class grade-band prediction.",
])

# ===========================================================================
# 15. REFERENCES
# ===========================================================================
h1("15. References")
bullets([
    "Cortez, P. and Silva, A. (2008). <i>Using Data Mining to Predict Secondary School "
    "Student Performance.</i> UCI Machine Learning Repository -- Student Performance Data "
    "Set (feature-distribution reference for the synthetic dataset).",
    "Pedregosa et al. (2011). <i>Scikit-learn: Machine Learning in Python.</i> Journal of "
    "Machine Learning Research, 12, 2825-2830.",
    "Breiman, L. (2001). <i>Random Forests.</i> Machine Learning, 45(1), 5-32.",
    "Official documentation: scikit-learn.org, pandas.pydata.org, sqlite.org, "
    "graphviz.org.",
])

# ===========================================================================
# Build PDF
# ===========================================================================
doc = SimpleDocTemplate(
    REPORT_PATH, pagesize=A4,
    topMargin=1.8 * cm, bottomMargin=1.8 * cm,
    leftMargin=2 * cm, rightMargin=2 * cm,
    title="Student Performance Predictor - Project Report",
)
doc.build(story)
print(f"Report generated at: {REPORT_PATH}")
