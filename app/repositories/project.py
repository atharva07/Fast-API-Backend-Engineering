from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.project import Project
from app.db.models.associations import ProjectUser

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    # Get by ID
    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.execute(
            select(Project)
            .where(Project.id == project_id)
        ).scalar_one_or_none()

    # Get by Name
    def get_by_name(self, name: str) -> Project | None:
        return self.db.execute(
            select(Project)
            .where(Project.name == name)
        ).scalar_one_or_none()

    # Get all projects
    def get_all(self) -> list[Project]:
        return self.db.execute(
            select(Project)
        ).scalars().all()

    # Get by user
    def get_by_user(self, user_id: int) -> list[Project]:
        return self.db.execute(
            select(Project)
            .join(
                ProjectUser,
                ProjectUser.project_id == Project.id,
            )
            .where(
                ProjectUser.user_id == user_id
            )
        ).scalars().all()

    # Add new Project
    def add(self, project: Project) -> Project:   
        self.db.add(project)
        return project

    # Delete Project
    def delete(self, project: Project) -> None:
        self.db.delete(project)