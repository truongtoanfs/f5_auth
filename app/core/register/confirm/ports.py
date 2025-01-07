from typing import Protocol
from .models import RegisterConfirmRequest
from app.libs.mysql.models.user import User


class RegisterConfirmUseCase(Protocol):
    def confirm_register(self, payload: RegisterConfirmRequest, token: str):
        raise NotImplementedError()


class RegisterConfirmPort(Protocol):
    def fetch_register_by_email(self, email: str):
        raise NotImplementedError()

    def fetch_user_by_email(self, email: str):
        raise NotImplementedError()

    def add_user_to_user(self, user: User):
        raise NotImplementedError()

    def delete_register_by_email(self, email: str):
        raise NotImplementedError()
