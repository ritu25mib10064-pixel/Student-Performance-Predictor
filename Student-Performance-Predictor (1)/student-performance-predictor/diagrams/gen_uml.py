"""
gen_uml.py
----------
Generates UML-style diagrams (Use Case, Class, Sequence) and the ER
diagram for the database schema, all as PNGs via Graphviz.
"""

import graphviz

# ---------------------------------------------------------------------
# 1. Use Case Diagram
# ---------------------------------------------------------------------
uc = graphviz.Digraph("usecase", format="png")
uc.attr(rankdir="LR", bgcolor="white", fontname="Helvetica")
uc.attr("node", fontname="Helvetica", fontsize="11")

uc.node("Student/User", shape="none", fontsize="13", fontname="Helvetica-Bold")
uc.node("Admin/Teacher", shape="none", fontsize="13", fontname="Helvetica-Bold")

use_cases = {
    "UC1": "Load & Prepare\nDataset",
    "UC2": "Train ML\nModel",
    "UC3": "View Evaluation\nReports/Charts",
    "UC4": "Predict Student\nOutcome",
    "UC5": "View Prediction\nHistory",
}
for key, label in use_cases.items():
    uc.node(key, label, shape="ellipse", style="filled", fillcolor="#DCE6F5",
            width="1.8", height="0.9")

uc.edge("Admin/Teacher", "UC1")
uc.edge("Admin/Teacher", "UC2")
uc.edge("Admin/Teacher", "UC3")
uc.edge("Student/User", "UC4")
uc.edge("Student/User", "UC5")
uc.edge("Admin/Teacher", "UC4", style="dashed")

uc.render("diagrams/usecase_diagram", cleanup=True)

# ---------------------------------------------------------------------
# 2. Class Diagram
# ---------------------------------------------------------------------
cls = graphviz.Digraph("classdiagram", format="png")
cls.attr(rankdir="TB", bgcolor="white", fontname="Helvetica")
cls.attr("node", shape="record", fontname="Helvetica", fontsize="10")

cls.node("DataManager", "{DataManager|"
          "+ load_or_generate_data()\\l"
          "+ clean_data(df)\\l"
          "+ save_to_database(df)\\l"
          "+ load_from_database()\\l"
          "+ log_prediction(id, result, conf)\\l"
          "+ get_prediction_history()\\l}")

cls.node("PerformanceModel", "{PerformanceModel|"
          "- scaler: StandardScaler\\l"
          "- clf: RandomForestClassifier\\l"
          "- is_trained: bool\\l|"
          "+ train(df): metrics\\l"
          "+ predict_single(features): (result, conf)\\l"
          "+ save()\\l"
          "+ load(): PerformanceModel\\l}")

cls.node("Visualizer", "{Visualizer|"
          "+ plot_class_distribution(df)\\l"
          "+ plot_feature_importance(importances)\\l"
          "+ plot_confusion_matrix(cm)\\l"
          "+ plot_correlation_heatmap(df)\\l"
          "+ generate_all_visuals(df, metrics)\\l}")

cls.node("AppCLI", "{AppCLI|"
          "- model: PerformanceModel\\l"
          "- df: DataFrame\\l|"
          "+ run()\\l}")

cls.node("Config", "{Config (module)|"
          "+ FEATURE_COLUMNS\\l"
          "+ TARGET_COLUMN\\l"
          "+ MODEL_PATH, DB_PATH, ...\\l}")

cls.edge("AppCLI", "DataManager", label="uses", arrowhead="vee")
cls.edge("AppCLI", "PerformanceModel", label="uses", arrowhead="vee")
cls.edge("AppCLI", "Visualizer", label="uses", arrowhead="vee")
cls.edge("PerformanceModel", "Config", label="reads", arrowhead="vee", style="dashed")
cls.edge("DataManager", "Config", label="reads", arrowhead="vee", style="dashed")
cls.edge("Visualizer", "Config", label="reads", arrowhead="vee", style="dashed")

cls.render("diagrams/class_diagram", cleanup=True)

# ---------------------------------------------------------------------
# 3. Sequence Diagram (Predict Outcome flow)
# ---------------------------------------------------------------------
seq = graphviz.Digraph("sequence", format="png")
seq.attr(rankdir="LR", bgcolor="white", fontname="Helvetica")
seq.attr("node", shape="box", style="filled", fillcolor="#DCE6F5", fontname="Helvetica", fontsize="10")

# lifelines as simple left-to-right ordered nodes with edges representing calls (simplified sequence)
participants = ["User", "AppCLI", "PerformanceModel", "DataManager", "SQLiteDB"]
with seq.subgraph() as s:
    s.attr(rank="same")
    for p in participants:
        seq.node(p, p, shape="box", fillcolor="#FFF2CC")

seq.edge("User", "AppCLI", label="1. Enter student features")
seq.edge("AppCLI", "PerformanceModel", label="2. predict_single(features)")
seq.edge("PerformanceModel", "PerformanceModel", label="3. scale + classify")
seq.edge("PerformanceModel", "AppCLI", label="4. return (result, confidence)")
seq.edge("AppCLI", "DataManager", label="5. log_prediction(...)")
seq.edge("DataManager", "SQLiteDB", label="6. INSERT INTO predictions")
seq.edge("AppCLI", "User", label="7. Display result")

seq.render("diagrams/sequence_diagram", cleanup=True)

# ---------------------------------------------------------------------
# 4. ER Diagram (Database Schema)
# ---------------------------------------------------------------------
er = graphviz.Digraph("erdiagram", format="png")
er.attr(rankdir="LR", bgcolor="white", fontname="Helvetica")
er.attr("node", shape="record", fontname="Helvetica", fontsize="10")

er.node("students", "{students|"
        "student_id: TEXT (PK)\\l"
        "study_hours_per_week: REAL\\l"
        "attendance_percent: REAL\\l"
        "previous_grade: REAL\\l"
        "assignments_completed_percent: REAL\\l"
        "sleep_hours: REAL\\l"
        "extracurricular_hours: REAL\\l"
        "parental_support_score: INTEGER\\l"
        "final_result: TEXT\\l}")

er.node("predictions", "{predictions|"
        "id: INTEGER (PK, AUTOINCREMENT)\\l"
        "student_id: TEXT (FK, refs students)\\l"
        "predicted_result: TEXT\\l"
        "confidence: REAL\\l"
        "predicted_at: TIMESTAMP\\l}")

er.edge("students", "predictions", label="1 .. * \n(one student can have\nmultiple predictions)", arrowhead="crow", arrowtail="tee", dir="both")

er.render("diagrams/er_diagram", cleanup=True)

print("UML and ER diagrams generated in diagrams/")
