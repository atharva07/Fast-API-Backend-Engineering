from sqlalchemy.exc import IntegrityError
from app.db.models.associations import ProjectUser
from app.db.unit_of_work import UnitOfWork
from app.exceptions.project_membership import ProjectMembershipAlreadyExistsError, ProjectMembershipNotFoundError

class ProjectMembershipService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add_member(self, project_id: int, user_id: int) -> ProjectUser:
        with self.uow:
            project = self.uow.projects.get_by_id(project_id)

            if project is None:
                raise ProjectMembershipNotFoundError("Project not Found")

            user = self.uow.users.get_by_id(user_id)

            if user is None:
                raise ProjectMembershipNotFoundError("User not Found")

            existing = self.uow.project_membership.get_membership(project_id, user_id)

            if existing is not None:
                raise ProjectMembershipAlreadyExistsError(
                    "User is already a member of this project"
                )

            membership = ProjectUser(project_id=project_id, user_id=user_id)

            self.uow.project_membership.add(membership)

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise ProjectMembershipAlreadyExistsError("User is already a member of this project")
                raise

            return membership

    def get_membership(self, project_id: int, user_id: int) -> ProjectUser:
        with self.uow:
            membership = (
                self.uow.project_membership.get_membership(project_id, user_id)
            )

            if membership is None:
                raise ProjectMembershipNotFoundError("User is not a member of this project")

            return membership