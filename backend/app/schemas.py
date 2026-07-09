from datetime import datetime

from sqlmodel import SQLModel


class SubscriberCreate(SQLModel):
    name: str
    program: str
    email: str
    surname: str
    other_names: str


class SubscriberUpdate(SQLModel):
    name: str | None = None
    program: str | None = None
    surname: str | None = None
    other_names: str | None = None


class SubscriberRead(SQLModel):
    name: str
    program: str
    email: str
    surname: str
    other_names: str


class EventCreate(SQLModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime | None = None
    notification_days_before: int | None = None
    notification_offsets: list[int] | None = None
    email_template: str = "event_reminder.html"
    is_active: bool = True


class EventUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    notification_days_before: int | None = None
    notification_offsets: list[int] | None = None
    email_template: str | None = None
    is_active: bool | None = None


class EventRead(SQLModel):
    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime | None
    notification_days_before: int | None
    notification_offsets: list[int] | None
    email_template: str
    is_active: bool
