import logging
from collections.abc import Awaitable, Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import NotificationSettings

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(
        self,
        *,
        notification_job: Callable[[], Awaitable[None]],
        settings: NotificationSettings,
    ):
        self.notification_job = notification_job
        self.settings = settings
        self.scheduler = AsyncIOScheduler(timezone=settings.NOTIFICATION_TIMEZONE)

    def start(self) -> None:
        if self.scheduler.running:
            return

        self.scheduler.add_job(
            self.notification_job,
            trigger=IntervalTrigger(minutes=self.settings.NOTIFICATION_SCAN_INTERVAL_MINUTES),
            id="academic-notification-job",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=300,
        )
        self.scheduler.start()
        logger.info(
            "Notification scheduler started: every %s minutes",
            self.settings.NOTIFICATION_SCAN_INTERVAL_MINUTES,
        )

    def shutdown(self) -> None:
        if not self.scheduler.running:
            return
        self.scheduler.shutdown(wait=False)
        logger.info("Notification scheduler shut down")
