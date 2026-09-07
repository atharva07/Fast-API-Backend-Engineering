from fastapi import APIRouter, Header, HTTPException
from app.models.test_case import TestCaseCreate, TestCaseResponse

router = APIRouter()

@router.get("")
def get_test_cases():
    return {
        "test_cases": [
            {
                "id": 1,
                "name": "Login with valid credentials",
                "status": "PASSED"
            },
            {
                "id": 2,
                "name": "Login with invalid password",
                "status": "FAILED"
            }
        ]
    }

@router.post("", response_model=TestCaseResponse)
def create_test_case(test_case: TestCaseCreate):
    return {
        "id": 1,
        "name": test_case.name,
        "description": test_case.description,
        "priority": test_case.priority,
        "status": test_case.status
    }

# Get specific test case by ID
@router.get("test-cases/{test_case_id}")
def get_test_case(test_case_id: int):
    if test_case_id != 1:
        raise HTTPException(
            status_code = 404,
            detail = "Test case not found"
        )

    return {
        "id": test_case_id,
        "name": "Sample Test Case",
    }

@router.get("test-cases/search")
def search_test_case(
    status: str | None = None,
    page: int = 1,
    limit: int = 10
):
    return {
        "status": status,
        "message": "Searching Test Case"
    }

@router.get("test-cases/debug")
def debug_request(x_request_id: str | None = Header(None)):
    return {
        "request_id": x_request_id
    }

@router.post("/api/projects/{project_id}/test-cases")
def create_tests_case(
    project_id: int,
    test_case: TestCaseCreate,
    notify: bool = False,
    x_request_id: str | None = Header(default=None),
):
    return {
        "project_id": project_id,
        "notify": notify,
        "request_id": x_request_id,
        "test_case": test_case
    }

@router.get("/error")
def trigger_error():
    raise Exception("This is a test exception")