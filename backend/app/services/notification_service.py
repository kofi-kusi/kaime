import logging
import asyncio
from datetime import datetime, timedelta, timezone

from app.core.config import NotificationSettings
from app.models import Event, Subscriber
from app.repositories.notification_repository import NotificationRepository
from app.services.channels.base import NotificationChannel
from app.services.template_renderer import TemplateRenderer

logger = logging.getLogger(__name__)


class NotificationOrchestratorService:
    def __init__(
        self,
        *,
        repository: NotificationRepository,
        renderer: TemplateRenderer,
        email_channel: NotificationChannel,
        settings: NotificationSettings,
    ):
        self.repository = repository
        self.renderer = renderer
        self.email_channel = email_channel
        self.settings = settings

    async def process_due_notifications(self, now: datetime | None = None) -> None:
        current_time = now or datetime.now(tz=timezone.utc)
        lookahead = timedelta(days=self.settings.NOTIFICATION_LOOKAHEAD_DAYS)
        events = self.repository.get_upcoming_events(
            from_dt=current_time,
            to_dt=current_time + lookahead,
        )
        subscribers = self.repository.get_subscribers()

        for event in events:
            await self._process_event(event=event, subscribers=subscribers, now=current_time)

    async def _process_event(
        self,
        *,
        event: Event,
        subscribers: list[Subscriber],
        now: datetime,
    ) -> None:
        event_date = event.start_date.date()
        if event.id is None:
            logger.warning("Skipping event with empty primary key: %s", event.title)
            return

        days_remaining = (event_date - now.date()).days

        if days_remaining < 0:
            return

        if days_remaining not in self._resolve_offsets(event):
            return

        for subscriber in subscribers:
            if self.repository.has_dispatch(
                event_id=event.id,
                recipient_email=subscriber.email,
                channel=self.email_channel.channel_name,
                days_before=days_remaining,
                scheduled_for=event_date,
            ):
                continue

            context = {
                "student_name": subscriber.full_name,
                "event_title": event.title,
                "description": event.description,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "days_remaining": days_remaining,
            }
            html_body = self.renderer.render(event.email_template, context)
            subject = self._build_subject(event.title, days_remaining)

            try:
                await self._send_with_retry(
                    subject=subject,
                    recipient=subscriber.email,
                    html_body=html_body,
                )
            except Exception as exc:
                logger.exception(
                    "Failed to send notification for event_id=%s recipient=%s",
                    event.id,
                    subscriber.email,
                )
                self.repository.record_dispatch(
                    event_id=event.id,
                    recipient_email=subscriber.email,
                    channel=self.email_channel.channel_name,
                    days_before=days_remaining,
                    scheduled_for=event_date,
                    status="failed",
                    error_message=str(exc),
                )
                continue

            self.repository.record_dispatch(
                event_id=event.id,
                recipient_email=subscriber.email,
                channel=self.email_channel.channel_name,
                days_before=days_remaining,
                scheduled_for=event_date,
                status="sent",
            )

    def _resolve_offsets(self, event: Event) -> set[int]:
        configured = event.notification_offsets
        if configured:
            return {value for value in configured if value >= 0}

        if event.notification_days_before is not None and event.notification_days_before >= 0:
            return {event.notification_days_before}

        return {value for value in self.settings.NOTIFICATION_DEFAULT_OFFSETS if value >= 0}

    async def _send_with_retry(self, *, subject: str, recipient: str, html_body: str) -> None:
        max_retries = max(1, self.settings.NOTIFICATION_MAX_RETRIES)
        backoff = max(1, self.settings.NOTIFICATION_RETRY_BACKOFF_SECONDS)

        for attempt in range(1, max_retries + 1):
            try:
                await self.email_channel.send(
                    subject=subject,
                    recipient=recipient,
                    html_body=html_body,
                )
                return
            except Exception:
                if attempt == max_retries:
                    raise
                await asyncio.sleep(backoff * attempt)

    @staticmethod
    def _build_subject(event_title: str, days_remaining: int) -> str:
        if days_remaining == 0:
            return f"Today: {event_title}"
        if days_remaining == 1:
            return f"Reminder: {event_title} starts tomorrow"
        return f"Reminder: {event_title} starts in {days_remaining} days"
