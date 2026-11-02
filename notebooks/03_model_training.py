import pandas as pd
import os
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X_train = pd.read_csv("processed/X_train.csv")
X_test = pd.read_csv("processed/X_test.csv")

y_train = pd.read_csv("processed/y_train.csv")['Loan_Status']
y_test = pd.read_csv("processed/y_test.csv")['Loan_Status']

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("LOGISTIC REGRESSION RESULTS")

print("\nModel Training completed Successfully!")

print("Training records: ", len(X_train))
print("Testing Records: ", len(X_test))

print("Model Accuracy:", accuracy * 100, "%")

os.makedirs("models", exist_ok=True)

joblib.dump( model, "models/logistic_regression.joblib")

print("\nModel saved successfully!")