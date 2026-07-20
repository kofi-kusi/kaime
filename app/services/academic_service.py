from app.models import Event, Subscriber
from app.repositories.academic_repository import AcademicRepository
from app.schemas import EventCreate, EventUpdate, SubscriberCreate, SubscriberUpdate


class ResourceNotFoundError(Exception):
    pass


class ResourceConflictError(Exception):
    pass


class AcademicService:
    def __init__(self, repository: AcademicRepository):
        self.repository = repository

    def create_subscriber(self, payload: SubscriberCreate) -> Subscriber:
        normalized_email = self._normalize_email(payload.email)
        existing = self.repository.get_subscriber(normalized_email)
        if existing:
            raise ResourceConflictError(f"Subscriber with email {normalized_email} already exists.")
        subscriber = Subscriber.model_validate(payload)
        subscriber.email = normalized_email
        return self.repository.create_subscriber(subscriber)

    def list_subscribers(self) -> list[Subscriber]:
        return self.repository.list_subscribers()

    def get_subscriber(self, email: str) -> Subscriber:
        normalized_email = self._normalize_email(email)
        subscriber = self.repository.get_subscriber(normalized_email)
        if subscriber is None:
            raise ResourceNotFoundError(f"Subscriber with email {normalized_email} was not found.")
        return subscriber

    def update_subscriber(self, email: str, payload: SubscriberUpdate) -> Subscriber:
        subscriber = self.get_subscriber(email)
        updates = payload.model_dump(exclude_none=True)
        for key, value in updates.items():
            setattr(subscriber, key, value)
        self.repository.save()
        self.repository.refresh(subscriber)
        return subscriber

    def delete_subscriber(self, email: str) -> None:
        subscriber = self.get_subscriber(email)
        self.repository.delete_subscriber(subscriber)

    def create_event(self, payload: EventCreate) -> Event:
        self._validate_offsets(payload.notification_offsets)
        event_data = payload.model_dump()
        event_data["email_template"] = str(payload.email_template)
        return self.repository.create_event(Event.model_validate(event_data))

    def list_events(self) -> list[Event]:
        return self.repository.list_events()

    def get_event(self, event_id: int) -> Event:
        event = self.repository.get_event(event_id)
        if event is None:
            raise ResourceNotFoundError(f"Event with id {event_id} was not found.")
        event_dict = event.model_dump()
        event.sqlmodel_update({"body": f"{event_dict['body'][:50]}..."})
        return event

    def update_event(self, event_id: int, payload: EventUpdate) -> Event:
        event = self.get_event(event_id)
        self._validate_offsets(payload.notification_offsets)
        updates = payload.model_dump(exclude_none=True)
        for key, value in updates.items():
            setattr(event, key, value)
        self.repository.save()
        self.repository.refresh(event)
        return event

    def set_event_active(self, event_id: int, is_active: bool) -> Event:
        event = self.get_event(event_id)
        event.is_active = is_active
        self.repository.save()
        self.repository.refresh(event)
        return event

    def delete_event(self, event_id: int) -> None:
        event = self.get_event(event_id)
        self.repository.delete_event(event)

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()

    @staticmethod
    def _validate_offsets(offsets: list[int] | None) -> None:
        if offsets is None:
            return
        if any(value < 0 for value in offsets):
            raise ResourceConflictError("notification_offsets must only include non-negative integers.")
