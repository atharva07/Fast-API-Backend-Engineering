from enum import Enum
from pydantic import BaseModel, Field

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TestCaseStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"

class TestCaseCreate(BaseModel):
    name: str = Field(min_length=3)
    description: str | None = None
    priority: Priority = Priority.MEDIUM

class TestCaseResponse(BaseModel):
    id: int
    name: str
    description: str | None
    priority: Priority
    status: TestCaseStatus