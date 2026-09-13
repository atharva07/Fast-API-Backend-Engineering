from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(
        self,
        name: str,
    ) -> Project | None:
        return self.db.execute(
            select(Project)
            .where(Project.name == name)
        ).scalar_one_or_none()

    def add(
        self,
        project: Project,
    ) -> Project:   
        self.db.add(project)

        return project