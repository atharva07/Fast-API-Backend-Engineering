from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.execute(
            select(User).where(
                User.id == user_id
            )
        ).scalar_one_or_none()

    def get_by_email(self, email_id: str) -> User | None:
        return self.db.execute(
            select(User).where(
                User.email == email_id
            )
        ).scalar_one_or_none()

    def get_all(self) -> list[User]:
        return self.db.execute(
            select(User)
        ).scalars().all()

    def add(self, user: User) -> User:
        self.db.add(user)
        return user