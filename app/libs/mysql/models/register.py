from typing import Optional
import uuid
from sqlmodel import Field, SQLModel
from datetime import datetime, timedelta, timezone
from config import apiConfig


class Register(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=uuid.uuid4)
    email: str = Field(index=True)
    password: str
    password_expired_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        + timedelta(seconds=apiConfig.PASSWORD_EXPIRED),
    )
    is_confirmed: bool = False
    confirmed_at: Optional[datetime] = None
    resend_verification_count: int = 0
    resend_verification_blocked_at: Optional[datetime] = None
