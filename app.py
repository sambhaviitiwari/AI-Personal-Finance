import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# ---------------------------------------------------------
# IMPORT CUSTOM MODULES
# ---------------------------------------------------------

from database import (
    SessionLocal,
    User,
    Expense,
    get_password_hash,
    verify_password,
    Base,
    engine
)

from ai_categorizer import predict_category
from ai_anomaly import detect_anomalies
from ai_forecast import get_spending_forecast
from ai_assistant import ask_assistant, extract_receipt_data


# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# STREAMLIT CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Expense Tracker",
    page_icon="📈",
    layout="wide"
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None


# ---------------------------------------------------------
# DATABASE HELPER
# ---------------------------------------------------------

def get_user_expenses(db, user_id):

    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .all()
    )

    if not expenses:
        return pd.DataFrame()

    data = []

    for exp in expenses:

        data.append({
            "id": exp.id,
            "amount": exp.amount,
            "date": exp.date,
            "category": exp.category,
            "description": exp.description,
            "is_anomaly": exp.is_anomaly
        })

    return pd.DataFrame(data)


# =========================================================
# AUTHENTICATION
# =========================================================

def render_auth():

    st.title("Welcome to AI-Powered Finance 🚀")

    tab1, tab2 = st.tabs(
        ["Login", "Sign Up"]
    )

    db = SessionLocal()

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    with tab1:

        st.subheader("Login")

        log_username = st.text_input(
            "Username",
            key="log_user"
        )

        log_password = st.text_input(
            "Password",
            type="password",
            key="log_pass"
        )

        if st.button("Login"):

            user = (
                db.query(User)
                .filter(
                    User.username == log_username
                )
                .first()
            )

            if user and verify_password(
                log_password,
                user.password_hash
            ):

                st.session_state["user_id"] = user.id
                st.session_state["username"] = user.username

                st.success(
                    "Logged in successfully!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid credentials"
                )

    # -----------------------------------------------------
    # SIGN UP
    # -----------------------------------------------------

    with tab2:

        st.subheader("Create Account")

        sign_username = st.text_input(
            "Username",
            key="sign_user"
        )

        sign_password = st.text_input(
            "Password",
            type="password",
            key="sign_pass"
        )

        if st.button("Sign Up"):

            existing_user = (
                db.query(User)
                .filter(
                    User.username == sign_username
                )
                .first()
            )

            if existing_user:

                st.error(
                    "Username already exists"
                )

            else:

                new_user = User(
                    username=sign_username,
                    password_hash=get_password_hash(
                        sign_password
                    )
                )

                db.add(new_user)
                db.commit()

                st.success(
                    "Account created! Please log in."
                )

    db.close()


# =========================================================
# MAIN APPLICATION
# =========================================================

def render_app():

    st.sidebar.title(
        f"👤 {st.session_state['username']}"
    )

    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    if st.sidebar.button("Logout"):

        st.session_state["user_id"] = None
        st.session_state["username"] = None

        st.rerun()

    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Transactions",
            "AI Assistant",
            "Generate Mock Data"
        ]
    )

    db = SessionLocal()

    df_expenses = get_user_expenses(
        db,
        st.session_state["user_id"]
    )

    # -----------------------------------------------------
    # PAGE ROUTING
    # -----------------------------------------------------

    if menu == "Dashboard":

        render_dashboard(
            df_expenses
        )

    elif menu == "Transactions":

        render_transactions(
            db,
            df_expenses
        )

    elif menu == "AI Assistant":

        render_assistant(
            df_expenses
        )

    elif menu == "Generate Mock Data":

        render_mock_data(
            db
        )

    db.close()


# =========================================================
# DASHBOARD
# =========================================================

def render_dashboard(df):

    st.title(
        "Financial Dashboard 📊"
    )

    # -----------------------------------------------------
    # EMPTY STATE
    # -----------------------------------------------------

    if df.empty:

        st.info(
            "No expenses found. "
            "Go to Transactions to add some "
            "or generate mock data."
        )

        return

    # -----------------------------------------------------
    # ANOMALY DETECTION
    # -----------------------------------------------------

    df = detect_anomalies(df)

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Spent",
        f"₹{df['amount'].sum():,.2f}"
    )

    col2.metric(
        "Total Transactions",
        len(df)
    )

    anomalies_count = len(
        df[
            df["is_anomaly"] == True
        ]
    )

    col3.metric(
        "Anomalies Detected",
        anomalies_count,
        delta_color="inverse"
    )

    st.markdown("---")

    # =====================================================
    # SPENDING TREND
    # =====================================================

    st.subheader(
        "📈 Spending Trend"
    )

    daily_spend = (
        df.groupby("date")["amount"]
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        daily_spend,
        x="date",
        y="amount",
        title="Daily Spending"
    )

    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount (₹)"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =====================================================
    # CATEGORY BREAKDOWN
    # =====================================================

    st.subheader(
        "🥧 Spending by Category"
    )

    cat_spend = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        cat_spend,
        names="category",
        values="amount",
        hole=0.3
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # =====================================================
    # ANOMALIES
    # =====================================================

    if anomalies_count > 0:

        st.subheader(
            "🚨 Unusual Spending Detected"
        )

        st.warning(
            f"The AI flagged {anomalies_count} "
            "transaction(s) as unusual based "
            "on your spending habits."
        )

        st.dataframe(
            df[
                df["is_anomaly"] == True
            ][
                [
                    "date",
                    "description",
                    "amount",
                    "category"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # AI SPENDING FORECAST
    # =====================================================

    st.subheader(
        "🔮 AI Spending Forecast"
    )

    try:

        forecast_result = get_spending_forecast(
            df.to_dict("records"),
            days_ahead=14
        )

        # -------------------------------------------------
        # FORECAST ERROR
        # -------------------------------------------------

        if "error" in forecast_result:

            st.info(
                "Not enough transaction data "
                "to generate a forecast."
            )

        else:

            forecast_summary = (
                forecast_result["summary"]
            )

            forecast_df = pd.DataFrame(
                forecast_summary.get(
                    "daily_forecasts",
                    []
                )
            )

            # -------------------------------------------------
            # FORECAST CHART
            # -------------------------------------------------

            if forecast_df.empty:

                st.info(
                    "Not enough data to generate "
                    "a forecast."
                )

            else:

                fig3 = px.line(
                    forecast_df,
                    x="date",
                    y="predicted_amount",
                    title=(
                        "Predicted Spending "
                        "(Next 14 Days)"
                    )
                )

                fig3.update_traces(
                    line_dash="dot"
                )

                fig3.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Predicted Amount (₹)"
                )

                st.plotly_chart(
                    fig3,
                    use_container_width=True
                )

                # -------------------------------------------------
                # FORECAST METRICS
                # -------------------------------------------------

                forecast_col1, forecast_col2 = (
                    st.columns(2)
                )

                forecast_col1.metric(
                    "Projected Spending",
                    f"₹{forecast_summary['projected_total']:,.2f}"
                )

                forecast_col2.metric(
                    "Forecast Confidence",
                    f"{forecast_summary['confidence_score'] * 100:.0f}%"
                )

                st.caption(
                    f"Model used: "
                    f"{forecast_summary['model_used']}"
                )

                # -------------------------------------------------
                # CATEGORY FORECAST
                # -------------------------------------------------

                st.subheader(
                    "📊 Category-wise Forecast"
                )

                category_forecasts = (
                    forecast_result.get(
                        "categories",
                        {}
                    )
                )

                if category_forecasts:

                    category_df = pd.DataFrame(
                        [
                            {
                                "Category": category,

                                "Projected Spending":
                                    data[
                                        "projected_total"
                                    ],

                                "Daily Average":
                                    data[
                                        "daily_average"
                                    ],

                                "Model":
                                    data[
                                        "model_used"
                                    ]
                            }

                            for category, data
                            in category_forecasts.items()
                        ]
                    )

                    st.dataframe(
                        category_df,
                        use_container_width=True,
                        hide_index=True
                    )

    except Exception as e:

        st.error(
            f"Forecast error: {e}"
        )


# =========================================================
# TRANSACTIONS
# =========================================================

def render_transactions(db, df):

    st.title(
        "Transactions 💸"
    )

    # =====================================================
    # ADD EXPENSE
    # =====================================================

    with st.expander(
        "➕ Add New Expense"
    ):

        desc = st.text_input(
            "Description",
            key="expense_description"
        )

        amt = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            format="%.2f",
            key="expense_amount"
        )

        dt = st.date_input(
            "Date",
            key="expense_date"
        )

        if st.button(
            "Save Expense",
            key="save_expense"
        ):

            if not desc.strip():

                st.error(
                    "Please enter an expense description."
                )

            else:

                # AI auto categorization
                cat = predict_category(
                    desc
                )

                new_exp = Expense(
                    amount=amt,
                    date=dt,
                    category=cat,
                    description=desc,
                    user_id=st.session_state[
                        "user_id"
                    ]
                )

                db.add(new_exp)
                db.commit()

                st.success(
                    f"Added successfully! "
                    f"AI categorized it as: **{cat}**"
                )

                st.rerun()

    # =====================================================
    # RECEIPT OCR
    # =====================================================

    with st.expander(
        "📸 Upload Receipt (AI OCR)"
    ):

        st.info(
            "Requires a valid GOOGLE_API_KEY "
            "in your .env file."
        )

        uploaded_file = st.file_uploader(
            "Choose a receipt image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ],
            key="receipt_upload"
        )

        if uploaded_file is not None:

            st.image(
                uploaded_file,
                caption="Receipt",
                width=300
            )

            if st.button(
                "Extract Data",
                key="extract_receipt"
            ):

                with st.spinner(
                    "AI is analyzing the receipt..."
                ):

                    try:

                        data = extract_receipt_data(
                            uploaded_file
                        )

                        if "error" in data:

                            st.error(
                                f"Error: {data['error']}"
                            )

                        else:

                            st.success(
                                "Receipt data extracted!"
                            )

                            st.write(
                                "Amount:",
                                data.get("amount")
                            )

                            st.write(
                                "Description:",
                                data.get("description")
                            )

                    except Exception as e:

                        st.error(
                            f"OCR error: {e}"
                        )

    # =====================================================
    # TRANSACTION HISTORY
    # =====================================================

    st.subheader(
        "📋 Transaction History"
    )

    if df.empty:

        st.info(
            "No transactions yet. "
            "Add an expense above."
        )

    else:

        display_df = (
            df.sort_values(
                by="date",
                ascending=False
            )
            .copy()
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# AI FINANCIAL ASSISTANT
# =========================================================

def render_assistant(df):

    st.title(
        "AI Financial Assistant 🤖"
    )

    st.write(
        "Ask questions about your finances "
        "in plain language."
    )

    st.info(
        "Requires a valid GOOGLE_API_KEY "
        "in your .env file."
    )

    if df.empty:

        st.warning(
            "You need some transactions first."
        )

        return

    question = st.text_input(
        "Example: "
        "'How much did I spend on Food this month?'",
        key="assistant_question"
    )

    if st.button(
        "Ask AI",
        key="ask_ai"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

            return

        with st.spinner(
            "Thinking..."
        ):

            summary = (
                df.groupby(
                    "category"
                )["amount"]
                .sum()
                .to_dict()
            )

            recent = (
                df.sort_values(
                    by="date",
                    ascending=False
                )
                .head(10)
                .to_dict("records")
            )

            context = (
                f"Category Totals: {summary}\n"
                f"Recent 10 Transactions: {recent}"
            )

            try:

                response = ask_assistant(
                    question,
                    context
                )

                st.write(
                    "### Answer:"
                )

                st.write(
                    response
                )

            except Exception as e:

                st.error(
                    f"AI Assistant error: {e}"
                )


# =========================================================
# MOCK DATA GENERATOR
# =========================================================

def render_mock_data(db):

    st.title(
        "Generate Mock Data 🧪"
    )

    st.write(
        "Use this for your faculty presentation "
        "to instantly populate the dashboard."
    )

    if st.button(
        "Generate 3 Months of Data",
        key="generate_mock"
    ):

        categories = [
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Utilities"
        ]

        descriptions = {

            "Food": [
                "Walmart",
                "Starbucks",
                "McDonalds",
                "Groceries"
            ],

            "Transport": [
                "Uber",
                "Gas Station",
                "Train Ticket"
            ],

            "Shopping": [
                "Amazon",
                "Target",
                "Clothes"
            ],

            "Entertainment": [
                "Netflix",
                "Movie",
                "Spotify"
            ],

            "Utilities": [
                "Electric Bill",
                "Water",
                "Internet"
            ]
        }

        today = datetime.now()

        expenses_to_add = []

        # -------------------------------------------------
        # NORMAL SPENDING
        # -------------------------------------------------

        for i in range(90):

            date = (
                today
                - timedelta(days=i)
            )

            # 1–3 transactions per day
            for _ in range(
                random.randint(1, 3)
            ):

                cat = random.choice(
                    categories
                )

                desc = random.choice(
                    descriptions[cat]
                )

                amt = random.uniform(
                    5.0,
                    50.0
                )

                exp = Expense(

                    amount=round(
                        amt,
                        2
                    ),

                    date=date.date(),

                    category=cat,

                    description=desc,

                    user_id=st.session_state[
                        "user_id"
                    ]
                )

                expenses_to_add.append(
                    exp
                )

        # -------------------------------------------------
        # ANOMALOUS TRANSACTION
        # -------------------------------------------------

        anomaly = Expense(

            amount=850.00,

            date=(
                today
                - timedelta(days=5)
            ).date(),

            category="Travel",

            description=(
                "Last minute Flight to Paris"
            ),

            user_id=st.session_state[
                "user_id"
            ]
        )

        expenses_to_add.append(
            anomaly
        )

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        db.bulk_save_objects(
            expenses_to_add
        )

        db.commit()

        st.success(
            "Generated ~150 mock transactions successfully!"
        )

        st.rerun()


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if st.session_state["user_id"] is None:

    render_auth()

else:

    render_app()