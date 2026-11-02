import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("train.csv")

print("First 5 rows of the dataset:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nShape of the dataset:", df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nSummary Statistics:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())

print("\nPercentage of missing values:")
print(df.isnull().sum()/len(df) * 100)

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nLoan status distribution:")
print(df['Loan_Status'].value_counts())

print("\nLoan status distribution (percentage):")
print(df['Loan_Status'].value_counts(normalize=True) * 100 )

# Graph 1: Loan Status Distribution

plt.figure(figsize=(6, 4))

sns.countplot(data=df, x="Loan_Status")

plt.title("Loan Approval Distribution")
plt.xlabel("Loan Status")
plt.ylabel("Number of Applicants")

plt.show()

# Graph 2: Applicant Income Distribution

plt.figure(figsize=(7, 4))

sns.histplot(data=df, x="ApplicantIncome", bins=30, kde=True)

plt.title("Applicant Income Distribution")
plt.xlabel("Applicant Income")
plt.ylabel("Frequency")

plt.show()

# Graph 3: Loan Amount Distribution

plt.figure(figsize=(7, 4))

sns.histplot(data=df, x="LoanAmount", bins=30, kde=True)

plt.title("Loan Amount Distribution")
plt.xlabel("Loan Amount")
plt.ylabel("Frequency")

plt.show()

# Graph 4: Credit History vs Loan Status

plt.figure(figsize=(7, 4))

sns.countplot(data=df, x="Credit_History", hue="Loan_Status")

plt.title("Credit History vs Loan Approval")
plt.xlabel("Credit History")
plt.ylabel("Number of Applicants")

plt.show()

# Graph 5: Education vs Loan Status

plt.figure(figsize=(7, 4))

sns.countplot(data=df, x="Education", hue="Loan_Status")

plt.title("Education vs Loan Approval")
plt.xlabel("Education")
plt.ylabel("Number of Applicants")

plt.show()

# Graph 6: Property Area vs Loan Status

plt.figure(figsize=(7, 4))

sns.countplot(data=df, x="Property_Area", hue="Loan_Status")

plt.title("Property Area vs Loan Approval")
plt.xlabel("Property Area")
plt.ylabel("Number of Applicants")

plt.show()

# Credit History vs Approval Rate

print("\nCredit History Approval Rate:")
print(pd.crosstab(
    df["Credit_History"],
    df["Loan_Status"],
    normalize="index"
) * 100)


# Education vs Approval Rate

print("\nEducation Approval Rate:")
print(pd.crosstab(
    df["Education"],
    df["Loan_Status"],
    normalize="index"
) * 100)


# Property Area vs Approval Rate

print("\nProperty Area Approval Rate:")
print(pd.crosstab(
    df["Property_Area"],
    df["Loan_Status"],
    normalize="index"
) * 100)