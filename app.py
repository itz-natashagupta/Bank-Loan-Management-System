
from database import create_table, save_application, get_all_applications
import streamlit as st
import pandas as pd
import joblib

# Ensure database and table are created at startup
create_table()


# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Bank Loan Management System",
    page_icon="🏦",
    layout="wide"
)


# ----------------------------------
# DEMO USER ACCOUNTS
# ----------------------------------

USERS = {
    "employee1": {
        "password": "Bank@123",
        "role": "Employee"
    },
    "admin": {
        "password": "Admin@123",
        "role": "Admin"
    }
}


# ----------------------------------
# SESSION STATE
# ----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


# ----------------------------------
# LOAD MODEL AND PREPROCESSOR
# ----------------------------------

@st.cache_resource
def load_model():

    model = joblib.load(
        "models/final_loan_prediction_model.joblib"
    )

    preprocessor = joblib.load(
        "processed/preprocessor.joblib"
    )

    return model, preprocessor


model, preprocessor = load_model()


# ----------------------------------
# LOGIN PAGE
# ----------------------------------


def login_page():

    # Custom login page styling

    st.markdown("""
        <style>

        .stApp {
            background-color: #F4F7FB;
        }

        .login-heading {
            text-align: center;
            color: #142D4E;
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .login-subheading {
            text-align: center;
            color: #64748B;
            font-size: 16px;
            margin-bottom: 30px;
        }

        .login-footer {
            text-align: center;
            color: #94A3B8;
            font-size: 12px;
            margin-top: 30px;
        }

        </style>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.markdown(
        '<div class="login-heading">🏦 BANK LOAN MANAGEMENT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subheading">'
        'Employee Login Portal | Secure Access'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 1.3, 1])

    with col2:

        with st.container(border=True):

            st.subheader("Welcome Back")

            st.caption(
                "Sign in with your employee credentials "
                "to access the banking system."
            )

            st.write("")

            with st.form("login_form"):

                username = st.text_input(
                    "Employee Username",
                    placeholder="Enter your username"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                st.write("")

                login_button = st.form_submit_button(
                    "Sign In",
                    use_container_width=True
                )

            if login_button:

                if username in USERS and USERS[username]["password"] == password:

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = USERS[username]["role"]

                    st.success("Login successful!")

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

    st.markdown(
        '<div class="login-footer">'
        'Bank Loan Management System | AIML Project'
        '</div>',
        unsafe_allow_html=True
    )



# ----------------------------------
# MAIN APPLICATION
# ----------------------------------

def main_application():

    st.sidebar.title("🏦 Bank Management")

    st.sidebar.write(
        f"Welcome, {st.session_state.username}"
    )

    st.sidebar.caption(
        f"Role: {st.session_state.role}"
    )

    # Navigation based on role

    if st.session_state.role == "Admin":

        pages = [
            "Dashboard",
            "Loan Prediction",
            "Application History",
            "Model Performance"
        ]

    else:

        pages = [
            "Dashboard",
            "Loan Prediction",
            "Application History"
        ]

    
    # Initialize navigation state
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Dashboard"

    # Handle navigation from dashboard quick actions
    requested_page = st.session_state.get("dashboard_action")

    if requested_page in pages:
        st.session_state.selected_page = requested_page

    # Clear the temporary navigation request
    st.session_state.dashboard_action = None

    # Sidebar navigation
    page = st.sidebar.radio(
        "Navigation",
        pages,
        key="selected_page"
    )


    st.sidebar.markdown("---")

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()



   
    # ----------------------------------
    # DASHBOARD
    # ----------------------------------

    
    # ----------------------------------
    # PROFESSIONAL BANK DASHBOARD
    # ----------------------------------

    if page == "Dashboard":

        # Dashboard styling

        st.markdown("""
            <style>

            .dashboard-heading {
                color: #142D4E;
                font-size: 32px;
                font-weight: 700;
            }

            .dashboard-subtitle {
                color: #64748B;
                font-size: 15px;
            }

            </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="dashboard-heading">'
            'Bank Overview</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-subtitle">'
            'Monitor and manage loan applications efficiently.'
            '</div>',
            unsafe_allow_html=True
        )

        st.write("")

        # Retrieve applications

        applications = get_all_applications()

        total_applications = len(applications)

        if total_applications > 0:

            approved = (
                applications["prediction"] == "Approved"
            ).sum()

            rejected = (
                applications["prediction"] == "Rejected"
            ).sum()

            approval_rate = (
                approved / total_applications
            ) * 100

        else:

            approved = 0
            rejected = 0
            approval_rate = 0

        # ----------------------------------
        # METRIC CARDS
        # ----------------------------------

        st.subheader("Application Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Applications",
            total_applications
        )

        col2.metric(
            "Approved",
            int(approved),
            delta="Successful predictions"
        )

        col3.metric(
            "Rejected",
            int(rejected),
            delta="Unsuccessful predictions"
        )

        col4.metric(
            "Approval Rate",
            f"{approval_rate:.1f}%"
        )

        st.markdown("---")

        # ----------------------------------
        # APPLICATION ANALYTICS
        # ----------------------------------

        st.subheader("Application Analytics")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            st.markdown("**Loan Status Distribution**")

            if total_applications > 0:

                status_counts = pd.Series({
                    "Approved": approved,
                    "Rejected": rejected
                })

                st.bar_chart(status_counts)

            else:

                st.info("No application data available.")

        with chart_col2:

            st.markdown("**Approval Overview**")

            if total_applications > 0:

                chart_data = pd.DataFrame({
                    "Status": ["Approved", "Rejected"],
                    "Applications": [
                        approved,
                        rejected
                    ]
                })

                st.bar_chart(
                    chart_data.set_index("Status")
                )

            else:

                st.info("Submit applications to view analytics.")

        st.markdown("---")

        # ----------------------------------
        # RECENT APPLICATIONS
        # ----------------------------------

        st.subheader("Recent Applications")

        if total_applications > 0:

            recent_applications = applications.head(5)

            recent_data = recent_applications[[
                "application_id",
                "applicant_name",
                "prediction",
                "submitted_by",
                "application_date"
            ]].copy()

            recent_data.columns = [
                "Application ID",
                "Applicant Name",
                "Loan Status",
                "Processed By",
                "Application Date"
            ]

            st.dataframe(
                recent_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No applications have been submitted yet."
            )

        st.markdown("---")

        # ----------------------------------
        # QUICK ACTIONS
        # ----------------------------------

        st.subheader("Quick Actions")

        action_col1, action_col2 = st.columns(2)

        with action_col1:

            if st.button(
                "Process New Loan Application",
                use_container_width=True
            ):

                st.session_state.dashboard_action = "Loan Prediction"
                st.rerun()

        with action_col2:

            if st.button(
                "View All Applications",
                use_container_width=True
            ):

                st.session_state.dashboard_action = "Application History"
                st.rerun()

        st.caption(
            "Bank Loan Management System | AIML Project"
        )



    # ----------------------------------
    # LOAN PREDICTION
    # ----------------------------------

    
    elif page == "Loan Prediction":

        st.markdown("""
            <style>
            .loan-heading {
                color: #142D4E;
                font-size: 32px;
                font-weight: 700;
            }
            .loan-subtitle {
                color: #64748B;
                font-size: 15px;
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="loan-heading">Loan Application Processing</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="loan-subtitle">'
            'Enter applicant details to evaluate loan eligibility '
            'using the machine learning model.'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            "Please ensure that all applicant information is accurate "
            "before submitting the application."
        )

        with st.form("loan_prediction_form"):

            # PERSONAL INFORMATION
            st.subheader("1. Personal Information")
            st.caption("Basic details of the loan applicant")

            applicant_name = st.text_input(
                "Applicant Full Name",
                placeholder="Enter applicant's full name"
            )

            col1, col2 = st.columns(2)

            with col1:
                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female"]
                )

                married = st.selectbox(
                    "Marital Status",
                    ["Yes", "No"]
                )

                dependents = st.selectbox(
                    "Number of Dependents",
                    ["0", "1", "2", "3+"]
                )

            with col2:
                education = st.selectbox(
                    "Education",
                    ["Graduate", "Not Graduate"]
                )

                self_employed = st.selectbox(
                    "Self Employed",
                    ["Yes", "No"]
                )

            st.markdown("---")

            # FINANCIAL INFORMATION
            st.subheader("2. Financial Information")
            st.caption("Income and requested loan details")

            col3, col4 = st.columns(2)

            with col3:
                applicant_income = st.number_input(
                    "Applicant Income",
                    min_value=0,
                    value=5000,
                    help="Enter monthly applicant income."
                )

                coapplicant_income = st.number_input(
                    "Coapplicant Income",
                    min_value=0,
                    value=0,
                    help="Enter monthly coapplicant income."
                )

                loan_amount = st.number_input(
                    "Loan Amount (in thousands)",
                    min_value=1,
                    value=120
                )

            with col4:
                loan_term = st.selectbox(
                    "Loan Amount Term (months)",
                    [360, 180, 120, 240, 60, 300, 480]
                )

                credit_history = st.selectbox(
                    "Credit History",
                    [1.0, 0.0],
                    format_func=lambda x:
                    "Good (1)" if x == 1.0
                    else "Poor (0)"
                )

                property_area = st.selectbox(
                    "Property Area",
                    ["Urban", "Rural", "Semiurban"]
                )

            st.markdown("---")

            submit = st.form_submit_button(
                "Predict Loan Status",
                use_container_width=True,
                type="primary"
            )

        # PREDICTION PROCESSING
        if submit:

            if not applicant_name.strip():

                st.warning(
                    "Please enter the applicant's full name."
                )

            else:

                applicant_data = pd.DataFrame([{
                    "Gender": gender,
                    "Married": married,
                    "Dependents": dependents,
                    "Education": education,
                    "Self_Employed": self_employed,
                    "ApplicantIncome": applicant_income,
                    "CoapplicantIncome": coapplicant_income,
                    "LoanAmount": loan_amount,
                    "Loan_Amount_Term": loan_term,
                    "Credit_History": credit_history,
                    "Property_Area": property_area
                }])

                # Apply saved preprocessing
                processed_data = preprocessor.transform(
                    applicant_data
                )

                # Generate prediction
                prediction = model.predict(
                    processed_data
                )[0]

                probabilities = model.predict_proba(
                    processed_data
                )[0]

                classes = model.classes_

                probability_dict = dict(
                    zip(classes, probabilities)
                )

                approval_probability = (
                    probability_dict.get("Y", 0) * 100
                )

                rejection_probability = (
                    probability_dict.get("N", 0) * 100
                )

                # Convert prediction into readable result
                result = (
                    "Approved" if prediction == "Y"
                    else "Rejected"
                )

                # Prepare application details
                application_details = {
                    "Applicant_Name": applicant_name.strip(),
                    "Gender": gender,
                    "Married": married,
                    "Dependents": dependents,
                    "Education": education,
                    "Self_Employed": self_employed,
                    "ApplicantIncome": applicant_income,
                    "CoapplicantIncome": coapplicant_income,
                    "LoanAmount": loan_amount,
                    "Loan_Amount_Term": loan_term,
                    "Credit_History": credit_history,
                    "Property_Area": property_area
                }

                # Save application in SQLite
                save_application(
                    application_details,
                    result,
                    st.session_state.username
                )

                # DISPLAY RESULT
                st.markdown("---")
                st.subheader("3. Loan Prediction Result")

                if prediction == "Y":
                    st.success(
                        "Loan Eligibility Prediction: APPROVED"
                    )
                else:
                    st.error(
                        "Loan Eligibility Prediction: REJECTED"
                    )

                col1, col2 = st.columns(2)

                col1.metric(
                    "Approval Probability",
                    f"{approval_probability:.2f}%"
                )

                col2.metric(
                    "Rejection Probability",
                    f"{rejection_probability:.2f}%"
                )

                st.markdown("**Prediction Confidence Overview**")

                probability_data = pd.DataFrame({
                    "Probability": [
                        approval_probability,
                        rejection_probability
                    ]
                }, index=["Approval", "Rejection"])

                st.bar_chart(
                    probability_data,
                    horizontal=True
                )

                st.success(
                    "Application saved successfully!"
                )

                st.caption(
                    "This is an ML-generated prediction, not a "
                    "final bank lending decision. Probabilities "
                    "are model estimates, not guaranteed outcomes."
                )


    # ----------------------------------
    # APPLICATION HISTORY
    # ----------------------------------

    
    elif page == "Application History":

        st.markdown("""
            <style>
            .history-heading {
                color: #142D4E;
                font-size: 32px;
                font-weight: 700;
            }
            .history-subtitle {
                color: #64748B;
                font-size: 15px;
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="history-heading">Application History</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="history-subtitle">'
            'Track, search and manage previously processed loan applications.'
            '</div>',
            unsafe_allow_html=True
        )

        # Retrieve applications
        applications = get_all_applications()

        if applications.empty:

            st.info(
                "No loan applications have been submitted yet."
            )

        else:

            # APPLICATION SUMMARY
            total_applications = len(applications)

            approved_applications = (
                applications["prediction"] == "Approved"
            ).sum()

            rejected_applications = (
                applications["prediction"] == "Rejected"
            ).sum()

            st.subheader("Application Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Applications",
                total_applications
            )

            col2.metric(
                "Approved",
                int(approved_applications)
            )

            col3.metric(
                "Rejected",
                int(rejected_applications)
            )

            st.markdown("---")

            # SEARCH AND FILTER
            st.subheader("Search and Filter Applications")

            col1, col2 = st.columns(2)

            with col1:

                search_query = st.text_input(
                    "Search Applicant",
                    placeholder="Enter applicant name or application ID"
                )

            with col2:

                status_filter = st.selectbox(
                    "Filter by Loan Status",
                    ["All", "Approved", "Rejected"]
                )

            filtered_data = applications.copy()

            if search_query.strip():

                search_query = search_query.strip()

                filtered_data = filtered_data[
                    filtered_data["applicant_name"].str.contains(
                        search_query,
                        case=False,
                        na=False
                    )
                    |
                    filtered_data["application_id"].astype(
                        str
                    ).str.contains(
                        search_query,
                        na=False
                    )
                ]

            if status_filter != "All":

                filtered_data = filtered_data[
                    filtered_data["prediction"] == status_filter
                ]

            st.markdown("---")

            # APPLICATION RECORDS
            st.subheader("Submitted Applications")

            st.caption(
                f"Showing {len(filtered_data)} of "
                f"{total_applications} applications"
            )

            if not filtered_data.empty:

                display_data = filtered_data[[
                    "application_id",
                    "applicant_name",
                    "prediction",
                    "applicant_income",
                    "loan_amount",
                    "submitted_by",
                    "application_date"
                ]].copy()

                display_data.columns = [
                    "Application ID",
                    "Applicant Name",
                    "Loan Status",
                    "Applicant Income",
                    "Loan Amount",
                    "Processed By",
                    "Application Date"
                ]

                st.dataframe(
                    display_data,
                    use_container_width=True,
                    hide_index=True
                )

                # DOWNLOAD REPORT
                csv_data = filtered_data.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="Download Applications Report",
                    data=csv_data,
                    file_name="loan_applications_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.markdown("---")

                # INDIVIDUAL APPLICATION DETAILS
                st.subheader("Individual Application Details")

                selected_id = st.selectbox(
                    "Select Application ID",
                    filtered_data["application_id"].tolist(),
                    format_func=lambda x:
                    f"Application #{x}"
                )

                selected_application = filtered_data[
                    filtered_data["application_id"] == selected_id
                ].iloc[0]

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown("**Applicant Information**")

                    st.write(
                        f"**Name:** {selected_application['applicant_name']}"
                    )

                    st.write(
                        f"**Gender:** {selected_application['gender']}"
                    )

                    st.write(
                        f"**Marital Status:** {selected_application['married']}"
                    )

                    st.write(
                        f"**Dependents:** {selected_application['dependents']}"
                    )

                    st.write(
                        f"**Education:** {selected_application['education']}"
                    )

                    st.write(
                        f"**Self Employed:** {selected_application['self_employed']}"
                    )

                with col2:

                    st.markdown("**Financial Information**")

                    st.write(
                        f"**Applicant Income:** {selected_application['applicant_income']}"
                    )

                    st.write(
                        f"**Coapplicant Income:** {selected_application['coapplicant_income']}"
                    )

                    st.write(
                        f"**Loan Amount:** {selected_application['loan_amount']}"
                    )

                    st.write(
                        f"**Loan Term:** {selected_application['loan_amount_term']} months"
                    )

                    st.write(
                        f"**Credit History:** {selected_application['credit_history']}"
                    )

                    st.write(
                        f"**Property Area:** {selected_application['property_area']}"
                    )

                st.markdown("---")

                st.markdown("**Prediction Information**")

                if selected_application["prediction"] == "Approved":

                    st.success("Prediction: APPROVED")

                else:

                    st.error("Prediction: REJECTED")

                st.caption(
                    f"Processed by: {selected_application['submitted_by']}"
                )

                st.caption(
                    f"Application Date: {selected_application['application_date']}"
                )

            else:

                st.info(
                    "No applications match your search or filter."
                )




    # ----------------------------------
    # MODEL PERFORMANCE - ADMIN ONLY
    # ----------------------------------

    
    elif page == "Model Performance":

        st.markdown("""
            <style>
            .performance-heading {
                color: #142D4E;
                font-size: 32px;
                font-weight: 700;
            }
            .performance-subtitle {
                color: #64748B;
                font-size: 15px;
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="performance-heading">'
            'Model Performance Analysis</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="performance-subtitle">'
            'Evaluate and compare machine learning algorithms '
            'used for loan eligibility prediction.'
            '</div>',
            unsafe_allow_html=True
        )

        # Load model comparison results
        comparison = pd.read_csv(
            "processed/model_performance_comparison.csv"
        )

        # MODEL COMPARISON
        st.subheader("1. Algorithm Comparison")

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # ACCURACY COMPARISON
        st.subheader("2. Accuracy Comparison")

        accuracy_chart = comparison.set_index("Model")["Accuracy"]

        st.bar_chart(accuracy_chart)

        st.markdown("---")

        # EVALUATION METRICS
        st.subheader("3. Detailed Evaluation Metrics")

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:

            st.markdown("**Precision and Recall**")

            st.bar_chart(
                comparison.set_index("Model")[
                    ["Precision", "Recall"]
                ]
            )

        with metric_col2:

            st.markdown("**F1 Score**")

            st.bar_chart(
                comparison.set_index("Model")["F1 Score"]
            )

        st.markdown("---")

        # SELECTED MODEL
        st.subheader("4. Selected Machine Learning Model")

        st.success(
            "Logistic Regression selected as the final model."
        )

        selected_model = comparison[
            comparison["Model"].str.contains(
                "Logistic Regression",
                case=False,
                na=False
            )
        ]

        if not selected_model.empty:

            selected_accuracy = float(
                selected_model.iloc[0]["Accuracy"]
            )

            selected_f1 = float(
                selected_model.iloc[0]["F1 Score"]
            )

            # Convert decimal values to percentages only when needed
            if selected_accuracy <= 1:
                selected_accuracy *= 100

            if selected_f1 <= 1:
                selected_f1 *= 100
            col1, col2 = st.columns(2)

            col1.metric(
                "Test Accuracy",
                f"{selected_accuracy:.2f}%"
            )

            col2.metric(
                "F1 Score",
                f"{selected_f1:.2f}%"
            )

        st.caption(
            "Model evaluation is based on the held-out test dataset. "
            "Performance metrics indicate predictive performance "
            "and do not guarantee real-world lending outcomes."
        )


    # ----------------------------------
    # FOOTER
    # ----------------------------------

    st.sidebar.markdown("---")

    st.sidebar.caption(
        "Bank Loan Management System | AIML Project"
    )


# ----------------------------------
# APPLICATION ENTRY POINT
# ----------------------------------

if st.session_state.logged_in:

    main_application()

else:

    login_page()
