from fastapi import Depends
from app.db.dependencies import get_unit_of_work
from app.db.models.user import User
from app.db.unit_of_work import UnitOfWork
from app.exceptions.project_membership import ProjectAccessDeniedError
from app.security.dependencies import get_current_user
from app.models.role import ProjectRole
from app.security.dependencies import get_current_user

def get_project_membership(
        project_id: int, 
        current_user: User = Depends(get_current_user), 
        uow: UnitOfWork = Depends(get_unit_of_work)
):
    with uow:

        membership = (
            uow.project_membership.get_membership(
                project_id=project_id,
                user_id=current_user.id
            )
        )

        if membership is None:
            raise ProjectAccessDeniedError("You do not have access to this Project")

        return membership

def require_role(required_role: ProjectRole):
    def role_checker(membership = Depends(get_project_membership)):
        print("MEMBERSHIP ROLE:", membership.role)
        print("REQUIRED ROLE:", required_role.value)

        if membership.role != required_role.value:
            raise ProjectAccessDeniedError("You do not have Permission to perform this action")

        return membership

    return role_checker