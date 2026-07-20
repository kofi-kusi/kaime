from sqlmodel import Session, delete, select

from app.models import Event, NotificationDispatch, Subscriber


class AcademicRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_subscriber(self, subscriber: Subscriber) -> Subscriber:
        subscriber_dict = subscriber.model_dump()
        subscriber = Subscriber(
            **subscriber_dict,
            email = subscriber_dict["email"].strip(),
        )
        self.session.add(subscriber)
        self.session.commit()
        self.session.refresh(subscriber)
        return subscriber

    def list_subscribers(self) -> list[Subscriber]:
        return list(self.session.exec(select(Subscriber).order_by(Subscriber.surname, Subscriber.name)))

    def get_subscriber(self, email: str) -> Subscriber | None:
        return self.session.get(Subscriber, email)

    def delete_subscriber(self, subscriber: Subscriber) -> None:
        self.session.delete(subscriber)
        self.session.commit()

    def create_event(self, event: Event) -> Event:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def list_events(self) -> list[Event]:
        return list(self.session.exec(select(Event).order_by(Event.start_date)))

    def get_event(self, event_id: int) -> Event | None:
        return self.session.get(Event, event_id)

    def delete_event(self, event: Event) -> None:
        if event.id is not None:
            self.session.exec(
                delete(NotificationDispatch).where(
                    NotificationDispatch.event_id == event.id
                )
            )
        self.session.delete(event)
        self.session.commit()

    def save(self) -> None:
        self.session.commit()

    def refresh(self, entity: Subscriber | Event) -> None:
        self.session.refresh(entity)
