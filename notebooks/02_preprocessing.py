import os
import joblib
import pandas as pd

df = pd.read_csv("train.csv")

df = df.drop("Loan_ID", axis=1)

X = df.drop("Loan_Status", axis=1)

y = df["Loan_Status"]

print("Input Features:")
print(X.head())

print("\nTarget Variable:")
print(y.head())

print("\nInput Shape:", X.shape)
print("Target Shape:", y.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2, stratify= y)

print("\nTraining and Testing data.")

print("X_train: ",X_train.shape)
print("X_test: ",X_test.shape)

print("y_train: ",y_train.shape)
print("y_test: ",y_test.shape)

import numpy as np
from sklearn.impute import SimpleImputer

numeric_columns = X_train.select_dtypes(
    include=np.number
).columns

categorical_columns = X_train.select_dtypes(
    include="object"
).columns

imputer1 = SimpleImputer(strategy="median")
imputer2 = SimpleImputer(strategy="most_frequent")

X_train[numeric_columns] = imputer1.fit_transform(
    X_train[numeric_columns]
)

X_test[numeric_columns] = imputer1.transform(
    X_test[numeric_columns]
)

X_train[categorical_columns] = imputer2.fit_transform(
    X_train[categorical_columns]
)

X_test[categorical_columns] = imputer2.transform(
    X_test[categorical_columns]
)

print("\nMissing Values After Imputation:")

print("Training Data:")
print(X_train.isnull().sum())

print("\nTesting Data:")
print(X_test.isnull().sum())

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_columns),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
    ],
    remainder='passthrough',
    sparse_threshold=0
)

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

feature_names = preprocessor.get_feature_names_out()

X_train_processed = pd.DataFrame(
    X_train_processed,
    columns=feature_names
)

X_test_processed = pd.DataFrame(
    X_test_processed,
    columns=feature_names
)

print("\nProcessed Training Data:")
print(X_train_processed.head())

print("\nProcessed Testing Data:")
print(X_test_processed.head())

print("\nProcessed Training Shape:", X_train_processed.shape)
print("Processed Testing Shape:", X_test_processed.shape)

print("\nFinal Dataset Information")

print("Training Data Shape:", X_train_processed.shape)
print("Testing Data Shape:", X_test_processed.shape)

print("\nAll values numerical:",
      X_train_processed.select_dtypes(exclude=np.number).empty)

# Create folders to save processed data
os.makedirs("processed", exist_ok=True)

# Save processed datasets
X_train_processed.to_csv(
    "processed/X_train.csv", index=False
)

X_test_processed.to_csv(
    "processed/X_test.csv", index=False
)

y_train.to_frame(name="Loan_Status").to_csv(
    "processed/y_train.csv", index=False
)

y_test.to_frame(name="Loan_Status").to_csv(
    "processed/y_test.csv", index=False
)

# Save fitted preprocessing pipeline
joblib.dump(
    preprocessor,
    "processed/preprocessor.joblib"
)

print("\nProcessed datasets and preprocessor saved successfully!")