from datetime import date, datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import JSON, Column, DateTime, UniqueConstraint
from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    phone_number: str = Field(max_length=20)
    email_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    password_hash: str = Field(exclude=True)


class User(UserBase, table=True):
    first_name: str = Field(max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str = Field(max_length=100)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )


class Subscriber(SQLModel, table=True):
    __tablename__ = "subscribers"

    name: str = Field(index=True)
    program: str
    email: str = Field(primary_key=True)
    surname: str = Field(index=True)
    other_names: str | None = Field(index=True)

    @property
    def full_name(self) -> str:
        joined = " ".join(
            part for part in [self.surname, self.other_names] if part
        ).strip()
        return joined or self.name


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str
    start_date: datetime
    end_date: datetime | None = Field(default=None)
    notification_days_before: int | None = Field(default=None, gt=-1)
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
