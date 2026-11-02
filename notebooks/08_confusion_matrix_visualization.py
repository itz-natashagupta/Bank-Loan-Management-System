import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix

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

    y_pred = model.predict(X_test)

    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=["N", "Y"]
    )

    plt.figure(figsize=(6, 4))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Rejected (N)", "Approved (Y)"],
        yticklabels=["Rejected (N)", "Approved (Y)"]
    )

    plt.title(name + " - Confusion Matrix")

    plt.xlabel("Predicted Status")

    plt.ylabel("Actual Status")

    plt.tight_layout()

    plt.savefig(
        "processed/" + name.replace(" ", "_") + "_confusion_matrix.png"
    )

    plt.show()

print("\nAll confusion matrices generated successfully!")