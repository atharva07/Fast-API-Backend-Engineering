from fastapi import Depends, Cookie, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.security.jwt import decode_access_token
from app.db.models.user import User
from app.db.dependencies import get_unit_of_work
from app.exceptions.auth import InvalidTokenError
from app.db.unit_of_work import UnitOfWork
from app.cache.redis_client import redis_client
from app.services.session import SessionServices

# bearer_scheme = HTTPBearer()

"""
    This is Authentication part, This is JWT based authentication
"""
# def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
#     token = credentials.credentials

#     return decode_access_token(token)

# def get_current_user(user_id: int = Depends(get_current_user_id), uow: UnitOfWork = Depends(get_unit_of_work)) -> User:
#     with uow:
#         user = uow.users.get_by_id(user_id)

#         if user is None:
#             raise InvalidTokenError("User associated with token no longer exists")

#         return user

"""
    This is session-based authentication, using Redis
"""
sessions = SessionServices()

SESSION_COOKIE = "session_id"

def get_current_user_id(
        session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE)
) -> int:
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated"
        )

    session = sessions.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or Invalid"
        )

    user_id = session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Session data"
        )

    return int(user_id)

def get_current_user(
        user_id: int = Depends(get_current_user_id),
        uow: UnitOfWork = Depends(get_unit_of_work)
) -> User:
    with uow:
        # This loads the usr from the SQL
        user = uow.users.get_by_id(user_id)

        if user is None:
            raise InvalidTokenError(
                "User associated with session no longer exists"
            )

        return user