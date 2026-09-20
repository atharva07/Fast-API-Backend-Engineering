from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.test_case import TestCaseNotFoundError, TestCaseNotExecutableError, TestCaseAlreadyExistsError
from app.exceptions.project import ProjectAlreadyExistsError
from app.exceptions.test_suite import TestSuiteNotFoundError, TestSuiteAlreadyExistsError
from app.exceptions.test_result import TestResultNotFoundError
from app.exceptions.user import UserNotFoundError, UserAlreadyExistsExceptions
from app.exceptions.auth import InvalidCredentialsError

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
                "message": f"An unexpected error occured: {str(exc)}"
            }
        },
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

async def test_case_already_exists_handler(
        request: Request,
        exc: TestCaseAlreadyExistsError
): 
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "TEST_CASE_ALREADY_EXISTS",
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
        },
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
        },
    )

"""
Exceptions related to Test Results
"""
async def test_result_not_found_handler(
        request: Request,
        exc: TestResultNotFoundError
):
    return JSONResponse(
        status_code=404,
        content= {
            "error": {
                "code": "TEST_RESULT_NOT_FOUND",
                "message": str(exc)
            }
        },
    )

"""
Exceptions related to User
"""
async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundError
):
    return JSONResponse(
        status_code=404,
        content= {
            "error": {
                "code": "USER_NOT_FOUND",
                "message": str(exc)
            }
        },
    )

async def user_already_exists_handler(
        request: Request,
        exc: UserAlreadyExistsExceptions
):
    return JSONResponse(
        status_code=409,
        content= {
            "error": {
                "code": "USER_ALREADY_EXISTS",
                "message": str(exc)
            }
        },
    )

"""
Exceptions related to Auth
"""
async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsError
):
    return JSONResponse(
        status_code=409,
        content= {
            "error": {
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        },
    )