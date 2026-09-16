from fastapi import FastAPI
from app.routers import test_cases
from app.exceptions.handlers import (
    generic_exception_handler,
    test_case_not_found_handler,
    test_case_not_executable_handler,
    project_already_exists_handler,
    project_not_found_handler
)
from app.exceptions.project import ProjectAlreadyExistsError, ProjectNotFoundError
from app.exceptions.test_case import (
    TestCaseNotExecutableError, TestCaseNotFoundError
)
from app.routers.projects import router as project_router

app = FastAPI()

"""
General Exceptions
"""
app.add_exception_handler(
    Exception,
    generic_exception_handler
)

"""
Exceptions related to Test Cases
"""
app.add_exception_handler(
    TestCaseNotFoundError,
    test_case_not_found_handler
)

app.add_exception_handler(
    TestCaseNotExecutableError,
    test_case_not_executable_handler
)

"""
Exceptions related to Projects
"""
app.add_exception_handler(
    ProjectAlreadyExistsError,
    project_already_exists_handler,
)

app.add_exception_handler(
    ProjectNotFoundError,
    project_not_found_handler,
)

@app.get("/")
def root():
    return {"message": "QAForge Backend is Running"}

app.include_router(
    test_cases.router,
    prefix="/api",
    tags=["Test Cases"],
)

app.include_router(
    project_router
)