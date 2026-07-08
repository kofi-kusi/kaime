from typing import Any

from config import notification_settings
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, NameEmail
from utils import TEMPLATE_DIR


class EmailSchema(BaseModel):
    email: list[NameEmail]
    body: dict[str, Any]


class NotificationService:
    def __init__(self):

        self.fm = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATE_DIR,
            ),
        )

    async def send_email(
        self,
        subject: str,
        email: EmailSchema,
    ):
        await self.fm.send_message(
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
        await self.fm.send_message(
            message=MessageSchema(
                subject=subject,
                recipients=email.model_dump().get("email"),
                template_body=email.model_dump().get("body"),
                subtype=MessageType.html,
            ),
            template_name=template_name,
        )
