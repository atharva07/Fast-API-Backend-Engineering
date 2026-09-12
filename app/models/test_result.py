from pydantic import BaseModel, ConfigDict

class TestResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    test_case_id: int
    status: str