from sqlalchemy.exc import IntegrityError
from app.db.models.project import Project
from app.db.unit_of_work import UnitOfWork
from app.exceptions.project import ProjectAlreadyExistsError, ProjectNotFoundError
from app.db.models.user import User
from app.models.system_role import SystemRole

class ProjectService:
    def __init__(self,uow: UnitOfWork):
        self.uow = uow

    '''
        This is a POST Request
    '''
    def create_project(self, name: str, description: str | None = None) -> Project:
        with self.uow:
            project = Project(name=name, description=description)

            self.uow.projects.add(project)

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise ProjectAlreadyExistsError("A Project with this name already Exists")
                raise

            return project

    """
        This is a GET Request
    """
    def get_all_projects(self) -> list[Project]:
        with self.uow:
            return self.uow.projects.get_all()

    """
        This is GET Request
    """
    def get_project_for_users(self, user_id: int, current_user: User) -> list[Project]:
        if current_user.system_role == SystemRole.ADMIN.value:
            return self.get_all_projects()
        
        with self.uow:
            return self.uow.projects.get_by_user(user_id)

    """
        This is a GET Request
    """
    def get_project(self, project_id: int) -> Project:
        with self.uow:
            project = self.uow.projects.get_by_id(project_id)

            if project is None:
                raise ProjectNotFoundError("Project Not Found")

            return project

    """
        This is a PUT Request
    """
    def replace_project(self, project_id: int, name: str, description: str | None) -> Project:
        with self.uow:
            project = self.uow.projects.get_by_id(project_id)

            if project is None:
                raise ProjectNotFoundError("Project Not Found")

            project.name = name
            project.description = description

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise ProjectAlreadyExistsError("A Project with this name already exists")
                raise

            return project

    """
        This is a PATCH Request
    """
    def update_project(self, project_id: int, name: str | None, description: str | None) -> Project:
        with self.uow:
            project = self.uow.projects.get_by_id(project_id)

            if project is None:
                raise ProjectNotFoundError("Project Not Found")

            if name is not None:
                project.name = name

            if description is not None:
                project.description = description

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise ProjectAlreadyExistsError("A Project with this name already exists")
                raise

            return project

    """
        This is a DELETE Request
    """
    def delete_project(self, project_id: int) -> None:
        with self.uow:
            project = self.uow.projects.get_by_id(project_id)

            if project is None:
                raise ProjectNotFoundError("Project Not Found")

            self.uow.projects.delete(project)

            self.uow.commit()