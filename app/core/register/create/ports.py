from typing import Protocol
from app.core.register.create.models import RegisterUserRequest


class RegisterUserUseCase(Protocol):
    def register(self, payload: RegisterUserRequest):
        raise NotImplementedError()


class RegisterUserPort(Protocol):
    async def fetch_user_by_email(self, email: str):
        raise NotImplementedError()

    async def fetch_register_by_email(self, email: str):
        raise NotImplementedError()
