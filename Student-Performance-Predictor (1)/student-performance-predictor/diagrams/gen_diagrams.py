"""
gen_diagrams.py
----------------
Generates the System Architecture and Process Flow diagrams as PNGs
using Graphviz. Run once to (re)produce diagrams/*.png.
"""

import graphviz

# ---------------------------------------------------------------------
# 1. System Architecture Diagram
# ---------------------------------------------------------------------
arch = graphviz.Digraph("architecture", format="png")
arch.attr(rankdir="LR", fontname="Helvetica", bgcolor="white")
arch.attr("node", fontname="Helvetica", style="filled", shape="box",
          fontsize="11")

with arch.subgraph(name="cluster_ui") as c:
    c.attr(label="Presentation Layer", style="rounded", color="#4472C4")
    c.node("CLI", "CLI Dashboard\n(app.py)", fillcolor="#DCE6F5")

with arch.subgraph(name="cluster_logic") as c:
    c.attr(label="Application / Logic Layer", style="rounded", color="#548235")
    c.node("DM", "Data Manager\n(data_manager.py)", fillcolor="#E2EFDA")
    c.node("MODEL", "ML Model\n(model.py)", fillcolor="#E2EFDA")
    c.node("VIZ", "Visualizer\n(visualizer.py)", fillcolor="#E2EFDA")

with arch.subgraph(name="cluster_data") as c:
    c.attr(label="Data Layer", style="rounded", color="#BF8F00")
    c.node("CSV", "Raw/Clean CSV\nFiles", fillcolor="#FFF2CC")
    c.node("DB", "SQLite Database\n(students.db)", fillcolor="#FFF2CC")
    c.node("PKL", "Trained Model\n(.pkl files)", fillcolor="#FFF2CC")

arch.node("OUT", "Charts & Reports\n(outputs/)", fillcolor="#FBE5D6")

arch.edge("CLI", "DM", label="requests data")
arch.edge("CLI", "MODEL", label="train / predict")
arch.edge("CLI", "VIZ", label="generate charts")
arch.edge("DM", "CSV")
arch.edge("DM", "DB")
arch.edge("MODEL", "PKL")
arch.edge("MODEL", "DM", label="reads features", style="dashed")
arch.edge("VIZ", "OUT")
arch.edge("DB", "MODEL", label="training data", style="dashed")

arch.render("diagrams/architecture_diagram", cleanup=True)

# ---------------------------------------------------------------------
# 2. Process Flow / Workflow Diagram
# ---------------------------------------------------------------------
flow = graphviz.Digraph("workflow", format="png")
flow.attr(rankdir="TB", fontname="Helvetica", bgcolor="white")
flow.attr("node", fontname="Helvetica", shape="box", style="rounded,filled",
          fillcolor="#DCE6F5", fontsize="11")

steps = [
    ("start", "Start", "ellipse", "#E2EFDA"),
    ("load", "Load / Generate\nRaw Dataset", "box", "#DCE6F5"),
    ("clean", "Clean & Validate\nData", "box", "#DCE6F5"),
    ("store", "Store in SQLite\nDatabase", "box", "#DCE6F5"),
    ("split", "Train/Test Split", "box", "#DCE6F5"),
    ("train", "Train Random Forest\nClassifier", "box", "#DCE6F5"),
    ("eval", "Evaluate Model\n(Accuracy, F1, etc.)", "box", "#DCE6F5"),
    ("decision", "Metrics\nSatisfactory?", "diamond", "#FFF2CC"),
    ("save", "Save Model +\nGenerate Charts", "box", "#DCE6F5"),
    ("predict", "User Enters New\nStudent Data", "box", "#DCE6F5"),
    ("output", "Predict Pass/Fail\n+ Confidence Score", "box", "#DCE6F5"),
    ("log", "Log Prediction\nto Database", "box", "#DCE6F5"),
    ("end", "End", "ellipse", "#E2EFDA"),
]
for key, label, shape, color in steps:
    flow.node(key, label, shape=shape, fillcolor=color)

flow.edge("start", "load")
flow.edge("load", "clean")
flow.edge("clean", "store")
flow.edge("store", "split")
flow.edge("split", "train")
flow.edge("train", "eval")
flow.edge("eval", "decision")
flow.edge("decision", "train", label="No - retune", style="dashed")
flow.edge("decision", "save", label="Yes")
flow.edge("save", "predict")
flow.edge("predict", "output")
flow.edge("output", "log")
flow.edge("log", "end")

flow.render("diagrams/workflow_diagram", cleanup=True)

print("Architecture and workflow diagrams generated in diagrams/")
