from typing import Any

from pydantic import BaseModel, EmailStr

from app.core.config import notification_settings
from app.services.channels.email import EmailNotificationChannel
from app.services.template_renderer import TemplateRenderer


class EmailSchema(BaseModel):
    email: list[EmailStr]
    body: dict[str, Any]


class NotificationService:
    def __init__(self):
        self.channel = EmailNotificationChannel(settings=notification_settings)
        self.renderer = TemplateRenderer(template_dir=notification_settings.TEMPLATE_DIR)

    async def send_email(self, subject: str, email: EmailSchema):
        for recipient in email.email:
            await self.channel.send(
                subject=subject,
                recipient=str(recipient),
                html_body=str(email.body),
            )

    async def send_email_with_template(
        self,
        subject: str,
        email: EmailSchema,
        template_name: str,
    ):
        for recipient in email.email:
            payload = email.body | {"student_name": str(recipient).split("@")[0]}
            html_body = self.renderer.render(template_name, payload)
            await self.channel.send(
                subject=subject,
                recipient=str(recipient),
                html_body=html_body,
            )
