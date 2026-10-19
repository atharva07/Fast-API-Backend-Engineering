from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from datetime import datetime
from sqlalchemy import DateTime

if TYPE_CHECKING:
    from app.db.models.test_case import TestCase

class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    test_case_id: Mapped[int] = mapped_column(
        ForeignKey(
            "test_case.id",
            ondelete="CASCADE",
        ),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    processing_started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    test_case: Mapped["TestCase"] = relationship(
        back_populates="results"
    )

    