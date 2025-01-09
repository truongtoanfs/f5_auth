from typing import Protocol
from app.core.user.forget.models import (
    ForgetUserRequest,
    ForgetUserConfirmRequest,
    ForgetUserResetRequest,
)


class UserForgetUseCase(Protocol):
    def get_confirm_code(self, payload: ForgetUserRequest):
        raise NotImplementedError()

    def confirm_code(self, payload: ForgetUserConfirmRequest, token: str):
        raise NotImplementedError()

    def reset_password(self, payload: ForgetUserResetRequest):
        raise NotImplementedError()


class UserForgetPort(Protocol):
    def get_user_by_email(self, email: str):
        raise NotImplementedError()

    def get_register_by_email(self, email: str):
        raise NotImplementedError()

    def update_password_register(self, email: str, password: str):
        raise NotImplementedError()

    def update_password_user(self, email: str, password: str):
        raise NotImplementedError()
