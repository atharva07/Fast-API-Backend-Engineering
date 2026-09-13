from fastapi import FastAPI
from app.routers import test_cases
from app.exceptions.handlers import (
    generic_exception_handler,
    test_case_not_found_handler,
    test_case_not_executable_handler,
    project_already_exists_handler
)
from app.exceptions.project import ProjectAlreadyExistsError
from app.exceptions.test_case import (
    TestCaseNotExecutableError, TestCaseNotFoundError
)

app = FastAPI()

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.add_exception_handler(
    TestCaseNotFoundError,
    test_case_not_found_handler
)

app.add_exception_handler(
    TestCaseNotExecutableError,
    test_case_not_executable_handler
)

app.add_exception_handler(
    ProjectAlreadyExistsError,
    project_already_exists_handler,
)

@app.get("/")
def root():
    return {"message": "QAForge Backend is Running"}

app.include_router(
    test_cases.router,
    prefix="/api",
    tags=["Test Cases"],
)