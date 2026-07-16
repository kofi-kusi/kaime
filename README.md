# Backend

Academic notification backend using **FastAPI**, **SQLModel/PostgreSQL**, **APScheduler**, and **Jinja2** templates.

## Why APScheduler here?

APScheduler is the best fit for this service because reminders are time-based, lightweight, and run inside the FastAPI process with no extra broker. It keeps deployment simple while still supporting interval/cron jobs, concurrency controls, and misfire handling.

For horizontal scaling or heavy queue workloads, migrate the `NotificationChannel` pipeline to Celery workers later without changing the orchestration contract.

## Quick start

1. Copy config:

```bash
cp .env.example ../.env
```

1. Start API:

```bash
uv run fastapi dev app/main.py
```

## Notification architecture

- `app/services/notification_service.py` orchestrates due checks, rendering, retries, and idempotency.
- `app/services/scheduler_service.py` manages periodic execution with APScheduler.
- `app/services/channels/base.py` defines channel contract for email/SMS/push extensibility.
- `app/services/channels/email.py` sends email notifications.
- `app/services/template_renderer.py` renders Jinja2 templates from `app/templates/`.
- `app/repositories/notification_repository.py` isolates data access and dispatch tracking.
- `app/main.py` wires scheduler startup/shutdown using FastAPI lifespan.

## Running a manual cycle

Use the internal endpoint to trigger processing immediately:

```bash
curl -X POST http://localhost:8000/internal/notifications/run
```

## API endpoints

- Subscribers:
  - `POST /subscribers`
  - `GET /subscribers`
  - `GET /subscribers/{email}`
  - `PATCH /subscribers/{email}`
  - `DELETE /subscribers/{email}`
- Events:
  - `POST /events`
  - `GET /events`
  - `GET /events/{event_id}`
  - `PATCH /events/{event_id}`
  - `PATCH /events/{event_id}/activate`
  - `PATCH /events/{event_id}/deactivate`
  - `DELETE /events/{event_id}`

When creating or updating events, `email_template` is restricted to the built-in template enum values (for example `event_reminder.html`, `exam_reminder.html`, `deadline_reminder.html`, `registration_open.html`).
