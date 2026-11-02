
import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# Load testing data

X_test = pd.read_csv("processed/X_test.csv")
y_test = pd.read_csv("processed/y_test.csv")["Loan_Status"]


# Load trained models

models = {
    "Logistic Regression": joblib.load(
        "models/logistic_regression.joblib"
    ),

    "Decision Tree": joblib.load(
        "models/decision_tree.joblib"
    ),

    "Random Forest": joblib.load(
        "models/random_forest.joblib"
    )
}


# Store model evaluation results

results = []

for name, model in models.items():

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test, y_pred, pos_label="Y"
    )

    recall = recall_score(
        y_test, y_pred, pos_label="Y"
    )

    f1 = f1_score(
        y_test, y_pred, pos_label="Y"
    )

    results.append({
        "Model": name,
        "Accuracy": round(accuracy * 100, 2),
        "Precision": round(precision * 100, 2),
        "Recall": round(recall * 100, 2),
        "F1 Score": round(f1 * 100, 2)
    })


# Create comparison table

comparison_df = pd.DataFrame(results)

print("\nMODEL PERFORMANCE COMPARISON")
print("=" * 65)

print(comparison_df.to_string(index=False))


# Save comparison results

comparison_df.to_csv(
    "processed/model_performance_comparison.csv",
    index=False
)

print("\nComparison saved successfully!")
