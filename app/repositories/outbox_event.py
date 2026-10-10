from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.outbox_event import OutboxEvent
from datetime import datetime, timedelta

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
            .with_for_update(
                skip_locked=True
            )
        ).scalars().all()

    def reset_stuck_events(
        self, 
        timeout_minutes: int = 10
    ) -> int:
        cutoff = datetime.utcnow() - timedelta(
            minutes=timeout_minutes
        )

        events = self.db.execute(
            select(OutboxEvent)
            .where(
                OutboxEvent.status == "PROCESSING",
                OutboxEvent.processing_started_at < cutoff
            )
            .with_for_update(
                skip_locked=True
            )
        ).scalars().all()

        for event in events:
            event.status = "PENDING"
            event.processing_started_at = None

        self.db.commit()

        return len(events)

    def claim_pending_event(
        self
    ) -> OutboxEvent | None:
        event = self.db.execute(
            select(OutboxEvent)
            .where(
                OutboxEvent.status == "PENDING"
            )
            .order_by(OutboxEvent.id)
            .with_for_update(skip_locked=True)
            .limit(1)
        ).scalar_one_or_none()

        if event is None:
            return None

        event.status = "PROCESSING"
        event.processing_started_at = datetime.utcnow()

        self.db.commit()

        return event