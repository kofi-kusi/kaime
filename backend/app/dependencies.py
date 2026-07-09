from collections.abc import Generator

from fastapi import Depends
from sqlmodel import Session

from app.core.config import NotificationSettings, notification_settings
from app.core.session import get_session
from app.repositories.academic_repository import AcademicRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.academic_service import AcademicService
from app.services.channels.email import EmailNotificationChannel
from app.services.notification_service import NotificationOrchestratorService
from app.services.template_renderer import TemplateRenderer


def get_notification_settings() -> NotificationSettings:
    return notification_settings


def get_template_renderer(
    settings: NotificationSettings = Depends(get_notification_settings),
) -> TemplateRenderer:
    return TemplateRenderer(template_dir=settings.TEMPLATE_DIR)


def get_email_channel(
    settings: NotificationSettings = Depends(get_notification_settings),
) -> EmailNotificationChannel:
    return EmailNotificationChannel(settings=settings)


def get_notification_repository(
    session: Session = Depends(get_session),
) -> NotificationRepository:
    return NotificationRepository(session=session)


def get_notification_service(
    repository: NotificationRepository = Depends(get_notification_repository),
    renderer: TemplateRenderer = Depends(get_template_renderer),
    email_channel: EmailNotificationChannel = Depends(get_email_channel),
    settings: NotificationSettings = Depends(get_notification_settings),
) -> NotificationOrchestratorService:
    return NotificationOrchestratorService(
        repository=repository,
        renderer=renderer,
        email_channel=email_channel,
        settings=settings,
    )


def get_academic_repository(
    session: Session = Depends(get_session),
) -> AcademicRepository:
    return AcademicRepository(session=session)


def get_academic_service(
    repository: AcademicRepository = Depends(get_academic_repository),
) -> AcademicService:
    return AcademicService(repository=repository)


def get_db_session() -> Generator[Session, None, None]:
    yield from get_session()
