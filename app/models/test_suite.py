from pydantic import BaseModel, Field

class TestSuiteCreate(BaseModel):
    name: str = Field(min_length=3)
    description: str | None = None

class TestSuiteUpdate(BaseModel):
    name: str | None = Field(
        default = None,
        min_length = 3
    )
    description: str | None = None

class TestSuiteResponse(BaseModel):
    id: int
    name: str
    description: str | None
    project_id: int

    model_config = {
        "from_attributes": True
    }