from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.project import Project
    from app.db.models.test_result import TestResult

class TestCase(Base):
    __tablename__ = "test_case"

    id: Mapped[int] = mapped_column(
        Integer, 
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

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    # This is database level relationship
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        nullable=True,
    )

    # This is ORM level relationship
    project: Mapped["Project | None"] = relationship(
        back_populates="test_case"
    )

    results: Mapped[list["TestResult"]] = relationship(
        back_populates="test_case"
    )