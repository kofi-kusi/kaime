import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session

from app.core.config import notification_settings
from app.core.session import engine
from app.repositories.notification_repository import NotificationRepository
from app.routers.events import router as events_router
from app.routers.subscribers import router as subscribers_router
from app.services.channels.email import EmailNotificationChannel
from app.services.notification_service import NotificationOrchestratorService
from app.services.scheduler_service import SchedulerService
from app.services.template_renderer import TemplateRenderer

logger = logging.getLogger(__name__)


def build_notification_orchestrator() -> NotificationOrchestratorService:
    session = Session(engine)
    repository = NotificationRepository(session=session)
    renderer = TemplateRenderer(template_dir=notification_settings.TEMPLATE_DIR)
    email_channel = EmailNotificationChannel(settings=notification_settings)
    return NotificationOrchestratorService(
        repository=repository,
        renderer=renderer,
        email_channel=email_channel,
        settings=notification_settings,
    )


async def run_notification_cycle() -> None:
    orchestrator = build_notification_orchestrator()
    try:
        await orchestrator.process_due_notifications()
    finally:
        orchestrator.repository.session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = SchedulerService(
        notification_job=run_notification_cycle,
        settings=notification_settings,
    )
    scheduler.start()
    app.state.scheduler = scheduler
    logger.info("Application startup complete")
    yield
    scheduler.shutdown()
    logger.info("Application shutdown complete")


app = FastAPI(lifespan=lifespan, title="Academic Notification Service")
app.include_router(subscribers_router)
app.include_router(events_router)


@app.get("/")
def main():
    return {"message": "Academic notification service is running"}


@app.post("/internal/notifications/run")
async def run_notifications_now():
    await run_notification_cycle()
    return {"status": "ok"}
