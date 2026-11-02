import pandas as pd
import joblib

from sklearn.metrics import accuracy_score

X_train = pd.read_csv("processed/X_train.csv")
X_test = pd.read_csv("processed/X_test.csv")

y_train = pd.read_csv("processed/y_train.csv")["Loan_Status"]
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


results = []

for name, model in models.items():

    # Training predictions
    train_pred = model.predict(X_train)

    # Testing predictions
    test_pred = model.predict(X_test)

    # Calculate accuracy
    train_accuracy = accuracy_score(y_train, train_pred)
    test_accuracy = accuracy_score(y_test, test_pred)

    results.append({
        "Model": name,
        "Training Accuracy": round(train_accuracy * 100, 2),
        "Testing Accuracy": round(test_accuracy * 100, 2)
    })

comparison = pd.DataFrame(results)

comparison = comparison.sort_values(
    by="Testing Accuracy",
    ascending=False
)


print("\nMACHINE LEARNING MODEL COMPARISON")

print(comparison.to_string(index=False))

comparison.to_csv(
    "processed/model_comparison.csv",
    index=False
)

print("\nComparison results saved successfully!")