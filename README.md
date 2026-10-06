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

## 💳 1. Expense & Transaction Management

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

## 🧠 2. Automated Expense Categorization

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
