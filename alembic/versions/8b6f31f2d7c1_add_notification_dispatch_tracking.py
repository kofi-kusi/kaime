"""Add notification dispatch tracking

Revision ID: 8b6f31f2d7c1
Revises: d09c9b5f28ee
Create Date: 2026-07-09 14:20:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "8b6f31f2d7c1"
down_revision: Union[str, Sequence[str], None] = "d09c9b5f28ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("events", sa.Column("notification_offsets", sa.JSON(), nullable=True))
    op.add_column(
        "events",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )

    op.create_table(
        "notification_dispatches",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("recipient_email", sa.String(), nullable=False),
        sa.Column("channel", sa.String(), nullable=False),
        sa.Column("days_before", sa.Integer(), nullable=False),
        sa.Column("scheduled_for", sa.Date(), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "event_id",
            "recipient_email",
            "channel",
            "days_before",
            "scheduled_for",
            "status",
            name="uq_notification_dispatch_key",
        ),
    )
    op.create_index(
        "ix_notification_dispatches_event_id",
        "notification_dispatches",
        ["event_id"],
        unique=False,
    )
    op.create_index(
        "ix_notification_dispatches_channel",
        "notification_dispatches",
        ["channel"],
        unique=False,
    )
    op.create_index(
        "ix_notification_dispatches_recipient_email",
        "notification_dispatches",
        ["recipient_email"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_notification_dispatches_recipient_email", table_name="notification_dispatches")
    op.drop_index("ix_notification_dispatches_channel", table_name="notification_dispatches")
    op.drop_index("ix_notification_dispatches_event_id", table_name="notification_dispatches")
    op.drop_table("notification_dispatches")
    op.drop_column("events", "is_active")
    op.drop_column("events", "notification_offsets")
