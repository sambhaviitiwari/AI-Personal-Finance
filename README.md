# 💰 AI Personal Finance

> An AI-powered personal finance platform that transforms transaction data into actionable financial insights through machine learning, analytics, forecasting, and conversational AI.

<p align="center">

  <a href="https://ai-personal-financee.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Live Demo">
  </a>

  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">

  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">

  <img src="https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white" alt="Scikit-learn">

</p>

---

## 📌 Overview

Managing personal finances involves more than simply recording transactions.

Traditional expense trackers can show users **where their money went**, but they often provide limited insight into:

- spending behaviour
- unusual transactions
- category-wise spending
- changing financial patterns
- future expenditure
- personalized financial insights

**AI Personal Finance** combines expense management, data analytics, machine learning, forecasting, and generative AI into a single financial intelligence application.

The current implementation is a **Python + Streamlit application** backed by a **SQLite database through SQLAlchemy**, with dedicated modules for expense categorization, anomaly detection, spending forecasting, financial analysis, and AI-assisted insights.

---

## 🎯 Problem Statement

Personal financial data is often spread across different sources such as:

- Bank transactions
- UPI payments
- Payment applications
- Debit and credit card transactions
- Receipts
- Manual expense records

Simply storing this information does not provide enough context.

Users need a system that can help answer questions such as:

> **Where am I spending the most?**

> **Is this transaction unusual?**

> **How is my spending changing over time?**

> **What might my future spending look like?**

> **What does my financial data actually tell me?**

This project explores how machine learning and generative AI can be integrated into a personal finance workflow to answer those questions.

---

# ✨ Key Features

## 💳 Expense & Transaction Management

The application provides a structured interface for managing financial transactions.

Users can:

- Add transactions
- Store transaction amount, date, category and description
- View transaction history
- Filter financial records
- Delete transactions
- Export transaction data as CSV
- Analyse stored transaction data

---

## 🧠 Automated Expense Categorization

The application uses a lightweight NLP classification pipeline to automatically categorize transaction descriptions.

### Pipeline

```text
Transaction Description
          │
          ▼
    TF-IDF Vectorization
          │
          ▼
 Logistic Regression
          │
          ▼
   Predicted Category
```

---

## 🚨 Anomaly Detection

Uses Isolation Forest to flag transactions that deviate from normal spending.

- Validates input: missing columns, non-numeric or missing values, empty data, insufficient history
- Configurable contamination parameter
- Fixed random state for reproducibility
- Results stored per transaction as `is_anomaly`

---

## 📊 Financial Analytics

- Total spending, transaction count, average transaction, largest expense
- Category-wise totals, counts, and averages
- Monthly spending and month-over-month change
- Anomaly summary

---

## 🔮 Spending Forecasting

The forecasting module adapts to how much history is available.

| Data available | Approach |
|---|---|
| Sparse | Moving average: overall average combined with the recent 7-day average |
| Sufficient | Random Forest Regressor on time and lag features |

### Features for the ML model

- Day of week
- Day of month
- Month
- Weekend flag
- Previous-day spend
- Previous-week spend
- Rolling 7-day average

---

## 🤖 AI Financial Assistant

Deterministic analytics are computed first, then passed as structured context to Google Gemini, so answers are grounded in your actual data.

### Example Questions

- "How much did I spend this month?"
- "What is my largest expense?"
- "Which category am I spending the most on?"
- "How has my spending changed?"
- "Show me unusual transactions."

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │       app.py        │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
 ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
 │  Transaction   │   │   Financial    │   │   AI / ML      │
 │  Management    │   │   Analytics    │   │   Modules      │
 └───────┬────────┘   └────────────────┘   └───────┬────────┘
         ▼                                         │
 ┌────────────────┐        Categorizer · Anomaly Detection
 │ SQLAlchemy +   │        Forecasting · AI Assistant (Gemini)
 │ SQLite         │
 └────────────────┘
```

---

## 📁 Project Structure

```text
AI-Personal-Finance/
├── app.py              # Streamlit UI
├── database.py         # SQLAlchemy models, DB config, auth utilities
├── ai_categorizer.py   # TF-IDF + Logistic Regression categorization
├── ai_anomaly.py       # Isolation Forest anomaly detection
├── ai_forecast.py      # Moving-average and Random Forest forecasting
├── ai_assistant.py     # Financial analytics + Gemini-assisted insights
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🗄️ Data Model

```text
User                         Expense
├── id                       ├── id
├── username                 ├── amount
└── password_hash            ├── date
                             ├── category
                             ├── description
                             ├── is_anomaly
                             └── user_id  → User.id
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| Data processing | Pandas, NumPy |
| Machine learning | Scikit-learn |
| NLP / Classification | TF-IDF, Logistic Regression |
| Anomaly detection | Isolation Forest |
| Forecasting | Random Forest, Moving Average |
| Database / ORM | SQLite, SQLAlchemy |
| Visualization | Plotly |
| Generative AI | Google Gemini |
| Auth | bcrypt |
| Config | python-dotenv |
| Deployment | Streamlit Community Cloud |

---

## ⚙️ Installation & Setup

**Prerequisites:** Python 3.9+, pip, Git

### 1. Clone

```bash
git clone https://github.com/sambhaviitiwari/AI-Personal-Finance.git
cd AI-Personal-Finance
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## 🔐 Security & Privacy

- Passwords are hashed with bcrypt
- Expenses are tied to individual users
- Input validation on analytics and ML modules
- API credentials loaded from environment variables

Never commit `.env`, `*.db`, `*.sqlite`, `*.sqlite3`, API keys, or real financial data.

---

## 🧪 Project Status

### Implemented

- Streamlit app with user accounts
- Transaction management and CSV export
- SQLite + SQLAlchemy data layer
- TF-IDF + Logistic Regression categorization
- Isolation Forest anomaly detection
- Spending analytics (monthly, category, change over time)
- Adaptive forecasting (moving average + Random Forest)
- Gemini-assisted financial insights
- Streamlit deployment

### Planned

- Automated unit and integration tests
- Model evaluation: cross-validation, precision / recall / F1, forecast backtesting
- Larger real-world training data for categorization
- Budgets and financial goals
- Receipt / OCR transaction extraction
- REST API layer and PostgreSQL
- Production-grade authentication and role-based access
- CI/CD pipeline

These are future improvements, not current functionality.

---

## 🧠 What We Learned

- Structuring a Python app into UI, data, ML, and AI modules
- TF-IDF text classification and unsupervised anomaly detection
- Feature engineering for time-series forecasting, including graceful handling of sparse data
- Relational modelling with SQLAlchemy
- Combining deterministic analytics with generative AI for grounded responses

---

## 🎓 Academic Project

Developed as a collaborative academic project exploring the integration of machine learning, data analytics, generative AI, and software engineering in a financial application.

---

## 👥 Team

- Nainsy Sharma
- Sambhavi Tiwari
- Jayita Saikia
- Animesh Pandey
- Piyush Yadav
- Pranshu Dubey
- Shivam Sinha

---

## 📜 License

This project is developed for academic and educational purposes.

Developed for academic and educational purposes. A formal open-source license may be added later.
