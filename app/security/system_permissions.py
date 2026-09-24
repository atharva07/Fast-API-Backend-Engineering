from app.models.system_permission import SystemPermission
from app.models.system_role import SystemRole

SYSTEM_ROLE_PERMISSIONS: dict[
    SystemRole,
    set[SystemPermission],
] = {
    SystemRole.ADMIN: {
        SystemPermission.PROJECT_CREATE
    },

    SystemRole.USER: set()
}