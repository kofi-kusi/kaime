from typing import Protocol


class NotificationChannel(Protocol):
    channel_name: str

    async def send(self, *, subject: str, recipient: str, html_body: str) -> None: ...
