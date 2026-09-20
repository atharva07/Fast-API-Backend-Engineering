from fastapi import APIRouter, Depends
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.auth import LoginRequest, LoginResponse
from app.services.auth import AuthService

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=LoginResponse)
def login(requests: LoginRequest, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = AuthService(uow)

    user = service.authenticate(email=requests.email, password=requests.password)

    return LoginResponse(user_id=user.id, message="Authentication successfull")