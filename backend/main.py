from fastapi import FastAPI

from .database import engine, Base
from . import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FINOVA AI API",
    description="AI-Powered Personal Finance & Expense Management API",
    version="1.0.0"
)


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