from fastapi import Depends
from app.exceptions.project_membership import ProjectAccessDeniedError
from app.models.system_permission import SystemPermission
from app.models.system_role import SystemRole
from app.security.dependencies import get_current_user
from app.db.models.user import User
from app.security.system_permissions import SYSTEM_ROLE_PERMISSIONS

def require_system_permission(required_premission: SystemPermission):
    def permission_checker(current_user: User = Depends(get_current_user)):
        role = SystemRole(current_user.system_role)

        permissions = SYSTEM_ROLE_PERMISSIONS.get(role, set())

        if required_premission not in permissions:
            raise ProjectAccessDeniedError("You do not have permission to perform this action")

        return current_user

    return permission_checker