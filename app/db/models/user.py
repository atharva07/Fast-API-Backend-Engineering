from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.db.models.associations import ProjectUser
from app.models.role import UserRole

if TYPE_CHECKING:
    from app.db.models.associations import ProjectUser

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    project_users: Mapped[list["ProjectUser"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    user_role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=UserRole.VIEWER.value
    )