from fastapi import Depends
from app.db.dependencies import get_unit_of_work
from app.db.models.user import User
from app.db.unit_of_work import UnitOfWork
from app.exceptions.project_membership import ProjectAccessDeniedError
from app.security.dependencies import get_current_user
from app.models.role import UserRole
from app.security.dependencies import get_current_user
from app.models.permission import Permission
from app.security.permissions import ROLE_PERMISSIONS
from app.exceptions.test_suite import TestSuiteNotFoundError

def get_project_membership(project_id: int, current_user: User = Depends(get_current_user),
            uow: UnitOfWork = Depends(get_unit_of_work)):
    if current_user.user_role == UserRole.ADMIN.value:
        return None
    
    with uow:
        membership = (
            uow.project_memberships.get_membership(project_id=project_id, user_id=current_user.id)
        )

        if membership is None:
            raise ProjectAccessDeniedError("You do not have access to this Project")

        return membership

def require_project_permission(required_permission: Permission):
    def permission_checker(current_user: User = Depends(get_current_user), membership = Depends(get_project_membership)):
        role = UserRole(current_user.user_role)

        permissions = ROLE_PERMISSIONS.get(role, set())

        if required_permission not in permissions:
            raise ProjectAccessDeniedError("You do not have permission to perform this action")

        return current_user

    return permission_checker

def require_global_permission(required_permission: Permission):
    def permission_checker(current_user: User = Depends(get_current_user)):
        role = UserRole(current_user.user_role)

        permissions = ROLE_PERMISSIONS.get(role, set())

        if required_permission not in permissions:
            raise ProjectAccessDeniedError("You do not have permission to perform this action")

        return current_user

    return permission_checker

def get_suite_project_id(suite_id: int, uow: UnitOfWork = Depends(get_unit_of_work)) -> int:
    with uow:
        project_id = uow.test_suites.get_project_id(suite_id)

        if project_id is None:
            raise TestSuiteNotFoundError("Test Suite Not Found")

        return project_id   

def get_suite_project_membership(project_id: int = Depends(get_suite_project_id), current_user: User = Depends(get_current_user),
                                uow: UnitOfWork = Depends(get_unit_of_work)):
    if current_user.user_role == UserRole.ADMIN.value:
        return None

    with uow:
        membership = (
            uow.project_memberships.get_membership(
                project_id=project_id,
                user_id=current_user.id
            )
        )

        if membership is None:
            raise ProjectAccessDeniedError(
                "You do not have access to this project"
            )

        return membership

def require_suite_permission(required_permission: Permission):
    def permission_checker(
        current_user: User = Depends(get_current_user),
        membership = Depends(get_suite_project_membership)
    ):
        role = UserRole(current_user.user_role)

        permissions = ROLE_PERMISSIONS.get(role, set())

        if required_permission not in permissions:
            raise ProjectAccessDeniedError(
                "You do not permission to perform this action"
            )

        return current_user
    
    return permission_checker