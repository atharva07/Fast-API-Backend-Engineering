from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.test_case import (
    TestCaseNotFoundError,
    TestCaseNotExecutableError
)
from app.exceptions.project import ProjectAlreadyExistsError
from app.exceptions.test_suite import TestSuiteNotFoundError, TestSuiteAlreadyExistsError

# Generic Exception handler
async def generic_exception_handler(
        request: Request,
        exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occured"
            }
        }
    )

"""
Exceptions realted to Test Case Module
"""
async def test_case_not_found_handler(
        request: Request,
        exc: TestCaseNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "TEST_CASE_NOT_FOUND",
                "message": str(exc),
            }
        },
    )

async def test_case_not_executable_handler(
        request: Request,
        exc: TestCaseNotExecutableError
):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "TEST_CASE_NOT_EXECUTABLE",
                "message": str(exc),
            }
        },
    )

"""
Exceptions realted to Project Module
"""
async def project_already_exists_handler(
        request: Request,
        exc: ProjectAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "PROJECT_ALREADY_EXISTS",
                "message": str(exc)
            }
        },
    )

async def project_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content = {
            "error": {
                "code": "PROJECT_NOT_FOUND",
                "message": str(exc)
            }
        },
    )

"""
Exceptions related to Test Suite
"""
async def test_suite_already_exists_handler(
        request: Request,
        exc: TestSuiteAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content = {
            "error": {
                "code": "TEST_SUITE_ALREADY_EXISTS",
                "message": str(exc)
            }
        }
    )

async def test_suite_not_found_handler(
        request: Request,
        exc: TestSuiteNotFoundError
):
    return JSONResponse(
        status_code=404,
        content = {
            "error": {
                "code": "TEST_SUITE_NOT_FOUND",
                "message": str(exc)
            }
        }
    )