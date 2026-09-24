from app.models.permission import Permission
from app.models.role import UserRole

ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {

    UserRole.ADMIN: {
        permission 
        for permission in Permission
    },

    UserRole.QA_ENGINEER: {
        Permission.PROJECT_VIEW,

        Permission.TEST_SUITE_VIEW,
        Permission.TEST_SUITE_CREATE,
        Permission.TEST_SUITE_DELETE,

        Permission.TEST_CASE_VIEW,
        Permission.TEST_CASE_CREATE,
        Permission.TEST_CASE_DELETE
    },

    UserRole.DEVELOPER: {
        Permission.PROJECT_VIEW,

        Permission.TEST_SUITE_VIEW,

        Permission.TEST_CASE_VIEW
    },

    UserRole.VIEWER: {
        Permission.PROJECT_VIEW,
        
        Permission.TEST_SUITE_VIEW,

        Permission.TEST_CASE_VIEW
    },
}


