from typing import Optional
import uuid
from sqlmodel import Field, SQLModel
from datetime import datetime


class User(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=uuid.uuid4)
    email: str = Field(index=True)
    password: str
    password_expired: bool = False
    password_expired_at: Optional[datetime] = None
    phone: Optional[str] = Field(None, max_length=20)
    fullname: str = ""
