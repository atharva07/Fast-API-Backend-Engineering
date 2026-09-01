from fastapi import APIRouter
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
@router.get("/{test_case_id}")
def get_test_case(test_case_id: int):
    return {
        "id": test_case_id,
        "name": "Sample Test Case",
    }