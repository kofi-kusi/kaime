# Kaime

Kaime is an academic notification platform that keeps students informed about
university events, exams, and deadlines without manual effort. Staff manage
subscribers and events through a dashboard, and Kaime automatically schedules
and sends reminder emails as those events approach.

The project has two parts:

- **Backend** — a FastAPI service (Python) that stores subscribers/events in
  PostgreSQL and runs a background scheduler that dispatches notifications.
- **Frontend** — a React + Vite dashboard for managing subscribers and events,
  built and served as static files by the backend.

## How it works

1. Staff create **events** (e.g. exam dates, registration deadlines) with a
   title, body, date range, and one or more notification offsets (how many
   days before the event a reminder should go out).
2. **Subscribers** (students) are registered with contact details.
3. A background scheduler periodically checks for due notifications, renders
   the appropriate Jinja2 email template, and dispatches it through a
   pluggable notification channel (email today; SMS/push can be added later).
4. Each dispatch is recorded to guarantee idempotency — a subscriber won't be
   notified twice for the same event/offset.

## Why APScheduler here?

APScheduler is the best fit for this service because reminders are time-based,
lightweight, and run inside the FastAPI process with no extra broker. It keeps
deployment simple while still supporting interval/cron jobs, concurrency
controls, and misfire handling.

For horizontal scaling or heavy queue workloads, migrate the
`NotificationChannel` pipeline to Celery workers later without changing the
orchestration contract.

## Tech stack

- **Backend**: FastAPI, SQLModel/SQLAlchemy, PostgreSQL, Alembic migrations,
  APScheduler, Jinja2 templates, fastapi-mail.
- **Frontend**: React 19, React Router, TypeScript, Vite, Tailwind CSS.

## Quick start

1. Copy config:

   ```bash
   cp .env.example ./.env
   ```

2. Start the API (backend):

   ```bash
   uv run fastapi dev
   ```

3. Run the dashboard (frontend), in a separate shell:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   build the frontend (`npm run build`) — the FastAPI app
   serves the resulting `frontend/dist` directory directly (see
   `app/main.py`).

## Notification architecture

- `app/services/notification_service.py` orchestrates due checks, rendering,
  retries, and idempotency.
- `app/services/scheduler_service.py` manages periodic execution with
  APScheduler.
- `app/services/channels/base.py` defines the channel contract for
  email/SMS/push extensibility.
- `app/services/channels/email.py` sends email notifications.
- `app/services/template_renderer.py` renders Jinja2 templates from
  `app/templates/`.
- `app/repositories/notification_repository.py` isolates data access and
  dispatch tracking.
- `app/main.py` wires scheduler startup/shutdown using FastAPI lifespan, and
  mounts the built frontend.

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

When creating or updating events, `email_template` is restricted to the
built-in template enum values (for example `event_reminder.html`,
`exam_reminder.html`, `deadline_reminder.html`, `registration_open.html`).

Interactive API docs are available at `/docs` once the backend is running.
