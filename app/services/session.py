import json
import secrets
from app.cache.redis_client import redis_client

class SessionServices:
    def __init__(self, ttl_seconds: int = 1800):
        if ttl_seconds <= 0:
            raise ValueError("Session TTL must be prositive")

        self.ttl_seconds = ttl_seconds

    def create_session(self, user_id: int) -> str:
        session_id = secrets.token_urlsafe(32)

        session_data = {
            "user_id": user_id,
        }

        redis_client.set(
            f"session:{session_id}",
            json.dumps(session_data),
            ex=self.ttl_seconds,
        )

        return session_id

    def get_session(self, session_id: str) -> dict | None:
        value = redis_client.get(f"session:{session_id}")

        if value is None:
            return None

        return json.loads(value)

    def delete_session(self, session_id: str) -> None:
        redis_client.delete(f"session:{session_id}")