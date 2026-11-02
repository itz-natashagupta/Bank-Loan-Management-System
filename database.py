
import sqlite3
import pandas as pd

DATABASE_NAME = "loan_applications.db"


def create_table():
    """Create the loan applications table if it does not exist."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_name TEXT NOT NULL,
            gender TEXT,
            married TEXT,
            dependents TEXT,
            education TEXT,
            self_employed TEXT,
            applicant_income REAL,
            coapplicant_income REAL,
            loan_amount REAL,
            loan_amount_term REAL,
            credit_history REAL,
            property_area TEXT,
            prediction TEXT,
            submitted_by TEXT,
            application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_application(data, prediction, username):
    """Save an applicant's details and prediction."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO applications (
            applicant_name, gender, married, dependents,
            education, self_employed, applicant_income,
            coapplicant_income, loan_amount, loan_amount_term,
            credit_history, property_area, prediction, submitted_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["Applicant_Name"],
        data["Gender"],
        data["Married"],
        data["Dependents"],
        data["Education"],
        data["Self_Employed"],
        data["ApplicantIncome"],
        data["CoapplicantIncome"],
        data["LoanAmount"],
        data["Loan_Amount_Term"],
        data["Credit_History"],
        data["Property_Area"],
        prediction,
        username
    ))

    connection.commit()
    connection.close()


def get_all_applications():
    """Retrieve all saved loan applications."""

    connection = sqlite3.connect(DATABASE_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM applications ORDER BY application_id DESC",
        connection
    )

    connection.close()
    return df
