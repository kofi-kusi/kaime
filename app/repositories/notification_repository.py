from datetime import date, datetime

from sqlmodel import Session, and_, select

from app.models import Event, NotificationDispatch, Subscriber


class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_upcoming_events(self, from_dt: datetime, to_dt: datetime) -> list[Event]:
        statement = (
            select(Event)
            .where(Event.is_active.is_(True))
            .where(and_(Event.start_date >= from_dt, Event.start_date <= to_dt))
        )
        return list(self.session.exec(statement))

    def get_subscribers(self) -> list[Subscriber]:
        return list(self.session.exec(select(Subscriber)))

    def has_dispatch(
        self,
        *,
        event_id: int,
        recipient_email: str,
        channel: str,
        days_before: int,
        scheduled_for: date,
    ) -> bool:
        statement = (
            select(NotificationDispatch.id)
            .where(NotificationDispatch.event_id == event_id)
            .where(NotificationDispatch.recipient_email == recipient_email)
            .where(NotificationDispatch.channel == channel)
            .where(NotificationDispatch.days_before == days_before)
            .where(NotificationDispatch.scheduled_for == scheduled_for)
            .where(NotificationDispatch.status == "sent")
        )
        return self.session.exec(statement).first() is not None

    def record_dispatch(
        self,
        *,
        event_id: int,
        recipient_email: str,
        channel: str,
        days_before: int,
        scheduled_for: date,
        status: str,
        error_message: str | None = None,
    ) -> NotificationDispatch:
        dispatch = NotificationDispatch(
            event_id=event_id,
            recipient_email=recipient_email,
            channel=channel,
            days_before=days_before,
            scheduled_for=scheduled_for,
            status=status,
            error_message=error_message,
        )
        self.session.add(dispatch)
        self.session.commit()
        self.session.refresh(dispatch)
        return dispatch
