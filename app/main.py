from fastapi import FastAPI
from app.routers import test_cases
from app.exceptions.handlers import generic_exception_handler

app = FastAPI()

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

@app.get("/")
def root():
    return {"message": "QAForge Backend is Running"}

app.include_router(
    test_cases.router,
    prefix="/api",
    tags=["Test Cases"],
)