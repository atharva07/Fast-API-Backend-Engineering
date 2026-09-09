from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

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

    project_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )