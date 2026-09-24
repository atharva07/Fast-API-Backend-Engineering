from pydantic import BaseModel
from app.models.role import UserRole

class ProjectMembership(BaseModel):
    user_id: int

class ProjectMembershipResponse(BaseModel):
    project_id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }