from sqlalchemy.exc import IntegrityError
from app.db.models.user import User
from app.db.unit_of_work import UnitOfWork
from app.exceptions.user import UserAlreadyExistsExceptions, UserNotFoundError
from app.security.password import hash_password

class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def create_user(self, name: str, email: str, password: str) -> User:
        with self.uow:
            existing_user = self.uow.users.get_by_email(email)

            if existing_user is not None:
                raise UserAlreadyExistsExceptions("User with this email already exists")

            hashed_password = hash_password(password)

            user = User(
                name=name,
                email=email,
                password_hash=hashed_password
            )

            self.uow.users.add(user)

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

            return user

    def get_user(self, user_id: int) -> User:
        with self.uow:
            user = self.uow.users.get_by_id(user_id)

            if user is None:
                raise UserNotFoundError("User Not Found")

            return user

    def get_users(self) -> list[User]:
        with self.uow:
            return self.uow.users.get_all()
        