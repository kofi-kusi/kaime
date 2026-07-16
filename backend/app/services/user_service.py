from fastapi import BackgroundTasks
from sqlmodel import Session

from app.schemas import UserIn, UserUpdateMe
from app.core.security import Token
from app.models import User

from .user_base import UserBaseService


class UserService(UserBaseService):
    def __init__(self, session: Session, tasks: BackgroundTasks):
        super().__init__(model=User, session=session, tasks=tasks)

    async def add(self, user_in: UserIn, router_prefix: str) -> User:
        return await self._add_user(
            user_in.model_dump(exclude_unset=True),
            router_prefix=router_prefix,
        )

    def read_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self._read_users(skip, limit)

    def token(self, email: str, password: str) -> Token:
        return Token(
            access_token=self._generate_token(email, password),
            token_type="bearer",
        )

    def update(self, user: User, user_update: UserUpdateMe):
        return self._update_user(
            user.id,
            user_update.model_dump(exclude_unset=True),
        )