from datetime import datetime
from enum import StrEnum

from sqlmodel import SQLModel


class EventEmailTemplate(StrEnum):
    ANNOUNCEMENT = "announcement.html"
    DEADLINE_REMINDER = "deadline_reminder.html"
    EVENT_REMINDER = "event_reminder.html"
    EXAM_REMINDER = "exam_reminder.html"
    REGISTRATION_CLOSING = "registration_closing.html"
    REGISTRATION_OPEN = "registration_open.html"
    REGISTRATION_REMINDER = "registration_reminder.html"
    RESULTS_PUBLISHED = "results_published.html"
    RESULTS_PUBLISHED_REMINDER = "results_published_reminder.html"
    UPCOMING_EVENT_REMINDER = "upcoming_event_reminder.html"
    VAC_RE_OPENING_REMINDER = "vac-re-opening_reminder.html"


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
    email_template: EventEmailTemplate = EventEmailTemplate.EVENT_REMINDER
    is_active: bool = True


class EventUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    notification_days_before: int | None = None
    notification_offsets: list[int] | None = None
    email_template: EventEmailTemplate | None = None
    is_active: bool | None = None


class EventRead(SQLModel):
    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime | None
    notification_days_before: int | None
    notification_offsets: list[int] | None
    email_template: EventEmailTemplate
    is_active: bool
