from enum import Enum
from pydantic import BaseModel, ConfigDict

class TestResultStatus(str, Enum):
    RUNNING = "RUNNING"
    PROCESSING = "PROCESSING"
    PASSED = "PASSED"
    FAILED = "FAILED"

class TestResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    test_case_id: int
    status: TestResultStatus

class PaginatedTestResultResponse(BaseModel):
    items: list[TestResultResponse]
    page: int
    page_size: int
    total: int
    total_pages: int