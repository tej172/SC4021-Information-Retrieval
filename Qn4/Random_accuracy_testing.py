
import json
import pandas as pd
import random
import ast
from sklearn.metrics import accuracy_score, classification_report, jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer

# Load and sample data for manual labeling
with open("data.json", "r") as f:
    full_data = json.load(f)

with open("evaluationDataset.json", "r") as f:
    eval_data = json.load(f)

eval_ids = set(doc["id"] for doc in eval_data)
filtered_data = [doc for doc in full_data if doc["id"] not in eval_ids]

print(f"📦 Full dataset: {len(full_data)} records")
print(f"✅ Evaluation set: {len(eval_data)} records")
print(f"🎯 Remaining after filtering: {len(filtered_data)} records")

sample_size = 150
sampled = random.sample(filtered_data, min(sample_size, len(filtered_data)))

df = pd.DataFrame([
    {
        "id": d["id"],
        "text": d["text"],
        "model_sentiment": d["polarity"],
        "model_category": d["category"],
        "human_sentiment": "",    
        "human_category": ""     
    }
    for d in sampled
])

output_path = "sample_for_sentiment_and_category_labeling.csv"
df.to_csv(output_path, index=False)
print(f"📁 Saved sample to '{output_path}' for manual labeling.")

# Evaluate accuracy after manual labels added
df = pd.read_csv("sample_filled_sentiment_and_category.csv")

df_sentiment = df[df["human_sentiment"].notnull()]
y_true_sent = df_sentiment["human_sentiment"]
y_pred_sent = df_sentiment["model_sentiment"]

report = classification_report(y_true_sent, y_pred_sent, output_dict=True)
sentiment_accuracy_table = pd.DataFrame([
    {"Class": label.capitalize(), "Prediction Accuracy": f"{report[label]['precision']:.3f}"}
    for label in ["positive", "negative", "neutral"] if label in report
])

print("\n📊 Sentiment Accuracy Table:")
print(sentiment_accuracy_table.to_string(index=False))

df["model_category"] = df["model_category"].apply(ast.literal_eval)
df["human_category"] = df["human_category"].apply(lambda x: x if isinstance(x, list) else ast.literal_eval(x) if pd.notna(x) else [])

y_true_cat = df["human_category"].tolist()
y_pred_cat = df["model_category"].tolist()

mlb = MultiLabelBinarizer()
mlb.fit(y_true_cat + y_pred_cat)

Y_true = mlb.transform(y_true_cat)
Y_pred = mlb.transform(y_pred_cat)

category_labels = mlb.classes_
jaccard_scores = jaccard_score(Y_true, Y_pred, average=None)

category_accuracy_table = pd.DataFrame({
    "Category": category_labels,
    "Prediction Accuracy (Jaccard)": jaccard_scores
}).sort_values(by="Prediction Accuracy (Jaccard)", ascending=False).reset_index(drop=True)

print("\n📊 Category Accuracy Table (Jaccard, Sorted):")
print(category_accuracy_table.to_string(index=False))
