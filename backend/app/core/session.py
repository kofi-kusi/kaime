from sqlmodel import Session, create_engine
from app.core.config import db_settings


engine = create_engine(
    url=db_settings.POSTGRES_URL,
    echo=True,
)

def get_session():
    with Session(engine) as session:
        yield session