import os
from fastapi import APIRouter, Depends, Response
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.auth import LoginRequest, LoginResponse
from app.services.auth import AuthService
from app.services.session import SessionServices

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# Setting up a session based authentication with Redis
session = SessionServices(ttl_seconds=1800)

SESSION_COOKIE = "session_id"
SESSION_TTL = 1800

COOKIE_SECURE = (
    os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
)

@router.post("/login", response_model=LoginResponse)
def login(requests: LoginRequest, response: Response, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = AuthService(uow)

    user_id = service.authenticate(email=requests.email, password=requests.password)

    # access_token = service.authenticate(email=requests.email, password=requests.password)
    
    session_id = session.create_session(user_id)

    response.set_cookie(
        key=SESSION_COOKIE, 
        value=session_id, 
        httponly=True, 
        secure=COOKIE_SECURE, 
        samesite="lax", 
        max_age=SESSION_TTL, 
        path="/"
    )

    return LoginResponse(message="Login Successful")