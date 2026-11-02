
import joblib
import os

# Load the selected model

final_model = joblib.load(
    "models/logistic_regression.joblib"
)

# Save as the final selected model

os.makedirs("models", exist_ok=True)

joblib.dump(
    final_model,
    "models/final_loan_prediction_model.joblib"
)

print("Final model selected: Logistic Regression")

print("Final model saved successfully!")

print("Model location: models/final_loan_prediction_model.joblib")
