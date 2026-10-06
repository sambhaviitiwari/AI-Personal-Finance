# 💰 FINOVA AI — Personal Finance Management Platform

> An AI-powered personal finance platform for intelligent expense tracking, automated categorization, anomaly detection, spending forecasts, financial analytics, and conversational AI assistance.

---

## 📌 Overview

**FINOVA AI** is an intelligent personal finance management platform designed to help users manage, analyze, and understand their financial activities.

Traditional expense trackers primarily focus on recording transactions. FINOVA AI extends this functionality by integrating **Machine Learning, Data Analytics, Forecasting, Anomaly Detection, and Generative AI**.

The platform allows users to track financial transactions, analyze spending patterns, automatically categorize expenses, detect unusual transactions, forecast future spending, and interact with their financial data through an AI-powered assistant.

---

## ✨ Features

### 💳 Expense Management

* Add and manage financial transactions
* Record income and expenses
* Store transaction amount, category, date, and description
* Maintain transaction history
* Organize financial records using a structured database

### 📊 Financial Analytics

The application provides insights into financial activity, including:

* Total spending
* Category-wise spending
* Income and expense tracking
* Spending trends
* Historical transaction analysis
* Interactive data visualization

### 🏷️ AI-Based Expense Categorization

The system includes an AI-powered categorization module that helps classify transactions into appropriate spending categories.

Examples include:

* Food
* Travel
* Shopping
* Entertainment
* Bills
* Healthcare
* Other financial categories

This reduces the need for completely manual categorization.

### 🚨 Anomaly Detection

FINOVA AI includes an anomaly detection module that analyzes transaction patterns and identifies unusual spending behavior.

For example:

```text
Normal Food Spending
       ↓
₹200 – ₹500
       ↓
Unexpected Transaction
       ↓
₹4,500
       ↓
⚠️ Potential Anomaly
```

The anomaly detection system helps users identify transactions that significantly deviate from their regular spending patterns.

### 🔮 Spending Forecasting

The forecasting module analyzes historical transaction data to estimate future spending.

It can be used to understand:

* Expected future expenditure
* Overall spending trends
* Category-wise spending forecasts
* Potential changes in spending behavior

### 💬 AI Financial Assistant

FINOVA AI includes a conversational AI assistant that allows users to ask questions about their financial data using natural language.

Example questions:

> How much did I spend on food?

> What are my highest expenses?

> Which category has the most spending?

> Analyze my spending pattern.

The AI assistant processes financial information and generates responses based on the available transaction data.

### 🔐 Backend API

The project includes a **FastAPI backend** for managing application data and API communication.

The backend provides:

* API endpoints
* Database connectivity
* User management
* Transaction management
* Budget-related data handling
* AI chat storage
* Forecast and anomaly-related data models
* Health monitoring endpoint

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │     User Interface  │
                    │      Streamlit      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Application      │
                    │      Logic          │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │ Transaction │  │  Analytics  │  │ AI Modules  │
       │ Management  │  │ & Dashboard │  │             │
       └──────┬──────┘  └─────────────┘  └──────┬──────┘
              │                                  │
              ▼                                  ▼
       ┌─────────────┐                  ┌──────────────────┐
       │   SQLite    │                  │ Categorization   │
       │  Database   │                  ├──────────────────┤
       └─────────────┘                  │ Anomaly Detection│
                                        ├──────────────────┤
                                        │ Spending Forecast│
                                        ├──────────────────┤
                                        │ AI Assistant     │
                                        └──────────────────┘
```

---

# 🛠️ Technology Stack

| Component                 | Technology         |
| ------------------------- | ------------------ |
| Programming Language      | Python             |
| Frontend / UI             | Streamlit          |
| Backend API               | FastAPI            |
| Database                  | SQLite             |
| ORM                       | SQLAlchemy         |
| Data Processing           | Pandas             |
| Machine Learning          | Scikit-learn       |
| Forecasting               | Prophet            |
| AI / Generative AI        | Google Gemini API  |
| Data Visualization        | Plotly             |
| Authentication / Security | Bcrypt             |
| API Testing               | FastAPI Swagger UI |

---

# 📂 Project Structure

```text
AI-Personal-Finance/
│
├── app.py
│   └── Main Streamlit application
│
├── database.py
│   └── Database configuration and operations
│
├── ai_categorizer.py
│   └── AI-based expense categorization
│
├── ai_anomaly.py
│   └── Transaction anomaly detection
│
├── ai_forecast.py
│   └── Spending prediction and forecasting
│
├── ai_assistant.py
│   └── AI-powered financial assistant
│
├── backend/
│   ├── main.py
│   │   └── FastAPI application
│   │
│   ├── models.py
│   │   └── Database models
│   │
│   ├── database.py
│   │   └── Backend database configuration
│   │
│   └── ...
│
├── requirements.txt
│   └── Project dependencies
│
├── .env
│   └── Environment variables and API keys
│
├── .gitignore
│   └── Files excluded from version control
│
└── README.md
    └── Project documentation
```

---

# ⚙️ Installation and Setup

## 1. Clone the Repository

```bash
git clone https://github.com/sambhaviitiwari/AI-Personal-Finance.git
cd AI-Personal-Finance
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project directory.

```env
GOOGLE_API_KEY=your_google_api_key
```

The Google API key is used by the AI Financial Assistant.

> Never upload your `.env` file or API keys to a public repository.

---

# 🚀 Running the Streamlit Application

Run:

```bash
streamlit run app.py
```

The application will start locally and can be accessed through the URL displayed in the terminal.

---

# 🌐 Live Application

The Streamlit application is deployed and accessible here:

**[FINOVA AI – Live Demo](https://ai-personal-financee.streamlit.app/?utm_source=chatgpt.com)**

---

# ⚡ Running the FastAPI Backend

Navigate to the project directory and activate the virtual environment.

Then run:

```bash
python -m uvicorn backend.main:app --reload
```

The backend will run locally at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

After starting the backend, open:

```text
http://127.0.0.1:8000/docs
```

This provides the Swagger UI interface where API endpoints can be tested directly.

The backend also includes a health endpoint to verify that the API and database connection are working correctly.

---

# 🧠 AI Modules

## 1. Expense Categorization

The categorization module analyzes transaction information and assigns an appropriate expense category.

```text
Transaction Description
        ↓
Data Processing
        ↓
Machine Learning / Classification
        ↓
Expense Category
```

---

## 2. Anomaly Detection

The anomaly detection module identifies transactions that significantly differ from normal spending behavior.

```text
Historical Transactions
        ↓
Spending Pattern Analysis
        ↓
Anomaly Detection
        ↓
Unusual Transaction Alert
```

---

## 3. Spending Forecasting

The forecasting system uses historical spending information to estimate future financial trends.

```text
Historical Spending Data
        ↓
Data Processing
        ↓
Forecasting Model
        ↓
Predicted Future Spending
```

---

## 4. AI Financial Assistant

The AI assistant enables users to interact with financial information using natural language.

```text
User Question
      ↓
Financial Context
      ↓
AI Processing
      ↓
Generated Financial Insight
```

---

# 🗄️ Database

The application uses **SQLite** for storing financial data.

The database is used to manage entities such as:

* Users
* Transactions
* Budgets
* Forecasts
* Anomalies
* AI chat history

SQLAlchemy is used as the ORM for database interaction in the backend.

---

# 👥 Team Members

* **Nainsy Sharma**
* **Sambhavi Tiwari**
* **Jayita Saikia**
* **Animesh Pandey**
* **Piyush Yadav**
* **Pranshu Dubey**
* **Shivam Sinha**

---

# 🎯 Project Objective

The primary objective of FINOVA AI is to move beyond traditional expense tracking and provide users with intelligent financial insights.

The system combines:

* Expense tracking
* Data analytics
* Machine learning
* Anomaly detection
* Spending prediction
* Generative AI
* Backend API integration

This creates a foundation for a smarter and more interactive personal finance management experience.

---

# 🔮 Future Scope

Possible future enhancements include:

* Advanced authentication and authorization
* Cloud database integration
* Improved ML models
* More advanced financial recommendations
* Receipt scanning and OCR
* Mobile application
* Notifications and financial alerts
* Advanced budget recommendation system

---

# 📄 License

This project is developed for educational and academic purposes.

---

# ⭐ Support

If you find this project useful, consider giving the repository a star ⭐.

---

## 💰 FINOVA AI

**Track smarter. Analyze deeper. Manage finances intelligently.**
