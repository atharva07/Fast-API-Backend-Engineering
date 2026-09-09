from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://localhost/qaforge"

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    bind=engine,
    # Sends pending SQL to PostgreSQL within the current transaction
    autoflush=False,
    # Commits the Transaction
    autocommit=False
)