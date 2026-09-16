from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    name: str = Field(min_length=3)
    description: str | None = None

class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
    )
    description: str | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    execution_timeout: int

    model_config = {
        "from_attributes": True
    }