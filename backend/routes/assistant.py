from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Transaction, Anomaly

from ai_assistant import (
    ask_assistant,
    build_financial_context
)

import pandas as pd


router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"]
)


class AssistantRequest(BaseModel):
    user_id: int
    question: str


@router.post("/ask")
def ask_financial_assistant(request: AssistantRequest):

    db: Session = SessionLocal()

    try:
        transactions = (
            db.query(Transaction)
            .filter(
                Transaction.user_id == request.user_id,
                Transaction.transaction_type == "expense"
            )
            .all()
        )

        if not transactions:
            return {
                "user_id": request.user_id,
                "question": request.question,
                "answer": (
                    "I don't have any expense transactions "
                    "for this user yet."
                )
            }

        anomaly_transactions = (
            db.query(Anomaly.transaction_id)
            .filter(
                Anomaly.user_id == request.user_id,
                Anomaly.transaction_id.isnot(None)
            )
            .all()
        )

        anomaly_ids = {
            transaction_id
            for (transaction_id,) in anomaly_transactions
        }

        data = []

        for transaction in transactions:
            data.append({
                "amount": transaction.amount,
                "category": transaction.category,
                "description": transaction.description,
                "date": transaction.transaction_date,
                "is_anomaly": transaction.id in anomaly_ids
            })

        df = pd.DataFrame(data)

        context = build_financial_context(df)

        answer = ask_assistant(
            request.question,
            context
        )

        return {
            "user_id": request.user_id,
            "question": request.question,
            "answer": answer
        }

    finally:
        db.close()