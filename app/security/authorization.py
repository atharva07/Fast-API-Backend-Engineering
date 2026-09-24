from fastapi import Depends
from app.db.dependencies import get_unit_of_work
from app.db.models.user import User
from app.db.unit_of_work import UnitOfWork
from app.exceptions.project_membership import ProjectAccessDeniedError
from app.security.dependencies import get_current_user
from app.models.role import ProjectRole
from app.security.dependencies import get_current_user
from app.models.permission import Permission
from app.security.permissions import ROLE_PERMISSIONS
from app.models.system_role import SystemRole

def get_project_membership(
        project_id: int,
        current_user: User = Depends(get_current_user), 
        uow: UnitOfWork = Depends(get_unit_of_work)
):
    if current_user.system_role == SystemRole.ADMIN.value:
        return None
    
    with uow:
        membership = (
            uow.project_membership.get_membership(project_id=project_id, user_id=current_user.id)
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

def require_permission(required_permission: Permission):
    def permission_checker(current_user: User = Depends(get_current_user), membership = Depends(get_project_membership)):
        if current_user.system_role == SystemRole.ADMIN.value:
            return current_user
        
        role = ProjectRole(membership.role)

        permissions = ROLE_PERMISSIONS.get(role, set())

        if required_permission not in permissions:
            raise ProjectAccessDeniedError("You do not have permission to perform this action")

        return membership

    return permission_checker