from .ports import RegisterConfirmUseCase, RegisterConfirmPort
from .models import RegisterConfirmRequest, RegisterConfirmResponseData
from app.libs.common.auth_handler import AuthHandler
from app.libs.exception.service import (
    UserNotExitException,
    PasswordInvalidException,
    UserExistException,
)
from app.libs.mysql.models.register import Register
from app.libs.mysql.models.user import User
from app.libs.common.constants import EXPIRE_TOKEN
from app.libs.redis.redis_client import RedisClient
from app.libs.redis.constants import redis_verify_access_token


class RegisterConfirmService(RegisterConfirmUseCase):

    def __init__(self, adapter: RegisterConfirmPort):
        self.adapter = adapter

    def confirm_register(self, payload: RegisterConfirmRequest, token: str):
        auth_handler = AuthHandler()
        token_data: dict = auth_handler.decode_token(token=token)
        email = token_data.get("email")

        user: User = self.adapter.fetch_user_by_email(email=email)
        if user:
            raise UserExistException

        register_user: Register = self.adapter.fetch_register_by_email(email=email)
        if register_user is None:
            raise UserNotExitException
        if not auth_handler.verify_hash_password(
            plain_password=payload.password, hashed_password=register_user.password
        ):
            raise PasswordInvalidException

        user = User(email=email, password=register_user.password)
        self.adapter.add_user_to_user(user)

        self.adapter.update_confirm_register(email=email)

        access_token = auth_handler.generate_token(
            data=dict(email=email),
            expires_delta=EXPIRE_TOKEN["SESSION"],
        )

        redis_client = RedisClient()
        redis_client.set(
            key=redis_verify_access_token.format(email=email), value=access_token
        )
        return RegisterConfirmResponseData(access_token=access_token)
