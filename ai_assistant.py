import os
import json
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv




load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-1.5-flash"




def calculate_financial_summary(df):
    """
    Creates an overall summary of the user's expenses.
    """

    if df is None or df.empty:
        return {
            "total_spending": 0,
            "transaction_count": 0,
            "average_transaction": 0,
            "largest_expense": None,
            "category_totals": {}
        }

    df = df.copy()

    
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(subset=["amount"])

    total_spending = float(df["amount"].sum())

    transaction_count = len(df)

    average_transaction = float(
        df["amount"].mean()
    )

    
    category_totals = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )

    category_totals = {
        str(category): round(float(amount), 2)
        for category, amount in category_totals.items()
    }

    
    largest = df.loc[df["amount"].idxmax()]

    largest_expense = {
        "amount": round(float(largest["amount"]), 2),
        "category": str(largest.get("category", "Unknown")),
        "description": str(
            largest.get("description", "Unknown")
        ),
        "date": str(largest.get("date", "Unknown"))
    }

    return {
        "total_spending": round(total_spending, 2),
        "transaction_count": transaction_count,
        "average_transaction": round(
            average_transaction,
            2
        ),
        "largest_expense": largest_expense,
        "category_totals": category_totals
    }




def calculate_monthly_spending(df):
    """
    Calculates total spending for every month.
    """

    if df is None or df.empty:
        return {}

    df = df.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["amount", "date"]
    )

    df["month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby("month")["amount"]
        .sum()
        .sort_index()
    )

    return {
        str(month): round(float(amount), 2)
        for month, amount in monthly.items()
    }




def calculate_category_analysis(df):
    """
    Provides detailed category-wise spending information.
    """

    if df is None or df.empty:
        return {}

    df = df.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["amount"]
    )

    result = (
        df.groupby("category")["amount"]
        .agg(
            total="sum",
            transactions="count",
            average="mean"
        )
        .sort_values(
            "total",
            ascending=False
        )
    )

    analysis = {}

    for category, row in result.iterrows():

        analysis[str(category)] = {
            "total": round(
                float(row["total"]),
                2
            ),
            "transactions": int(
                row["transactions"]
            ),
            "average": round(
                float(row["average"]),
                2
            )
        }

    return analysis




def calculate_spending_change(df):
    """
    Compares the latest month with the previous month.
    """

    monthly = calculate_monthly_spending(df)

    if len(monthly) < 2:
        return {
            "available": False,
            "message": (
                "Not enough monthly data "
                "for comparison."
            )
        }

    months = list(monthly.keys())

    previous_month = months[-2]
    current_month = months[-1]

    previous_amount = monthly[previous_month]
    current_amount = monthly[current_month]

    difference = (
        current_amount -
        previous_amount
    )

    if previous_amount != 0:

        percentage_change = (
            difference /
            previous_amount
        ) * 100

    else:

        percentage_change = None

    return {
        "available": True,
        "previous_month": previous_month,
        "current_month": current_month,
        "previous_spending": previous_amount,
        "current_spending": current_amount,
        "difference": round(
            difference,
            2
        ),
        "percentage_change": (
            round(
                percentage_change,
                2
            )
            if percentage_change is not None
            else None
        )
    }




def get_anomaly_information(df):
    """
    Retrieves transactions already flagged as anomalies
    by the project's anomaly detection module.
    """

    if (
        df is None
        or df.empty
        or "is_anomaly" not in df.columns
    ):
        return []

    anomalies = df[
        df["is_anomaly"] == True
    ]

    results = []

    for _, row in anomalies.iterrows():

        results.append({
            "amount": round(
                float(row["amount"]),
                2
            ),
            "category": str(
                row.get(
                    "category",
                    "Unknown"
                )
            ),
            "description": str(
                row.get(
                    "description",
                    "Unknown"
                )
            ),
            "date": str(
                row.get(
                    "date",
                    "Unknown"
                )
            )
        })

    return results



def build_financial_context(df):
    """
    Creates all verified financial information that
    will be given to the AI assistant.
    """

    context = {

        "overall_summary":
            calculate_financial_summary(df),

        "monthly_spending":
            calculate_monthly_spending(df),

        "category_analysis":
            calculate_category_analysis(df),

        "spending_comparison":
            calculate_spending_change(df),

        "flagged_unusual_transactions":
            get_anomaly_information(df)
    }

    return context




SYSTEM_PROMPT = """
You are an AI Personal Finance Assistant.

Your purpose is to help the user understand their
personal expense data.

IMPORTANT RULES:

1. ONLY use the financial data provided in the
   VERIFIED FINANCIAL DATA section.

2. NEVER invent financial numbers.

3. NEVER invent transactions.

4. NEVER invent categories or dates.

5. If the available data is insufficient to answer
   a question, clearly tell the user that there is
   not enough data.

6. If a transaction is marked as unusual, describe
   it as a potentially unusual transaction.

7. NEVER say that an unusual transaction is
   definitely fraud.

8. Forecasts or predictions must be described as
   estimates, not guaranteed results.

9. Budget or saving suggestions must be described
   as recommendations.

10. Do not modify the user's financial records.

11. Give answers in simple language.

12. When useful, explain the calculation behind
    your answer.

13. Do not expose information belonging to another
    user.

14. Do not pretend to know information that is not
    present in the supplied financial data.

15. This assistant provides financial information
    and spending insights, not guaranteed
    professional financial advice.
"""




def ask_assistant(question, context_data):
    """
    Sends the user's question and verified financial
    context to Gemini and returns the answer.
    """

    if not GOOGLE_API_KEY:
        return (
            "Google API key is not configured. "
            "Please check your .env file."
        )

    if not question or not question.strip():
        return (
            "Please enter a financial question."
        )

    try:

        
        if isinstance(context_data, str):

            context = context_data

        else:

            context = json.dumps(
                context_data,
                indent=2,
                default=str
            )

        model = genai.GenerativeModel(
            MODEL_NAME
        )

        prompt = f"""
{SYSTEM_PROMPT}

==================================================
VERIFIED FINANCIAL DATA
==================================================

{context}

==================================================
USER QUESTION
==================================================

{question}

==================================================
INSTRUCTIONS
==================================================

Answer the user's question using ONLY the
verified financial data above.

Be concise but useful.

If the question asks for a calculation,
use the supplied numbers.

If the question asks for a recommendation,
make it clear that it is a recommendation.

If the data does not contain enough information,
say so instead of guessing.
"""

        response = model.generate_content(
            prompt
        )

        if response is None:
            return (
                "I couldn't generate a response."
            )

        if not hasattr(response, "text"):
            return (
                "I couldn't generate a response."
            )

        answer = response.text.strip()

        if not answer:
            return (
                "I couldn't generate a response."
            )

        return answer

    except Exception as e:

        return (
            "Sorry, I couldn't process your "
            f"question right now. Error: {str(e)}"
        )


# ============================================================
# RECEIPT DATA EXTRACTION
# ============================================================

def extract_receipt_data(image):
    """
    Extracts transaction information from a receipt image.

    This function is kept because the existing app.py
    imports and uses it.
    """

    if not GOOGLE_API_KEY:
        return None

    try:

        model = genai.GenerativeModel(
            MODEL_NAME
        )

        prompt = """
Analyze this receipt image and extract the following
information:

1. Merchant name
2. Total amount
3. Date
4. Suggested expense category

Return ONLY valid JSON in this format:

{
    "merchant": "...",
    "amount": 0,
    "date": "...",
    "category": "..."
}

If a field cannot be determined, use null.
"""

        response = model.generate_content(
            [
                prompt,
                image
            ]
        )

        if not response or not response.text:
            return None

        text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        return json.loads(text)

    except Exception as e:

        print(
            f"Receipt extraction error: {e}"
        )

        return None
