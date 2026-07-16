from typing import Any

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr

from app.core.config import user_notification_settings
from app.utils import TEMPLATE_DIR


class EmailSchema(BaseModel):
    email: list[EmailStr]
    body: dict[str, Any]


class NotificationService:
    def __init__(self, tasks: BackgroundTasks):
        self.tasks = tasks
        self.fm = FastMail(
            ConnectionConfig(
                **user_notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATE_DIR / "user-email-templates",
            ),
        )

    async def send_email(
        self,
        subject: str,
        email: EmailSchema,
    ):
        self.tasks.add_task(
            self.fm.send_message,
            message=MessageSchema(
                subject=subject,
                recipients=email.model_dump().get("email"),
                body=email.model_dump().get("body"),
                subtype=MessageType.plain,
            ),
        )

    async def send_email_with_template(
        self,
        subject: str,
        email: EmailSchema,
        template_name: str,
    ):
        self.tasks.add_task(
            self.fm.send_message,
            message=MessageSchema(
                subject=subject,
                recipients=email.model_dump().get("email"),
                template_body=email.model_dump().get("body"),
                subtype=MessageType.html,
            ),
            template_name=template_name,
        )