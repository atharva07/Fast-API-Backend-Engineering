from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.db.models.associations import project_users

if TYPE_CHECKING:
    from app.db.models.test_case import TestCase
    from app.db.models.user import User

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    test_case: Mapped[list["TestCase"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )

    users: Mapped[list["User"]] = relationship(
        secondary=project_users,
        back_populates="projects"
    )

    execution_timeout: Mapped[int] = mapped_column(
        nullable=False,
        default=3000,
    )