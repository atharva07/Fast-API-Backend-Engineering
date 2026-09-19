from fastapi import FastAPI
from app.routers import test_cases
from app.exceptions.handlers import (
    generic_exception_handler,
    test_case_not_found_handler,
    test_case_not_executable_handler,
    project_already_exists_handler,
    project_not_found_handler,
    test_suite_not_found_handler,
    test_suite_already_exists_handler,
    test_result_not_found_handler
)
from app.exceptions.project import ProjectAlreadyExistsError, ProjectNotFoundError
from app.exceptions.test_case import (TestCaseNotExecutableError, TestCaseNotFoundError)
from app.exceptions.test_suite import (TestSuiteNotFoundError, TestSuiteAlreadyExistsError)
from app.exceptions.test_result import TestResultNotFoundError
from app.routers.test_cases import router as test_case_router
from app.routers.projects import router as project_router
from app.routers.test_suites import router as test_suite_router
from app.routers.test_results import router as test_result_router

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

"""
Exceptions related to Test Suite
"""
app.add_exception_handler(
    TestSuiteNotFoundError,
    test_suite_not_found_handler,
)

app.add_exception_handler(
    TestSuiteAlreadyExistsError,
    test_suite_already_exists_handler
)

"""
Exception related to Test Result
"""
app.add_exception_handler(
    TestResultNotFoundError,
    test_result_not_found_handler
)

@app.get("/")
def root():
    return {"message": "QAForge Backend is Running"}

app.include_router(
    test_case_router
)

app.include_router(
    project_router
)

app.include_router(
    test_suite_router
)

app.include_router(
    test_result_router
)