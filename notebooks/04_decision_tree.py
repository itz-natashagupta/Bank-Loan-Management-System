import pandas as pd
import os
import joblib

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X_train = pd.read_csv("processed/X_train.csv")
X_test = pd.read_csv("processed/X_test.csv")

y_train = pd.read_csv("processed/y_train.csv")["Loan_Status"]
y_test = pd.read_csv("processed/y_test.csv")["Loan_Status"]

model = DecisionTreeClassifier(
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("DECISION TREE RESULTS")

print("\nModel Training Completed Successfully!")

print("Training Records:", len(X_train))
print("Testing Records:", len(X_test))

print("Model Accuracy:", accuracy * 100, "%")

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/decision_tree.joblib"
)

print("\nDecision Tree Model saved successfully!")