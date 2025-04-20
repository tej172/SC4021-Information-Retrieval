from google.colab import drive
import json
import pandas as pd
import numpy as np
from pprint import pprint
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    jaccard_score,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.preprocessing import MultiLabelBinarizer

# Mount Drive
drive.mount('/content/drive')

# Load Dataset
file_path = "/content/drive/MyDrive/x_data/final_data/evaluationDataset_final.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 30)
print("Number of eval records:", len(data))
print("First record example:")
pprint(data[0])


# === QUICK COMPARISON BLOCK (Classification Report Only) ===
print("\n" + "="*40)
print("📊 Raw Classification Reports for Polarity & Subjectivity")

# Lists to collect prediction vs gold for each annotator
y_true_pol_annotator1, y_true_subj_annotator1 = [], []
y_true_pol_annotator2, y_true_subj_annotator2 = [], []
y_pred_pol, y_pred_subj = [], []

for item in data:
    pred_pol = item.get("polarity", "").lower()
    pred_subj = item.get("subjectivity", "").lower()

    manual_labels = item.get("manual_labels", {})
    ann1 = manual_labels.get("annotator1", {})
    ann2 = manual_labels.get("annotator2", {})

    y_pred_pol.append(pred_pol)
    y_pred_subj.append(pred_subj)

    y_true_pol_annotator1.append(ann1.get("polarity", "").lower())
    y_true_subj_annotator1.append(ann1.get("subjectivity", "").lower())
    y_true_pol_annotator2.append(ann2.get("polarity", "").lower())
    y_true_subj_annotator2.append(ann2.get("subjectivity", "").lower())

# Collect all classes from both sides
label_set_pol = sorted(set(y_pred_pol + y_true_pol_annotator1 + y_true_pol_annotator2))
label_set_subj = sorted(set(y_pred_subj + y_true_subj_annotator1 + y_true_subj_annotator2))

print("="*20)
print("Polarity vs Annotator 1")
print(classification_report(y_true_pol_annotator1, y_pred_pol, labels=label_set_pol, zero_division=0))
print("Polarity vs Annotator 2")
print(classification_report(y_true_pol_annotator2, y_pred_pol, labels=label_set_pol, zero_division=0))

print("="*20)
print("Subjectivity vs Annotator 1")
print(classification_report(y_true_subj_annotator1, y_pred_subj, labels=label_set_subj, zero_division=0))
print("Subjectivity vs Annotator 2")
print(classification_report(y_true_subj_annotator2, y_pred_subj, labels=label_set_subj, zero_division=0))


# === DETAILED EVALUATION FOR ANNOTATORS 1 AND 2 ===
def evaluate_annotator(data, annotator_key="annotator1"):
    print(f"\n{'='*40}\n📊 EVALUATION USING {annotator_key.upper()}")

    # Build DataFrame
    df = pd.DataFrame([
        {
            "id": d["id"],
            "text": d["text"],
            "model_polarity": d["polarity"],
            "model_subjectivity": d["subjectivity"],
            "model_category": d["category"],
            "true_polarity": d.get("manual_labels", {}).get(annotator_key, {}).get("polarity", "").lower(),
            "true_subjectivity": d.get("manual_labels", {}).get(annotator_key, {}).get("subjectivity", "").lower(),
            "true_category": d.get("manual_labels", {}).get(annotator_key, {}).get("category", [])
        }
        for d in data
    ])

    # =============== POLARITY ===================
    print("\n📊 Polarity Evaluation")
    y_true_pol = df["true_polarity"]
    y_pred_pol = df["model_polarity"]

    report_pol = classification_report(y_true_pol, y_pred_pol, output_dict=True)
    table_pol = pd.DataFrame([
        {"Class": label.capitalize(), "Precision": f"{report_pol[label]['precision']:.3f}",
         "Recall": f"{report_pol[label]['recall']:.3f}", "F1-Score": f"{report_pol[label]['f1-score']:.3f}"}
        for label in ["positive", "neutral", "negative"] if label in report_pol
    ])
    print(table_pol.to_string(index=False))

    overall_pol = pd.DataFrame({
        "Metric": ["Precision", "Recall", "F1-Score", "Accuracy"],
        "Score": [
            f"{precision_score(y_true_pol, y_pred_pol, average='weighted', zero_division=0):.3f}",
            f"{recall_score(y_true_pol, y_pred_pol, average='weighted', zero_division=0):.3f}",
            f"{f1_score(y_true_pol, y_pred_pol, average='weighted', zero_division=0):.3f}",
            f"{accuracy_score(y_true_pol, y_pred_pol):.3f}"
        ]
    })
    print("\n🔢 Overall Polarity Metrics:")
    print(overall_pol.to_string(index=False))

    # =============== SUBJECTIVITY ===================
    print("\n📊 Subjectivity Evaluation")
    y_true_subj = df["true_subjectivity"]
    y_pred_subj = df["model_subjectivity"]

    report_subj = classification_report(y_true_subj, y_pred_subj, output_dict=True)
    table_subj = pd.DataFrame([
        {"Class": label.capitalize(), "Precision": f"{report_subj[label]['precision']:.3f}",
         "Recall": f"{report_subj[label]['recall']:.3f}", "F1-Score": f"{report_subj[label]['f1-score']:.3f}"}
        for label in ["neutral", "opinionated"] if label in report_subj
    ])
    print(table_subj.to_string(index=False))

    overall_subj = pd.DataFrame({
        "Metric": ["Precision", "Recall", "F1-Score", "Accuracy"],
        "Score": [
            f"{precision_score(y_true_subj, y_pred_subj, average='weighted', zero_division=0):.3f}",
            f"{recall_score(y_true_subj, y_pred_subj, average='weighted', zero_division=0):.3f}",
            f"{f1_score(y_true_subj, y_pred_subj, average='weighted', zero_division=0):.3f}",
            f"{accuracy_score(y_true_subj, y_pred_subj):.3f}"
        ]
    })
    print("\n🔢 Overall Subjectivity Metrics:")
    print(overall_subj.to_string(index=False))

    # =============== CATEGORY MULTILABEL EVAL ===================
    print("\n📊 Category Evaluation (Multi-label Jaccard)")

    # Clean inputs
    df["model_category"] = df["model_category"].apply(lambda x: x if isinstance(x, list) else [])
    df["true_category"] = df["true_category"].apply(lambda x: x if isinstance(x, list) else [])

    y_pred_cat = df["model_category"].tolist()
    y_true_cat = df["true_category"].tolist()

    mlb = MultiLabelBinarizer()
    mlb.fit(y_pred_cat + y_true_cat)

    Y_true = mlb.transform(y_true_cat)
    Y_pred = mlb.transform(y_pred_cat)

    jaccard_scores = jaccard_score(Y_true, Y_pred, average=None)
    category_labels = mlb.classes_

    category_accuracy_table = pd.DataFrame({
        "Category": category_labels,
        "Prediction Accuracy (Jaccard)": jaccard_scores
    }).sort_values(by="Prediction Accuracy (Jaccard)", ascending=False).reset_index(drop=True)

    print(category_accuracy_table.to_string(index=False))

    overall_jaccard = jaccard_score(Y_true, Y_pred, average="samples")
    print(f"\n📈 Overall Sample-wise Jaccard Score: {overall_jaccard:.3f}")

# Run evaluations
evaluate_annotator(data, annotator_key="annotator1")
evaluate_annotator(data, annotator_key="annotator2")
