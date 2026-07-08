from sqlmodel import SQLModel, Field

class Subscribers(SQLModel, table=True):
    name: str = Field(index=True)
    program: str
    email: str = Field(primary_key=True)
    surname: str = Field(index=True)
    other_names: str = Field(index=True)