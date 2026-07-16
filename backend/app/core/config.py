from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DIR = BASE_DIR.parent
_base_config = SettingsConfigDict(
    env_file=(PROJECT_DIR / ".env", BASE_DIR / ".env"),
    env_ignore_empty=True,
    extra="ignore",
)


class AppSettings(BaseSettings):
    APP_NAME: str = "Pharmafly"
    APP_DOMAIN: str = "http://localhost:8000"


class NotificationSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    NOTIFICATION_SCAN_INTERVAL_MINUTES: int = 30
    NOTIFICATION_LOOKAHEAD_DAYS: int = 14
    NOTIFICATION_MAX_RETRIES: int = 3
    NOTIFICATION_RETRY_BACKOFF_SECONDS: int = 3
    NOTIFICATION_TIMEZONE: str = "UTC"
    NOTIFICATION_DEFAULT_OFFSETS: tuple[int, ...] = (7, 3, 1, 0)
    TEMPLATE_DIR: Path = BASE_DIR / "app" / "templates"

    model_config = _base_config


class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = _base_config

    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class SecuritySettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = _base_config


notification_settings = NotificationSettings()
db_settings = DatabaseSettings()
security_settings = SecuritySettings()
app_settings = AppSettings()
