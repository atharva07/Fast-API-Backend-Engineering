from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.test_result import TestResult
    from app.db.models.test_suite import TestSuite

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
        nullable=False,
        default="DRAFT" 
    )

    # This is database level relationship
    suite_id: Mapped[int] = mapped_column(
        ForeignKey(
            "test_suites.id",
            ondelete="CASCADE"
        ),
        nullable=False,
    )

    # This is ORM level relationship
    results: Mapped[list["TestResult"]] = relationship(
        back_populates="test_case",
        cascade="all, delete-orphan"
    )

    suite: Mapped["TestSuite"] = relationship(
        back_populates="test_cases"
    )