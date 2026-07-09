from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import NotificationSettings


class EmailNotificationChannel:
    channel_name = "email"

    def __init__(self, settings: NotificationSettings):
        self.mailer = FastMail(
            ConnectionConfig(
                MAIL_USERNAME=settings.MAIL_USERNAME,
                MAIL_PASSWORD=settings.MAIL_PASSWORD,
                MAIL_FROM=settings.MAIL_FROM,
                MAIL_PORT=settings.MAIL_PORT,
                MAIL_SERVER=settings.MAIL_SERVER,
                MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
                MAIL_STARTTLS=settings.MAIL_STARTTLS,
                MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
                USE_CREDENTIALS=settings.USE_CREDENTIALS,
                VALIDATE_CERTS=settings.VALIDATE_CERTS,
            ),
        )

    async def send(self, *, subject: str, recipient: str, html_body: str) -> None:
        await self.mailer.send_message(
            MessageSchema(
                subject=subject,
                recipients=[recipient],
                body=html_body,
                subtype=MessageType.html,
            ),
        )
