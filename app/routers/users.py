from fastapi import APIRouter, Depends, status
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.user import UserCreate, UserResponse
from app.services.user import UserService

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