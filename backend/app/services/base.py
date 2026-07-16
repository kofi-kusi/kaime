from uuid import UUID

from sqlmodel import Session


class BaseService:
    def __init__(self, model, session: Session):
        self.model = model
        self.session = session

    def _get(self, id: UUID):
        return self.session.get(self.model, id)

    def _add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def _update(self, entity):
        return self._add(entity)

    def _delete(self, entity):
        self.session.delete(entity)