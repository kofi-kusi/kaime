from datetime import date, datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field, SQLModel


class Subscriber(SQLModel, table=True):
    __tablename__ = "subscribers"

    name: str = Field(index=True)
    program: str
    email: str = Field(primary_key=True)
    surname: str = Field(index=True)
    other_names: str = Field(index=True)

    @property
    def full_name(self) -> str:
        joined = " ".join(part for part in [self.surname, self.other_names] if part).strip()
        return joined or self.name


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    start_date: datetime
    end_date: datetime | None = Field(default=None)
    notification_days_before: int | None = Field(default=None)
    notification_offsets: list[int] | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )
    email_template: str = Field(default="event_reminder.html")
    is_active: bool = Field(default=True, nullable=False)


class NotificationDispatch(SQLModel, table=True):
    __tablename__ = "notification_dispatches"
    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "recipient_email",
            "channel",
            "days_before",
            "scheduled_for",
            "status",
            name="uq_notification_dispatch_key",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: int = Field(foreign_key="events.id", nullable=False, index=True)
    recipient_email: str = Field(nullable=False, index=True)
    channel: str = Field(default="email", nullable=False, index=True)
    days_before: int = Field(nullable=False)
    scheduled_for: date = Field(nullable=False)
    sent_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    status: str = Field(default="sent", nullable=False)
    error_message: str | None = Field(default=None)


# Backward-compatibility aliases for existing imports.
Subscribers = Subscriber
Events = Event
Mock_Subscribers = Subscriber

    
