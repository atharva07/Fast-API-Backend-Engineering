from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.outbox_event import OutboxEvent

class OutboxEventRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, event: OutboxEvent) -> OutboxEvent:
        self.db.add(event)

        return event

    def get_pending_events(self) -> list[OutboxEvent]:
        return self.db.execute(
            select(OutboxEvent)
            .where(
                OutboxEvent.status == "PENDING"
            )
            .order_by(OutboxEvent.id)
        ).scalars().all()