from .models import LoginRequest
from typing import Protocol

class LoginUseCase(Protocol):
    def login(self, payload: LoginRequest):
        raise NotImplemented
    

class LoginPort(Protocol):
    async def fetch_user_by_email(self, email: str):
        raise NotImplementedError()

