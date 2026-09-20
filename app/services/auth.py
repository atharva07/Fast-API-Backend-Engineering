from app.db.unit_of_work import UnitOfWork
from app.exceptions.auth import InvalidCredentialsError
from app.security.password import verify_password

class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def authenticate(self, email: str, password: str):
        with self.uow:
            user = self.uow.users.get_by_email(email)

            if user is None:
                raise InvalidCredentialsError("Invalid Email or Password")

            if not verify_password(password, user.password_hash):
                raise InvalidCredentialsError("Invalid Email or Password")

            return user