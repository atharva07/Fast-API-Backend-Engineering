from pydantic import BaseModel
from app.models.role import ProjectRole

class ProjectMembership(BaseModel):
    user_id: int
    role: ProjectRole

class ProjectMembershipResponse(BaseModel):
    project_id: int
    user_id: int
    role: ProjectRole

    model_config = {
        "from_attributes": True
    }