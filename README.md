# Bank Loan Management System

A machine learning-based Bank Loan Management System that predicts loan
eligibility from applicant details and provides a simple interface for
submitting and reviewing loan applications.

## Project Overview

This project demonstrates how machine learning can support an initial
loan-eligibility assessment. Applicants enter their personal and
financial details through a Streamlit web application. A trained machine
learning model processes the details and predicts whether the
application is likely to be approved or rejected.

The application also stores submitted applications in an SQLite database
and provides role-based views for employees and administrators.

> **Disclaimer:** This is an academic demonstration project, not a real
> banking or credit-decision system. Its predictions should not be used
> to make actual lending decisions.

## Problem Statement

Manual loan-eligibility assessment can involve repetitive review of
applicant information. This project builds a prototype that uses machine
learning to analyse applicant details and generate a preliminary
eligibility prediction, while maintaining application records for
review.

## Key Features

-   **Login system:** Separate Employee and Admin roles.
-   **Loan prediction:** Enter applicant details and receive an
    eligibility prediction.
-   **Application storage:** Save submitted applications in an SQLite
    database.
-   **Application history:** View, search, and filter previously
    submitted applications.
-   **CSV export:** Download application-history records.
-   **Model performance page:** Compare the trained machine learning
    models.
-   **Dashboard:** View application summaries and recent activity.

## Technologies Used

-   **Programming language:** Python
-   **Web application:** Streamlit
-   **Machine learning:** Scikit-learn
-   **Data processing:** Pandas
-   **Model storage:** Joblib
-   **Database:** SQLite
-   **Visualisation:** Streamlit charts / supported plotting libraries

## Machine Learning

The project trains and compares three classification algorithms:

1.  Logistic Regression
2.  Decision Tree
3.  Random Forest

Logistic Regression was selected as the final model based on the
evaluation results.

### Model comparison

  Model                   Accuracy   Precision   Recall   F1-score
  --------------------- ---------- ----------- -------- ----------
  Logistic Regression       80.49%      80.20%   95.29%     87.10%
  Decision Tree             78.05%      88.16%   78.82%     83.23%
  Random Forest             80.49%      81.44%   92.94%     86.81%

These scores reflect evaluation on the project's test split. They are
not a guarantee of real-world performance.

### Input features

The prediction model uses the following applicant features:

-   Gender
-   Marital status
-   Number of dependents
-   Education
-   Self-employment status
-   Applicant income
-   Co-applicant income
-   Loan amount
-   Loan amount term
-   Credit history
-   Property area

`Loan_ID` is excluded from model training because it is an identifier
rather than an applicant feature.

## Project Structure

``` text
Loan_Prediction_System/
│
├── app.py
├── database.py
├── requirements.txt
├── train.csv
├── test.csv
│
├── models/
│   ├── logistic_regression.joblib
│   ├── decision_tree.joblib
│   ├── random_forest.joblib
│   └── final_loan_prediction_model.joblib
│
├── processed/
│   ├── preprocessor.joblib
│   ├── X_train.csv
│   ├── X_test.csv
│   ├── y_train.csv
│   ├── y_test.csv
│   └── model_performance_comparison.csv
│
└── notebooks/
    ├── 01_eda.py
    ├── 02_preprocessing.py
    └── ...
```

The SQLite database file (`loan_applications.db`) is created
automatically when the application runs. It is intentionally excluded
from the repository because it stores submitted application records.

## Installation and Setup

### 1. Clone the repository

``` bash
git clone https://github.com/<your-github-username>/Bank-Loan-Management-System.git
cd Bank-Loan-Management-System
```

Replace `<your-github-username>` with your GitHub username.

### 2. Create and activate a virtual environment (recommended)

**Windows:**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Run the application

``` bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in
your browser.

## Demo Login

The application includes demo accounts configured in `app.py`:

  Role       Username      Password
  ---------- ------------- -------------
  Employee   `employee1`   `Bank@123`
  Admin      `admin`       `Admin@123`

These are **public demonstration credentials only**. Anyone with access
to the source code can see them. Do not use these credentials, or this
authentication approach, for a real application or deployment.

## Database

The application uses SQLite to store submitted applications. The
database table includes applicant details, the model prediction, the
submitting username, and the application timestamp.

A local database file is generated automatically when the app starts.
Each user's local database is separate unless a shared database service
is configured.

## Notes

-   Keep the trained model files and preprocessing file in the `models/`
    and `processed/` directories as expected by the application.
-   Keep `requirements.txt` updated when project dependencies change.
-   Do not commit private applicant data, local database files, API
    keys, or other secrets.
-   The model's prediction is an estimate based on the dataset and
    training process. It does not replace a bank's verification, policy
    checks, or human review.

## Future Scope

-   Add stronger authentication and secure password management.
-   Add applicant document upload and verification.
-   Improve model evaluation using additional data and validation
    methods.
-   Add explainability to show which factors influenced a prediction.
-   Deploy the application with secure database hosting and access
    controls.

## Contributors

Add the names of your project team members here.

## License

No license has been selected for this repository yet. Add a license if
you want to specify how others may use, modify, and distribute the
project.
