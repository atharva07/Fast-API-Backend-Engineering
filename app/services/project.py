from sqlalchemy.exc import IntegrityError
from app.db.models.project import Project
from app.db.unit_of_work import UnitOfWork
from app.exceptions.project import ProjectAlreadyExistsError

class ProjectService:
    def __init__(
        self,
        uow: UnitOfWork
    ):
        self.uow = uow

    def create_project(
        self,
        name: str,
        description: str | None = None,
    ) -> Project:
        with self.uow:
            project = Project(
                name=name, 
                description=description,
            )

            self.uow.projects.add(project)

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise ProjectAlreadyExistsError(
                        "A Project with this name already Exists"
                    )

                raise

            return project