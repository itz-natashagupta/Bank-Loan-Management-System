import pandas as pd
import joblib

from sklearn.metrics import (confusion_matrix, classification_report,
                             accuracy_score)

X_test = pd.read_csv("processed/X_test.csv")
y_test = pd.read_csv("processed/y_test.csv")["Loan_Status"]

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

for name, model in models.items():

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    # Predictions
    y_pred = model.predict(X_test)

    # Accuracy
    print("\nAccuracy:",
          round(accuracy_score(y_test, y_pred) * 100, 2), "%")

    # Confusion Matrix
    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=["N", "Y"]
    )

    print("\nConfusion Matrix:")
    print(cm)

print("\nClassification Report:")

print(classification_report(
        y_test,
        y_pred,
        labels=["N", "Y"],
        target_names=["Rejected (N)", "Approved (Y)"],
        zero_division=0
    ))