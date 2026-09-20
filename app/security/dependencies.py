from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.security.jwt import decode_access_token
from app.db.models.user import User
from app.db.dependencies import get_unit_of_work
from app.exceptions.auth import InvalidTokenError
from app.db.unit_of_work import UnitOfWork

bearer_scheme = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
    token = credentials.credentials

    return decode_access_token(token)

def get_current_user(user_id: int = Depends(get_current_user_id), uow: UnitOfWork = Depends(get_unit_of_work)) -> User:
    with uow:
        user = uow.users.get_by_id(user_id)

        if user is None:
            raise InvalidTokenError("User associated with token no longer exists")

        return user