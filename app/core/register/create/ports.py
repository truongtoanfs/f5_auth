from typing import Protocol
from datetime import datetime
from app.core.register.create.models import RegisterUserRequest


class RegisterUserUseCase(Protocol):
    def register(self, payload: RegisterUserRequest):
        raise NotImplementedError()


class RegisterUserPort(Protocol):
    async def fetch_user_by_email(self, email: str):
        raise NotImplementedError()

    async def fetch_register_by_email(self, email: str):
        raise NotImplementedError()

    async def update_register_password(
        self, email: str, hash_password: str, password_expired: datetime
    ):
        raise NotImplementedError()
