from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.associations import ProjectUser
    from app.db.models.test_suite import TestSuite

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    execution_timeout: Mapped[int] = mapped_column(
        nullable=False,
        default=3000,
    )

    test_suites: Mapped[list["TestSuite"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )

    # A Project can have multiple project users as an object
    project_users: Mapped[list["ProjectUser"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )