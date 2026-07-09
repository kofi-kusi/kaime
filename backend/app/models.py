from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import uuid4

class Subscribers(SQLModel, table=True):
    name: str = Field(index=True)
    program: str
    email: str = Field(primary_key=True)
    surname: str = Field(index=True)
    other_names: str = Field(index=True)

class Mock_Subscribers(Subscribers):
    pass
    
class Events(SQLModel, table=True):
    id: int = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str
    start_date: datetime | None = Field(default=None)
    end_date: datetime | None = Field(default=None)
    notification_days_before: int | None = Field(default=None)
    email_template: str | None = Field(default=None)

    
