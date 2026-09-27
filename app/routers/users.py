from fastapi import APIRouter, Depends, status
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.user import UserCreate, UserResponse
from app.services.user import UserService
from app.models.permission import Permission
from app.models.user import UserRoleUpdate
from app.security.authorization import require_global_permission
from app.db.models.user import User

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

"""
    POST Request
"""
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = UserService(uow)

    return service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )

"""
    GET Request
"""
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = UserService(uow)

    return service.get_user(user_id)

"""
    GET Request
"""
@router.get("", response_model=list[UserResponse])
def get_users(uow: UnitOfWork = Depends(get_unit_of_work)):
    service = UserService(uow)

    return service.get_users()

"""
    UPDATE User Role, ADMIN will be allowed to update the user role
"""
@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: int, role_update: UserRoleUpdate, 
                    current_user: User = Depends(require_global_permission(Permission.USER_ROLE_UPDATE)),
                    uow: UnitOfWork = Depends(get_unit_of_work)
):  
    service = UserService(uow)

    return service.update_user_role(
        user_id=user_id,
        user_role=role_update.user_role
    )