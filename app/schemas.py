from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlmodel import SQLModel


class UserBase(BaseModel):
    first_name: str = Field(max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=255)
    phone_number: str = Field(max_length=20)


class UserIn(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime | None = Field(default=None)


class UserUpdateMe(BaseModel):
    first_name: str | None = Field(default=None, max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)


class UsersList(BaseModel):
    users: list[UserOut]
    count: int


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
    body: str
    start_date: datetime
    end_date: datetime | None = None
    notification_days_before: int | None = None
    notification_offsets: list[int] | None = None
    email_template: EventEmailTemplate
    is_active: bool = True


class EventUpdate(SQLModel):
    title: str | None = None
    body: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    notification_days_before: int | None = None
    notification_offsets: list[int] | None = None
    email_template: EventEmailTemplate | None = None
    is_active: bool | None = None


class EventRead(SQLModel):
    id: int
    title: str
    body: str
    start_date: datetime
    end_date: datetime | None
    notification_days_before: int | None
    notification_offsets: list[int] | None
    email_template: EventEmailTemplate
    is_active: bool
