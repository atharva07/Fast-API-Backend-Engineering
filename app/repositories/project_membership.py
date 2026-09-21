from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.associations import ProjectUser

class ProjectMembeshipRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_membership(self, project_id: int, user_id: int) -> ProjectUser | None:
        return self.db.execute(
            select(ProjectUser).where(
                ProjectUser.project_id == project_id,
                ProjectUser.user_id == user_id,
            )
        ).scalar_one_or_none()

    def get_project_members(self, project_id: int) -> list[ProjectUser]:
        return self.db.execute(
            select(ProjectUser).where(
                ProjectUser.project_id == project_id
            )
        ).scalars().all()

    def add(self, membership: ProjectUser) -> ProjectUser:
        self.db.add(membership)
        return membership
    