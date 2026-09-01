from fastapi import FastAPI
from app.routers import test_cases

app = FastAPI()

@app.get("/")
def root():
    return {"message": "QAForge Backend is Running"}

app.include_router(
    test_cases.router,
    prefix="/api/test-cases",
    tags=["Test Cases"],
)