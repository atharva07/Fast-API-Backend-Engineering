from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

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
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: str | None
    priority: Priority
    status: TestCaseStatus

class TestCaseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    description: str | None = None
    priority: Priority | None = None
    status: TestCaseStatus | None = None