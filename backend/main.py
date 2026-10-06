from fastapi import FastAPI

from .database import engine, Base
from . import models
from .routes.transactions import router as transaction_router
from .routes.users import router as user_router
from .routes.assistant import router as assistant_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FINOVA AI API",
    description="AI-Powered Personal Finance & Expense Management API",
    version="1.0.0"
)


app.include_router(transaction_router)
app.include_router(user_router)
app.include_router(assistant_router)

@app.get("/")
def root():
    return {
        "message": "FINOVA AI Backend is running!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }