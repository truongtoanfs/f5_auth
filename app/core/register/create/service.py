from datetime import datetime, timezone, timedelta
from app.core.register.create.ports import RegisterUserUseCase, RegisterUserPort
from app.core.register.create.models import RegisterUserRequest, RegisterUserResponse
from app.libs.exception.service import UserExistException, UserConfirmedException
from app.libs.common.auth_handler import AuthHandler
from config import apiConfig


class RegisterUserService(RegisterUserUseCase):

    def __init__(self, adapter: RegisterUserPort):
        self.adapter = adapter

    async def register(self, payload: RegisterUserRequest):
        user = await self.adapter.fetch_user_by_email(email=payload.email)
        if user is None:
            raise UserExistException

        current_time = datetime.now(timezone.utc)

        auth_handler = AuthHandler()
        password = auth_handler.generate_random_password()
        hash_password = auth_handler.generate_hash_password(password=password)

        register = await self.adapter.fetch_register_by_email(email=payload.email)
        if register:
            if register.is_confirmed:
                raise UserConfirmedException
            if register.password_expired_at < current_time:
                await self.adapter.update_register_password(
                    email=payload.email,
                    hash_password=hash_password,
                    password_expired=current_time
                    + timedelta(seconds=apiConfig.PASSWORD_EXPIRED),
                )

        return RegisterUserResponse(tmp_token="abcd", retry_time=5)
