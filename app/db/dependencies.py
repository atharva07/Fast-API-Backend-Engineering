from collections.abc import Generator
from app.db.database import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()

    print("DATABASE SESSION CREATED")

    try:
        yield db
    finally:
        print("DATABASE SESSION CLOSING")
        db.close()