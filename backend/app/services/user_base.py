from datetime import timedelta
from typing import Generic, TypeVar
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException, status
from pwdlib import PasswordHash
from sqlmodel import Session, col, select

from app.core.config import app_settings, security_settings
from app.core.security import generate_access_token
from app.utils import decode_url_safe_token, generate_url_safe_token
from .user_notifications import NotificationService
from pydantic import BaseModel, EmailStr
from typing import Any

from app.models import User
from .base import BaseService

password_hash = PasswordHash.recommended()

TUser = TypeVar("TUser", bound=User)


class EmailSchema(BaseModel):
    email: list[EmailStr]
    body: dict[str, Any]


class UserBaseService(BaseService, Generic[TUser]):
    def __init__(self, model: type[TUser], session: Session, tasks: BackgroundTasks):
        self.model = model
        self.session = session
        self.notification = NotificationService(tasks=tasks)

    async def _add_user(self, data: dict, router_prefix: str) -> User:
        user = self.model(
            **data,
            password_hash=password_hash.hash(data["password"]),
        )
        user = self._add(user)

        token = generate_url_safe_token({"id": str(user.id)})
        await self.notification.send_email_with_template(
            subject="Welcome to Kaime!",
            email=EmailSchema(
                email=[user.email],
                body={
                    "verify_url": f"{app_settings.APP_DOMAIN}{router_prefix}/verify-email?token={token}",
                    "username": user.first_name,
                },
            ),
            template_name="mail_email_verify.html",
        )

        return user

    def verify_email(self, token: str):
        try:
            token_data = decode_url_safe_token(token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token",
            )
        user = self.session.get(self.model, UUID(token_data["id"]))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        user.email_verified = True
        self._update(user)

    def _read_users(self, skip: int = 0, limit: int = 100):
        statement = (
            select(self.model)
            .order_by(col(self.model.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        users = self.session.exec(statement).all()
        return users

    def _get_user_by_email(self, email: str) -> User | None:
        return self.session.scalar(
            select(self.model).where(self.model.email == email),
        )

    def _generate_token(self, email: str, password: str) -> str:
        user = self._get_user_by_email(email)
        if not user or not password_hash.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return generate_access_token(
            data={
                "sub": str(user.id),
            },
            expires_delta=timedelta(
                minutes=security_settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )

    def _update_user(self, user_id: UUID, data: dict) -> User:
        user = self.session.get(self.model, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.sqlmodel_update(data)
        self._update(user)
        return user

    def send_reset_password_link(self, user: dict):
        token = generate_url_safe_token({"id": str(user["id"])})
        return token

    def reset_password(self, token: str, body: dict):
        try:
            token_data = decode_url_safe_token(token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token",
            )
        user = self.session.get(self.model, UUID(token_data["id"]))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if not password_hash.verify(body["current_password"], user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        user.password_hash = password_hash.hash(body["new_password"])
        self._update(user)
        return user