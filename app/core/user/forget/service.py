from datetime import datetime, timezone
from .ports import UserForgetUseCase, UserForgetPort
from app.core.user.forget.models import (
    ForgetUserRequest,
    ForgetUserConfirmRequest,
    ForgetUserResetRequest,
    ForgetUserResponse,
    ForgetUserConfirmData,
    ForgetUserResetData,
)
from app.libs.exception.service import (
    UserNotExitException,
    PasswordInvalidException,
    BlockedEmailException,
    SendEmailTimeException,
)
from app.libs.common.auth_handler import AuthHandler
from app.libs.mail.send_mail import send_mail
from app.libs.common.constants import EXPIRE_TOKEN, RESEND_VERIFICATION
from app.libs.mysql.models.register import Register
from app.libs.redis.redis_client import RedisClient
from app.libs.redis.constants import redis_verify_access_token
from app.libs.exception.service import TokenException
from app.libs.redis.constants import (
    redis_forget_sended_confirm_count,
    redis_forget_sended_confirm_time,
)
from app.libs.common.utils import seconds_left


class ForgetUserService(UserForgetUseCase):
    def __init__(self, adapter: UserForgetPort):
        self.adapter = adapter

    def __check_send_email_attempts(self, email: str):
        redis_client = RedisClient()

        sended_count = redis_client.get(
            key=redis_forget_sended_confirm_count.format(email=email)
        )

        register_timestamp = redis_client.get(
            key=redis_forget_sended_confirm_time.format(email=email)
        )
        current_timestamp = int(datetime.now(timezone.utc).timestamp())
        if sended_count is None:
            redis_client.set(
                key=redis_forget_sended_confirm_count.format(email=email),
                value=1,
                ex=seconds_left(),
            )
            redis_client.set(
                key=redis_forget_sended_confirm_time.format(email=email),
                value=current_timestamp,
                ex=seconds_left(),
            )
            return

        if int(sended_count) > 3:
            raise BlockedEmailException

        # check resend 60s, 90s, 120s
        next_timestamp = int(register_timestamp) + int(sended_count) * 30 + 30
        retry_time = next_timestamp - current_timestamp
        if retry_time > 0:
            raise SendEmailTimeException(retry_time=retry_time)

        redis_client.set(
            key=redis_forget_sended_confirm_count.format(email=email),
            value=int(sended_count) + 1,
            ex=seconds_left(),
        )
        redis_client.set(
            key=redis_forget_sended_confirm_time.format(email=email),
            value=current_timestamp,
            ex=seconds_left(),
        )

    def get_confirm_code(self, payload: ForgetUserRequest):
        user = self.adapter.get_user_by_email(email=payload.email)
        if user is None:
            raise UserNotExitException

        self.__check_send_email_attempts(email=payload.email)

        auth_handler = AuthHandler()
        password = auth_handler.generate_random_password()
        hash_password = auth_handler.generate_hash_password(password=password)

        self.adapter.update_password_register(
            email=payload.email, password=hash_password
        )

        send_mail(receiver_email=payload.email, password=password)

        access_token = auth_handler.generate_token(
            data=dict(email=payload.email),
            expires_delta=EXPIRE_TOKEN["REGISTER"],
        )
        return ForgetUserResponse(
            tmp_token=access_token,
            retry_time=RESEND_VERIFICATION["RETRY_AFTER"]["PASSWORD"],
        )

    def confirm_code(self, payload: ForgetUserConfirmRequest, token):
        auth_handler = AuthHandler()
        token_data: dict = auth_handler.decode_token(token=token)
        email = token_data.get("email")

        register_user: Register = self.adapter.get_register_by_email(email=email)
        if register_user is None:
            raise UserNotExitException

        if not auth_handler.verify_hash_password(
            plain_password=payload.password, hashed_password=register_user.password
        ):
            raise PasswordInvalidException

        access_token = auth_handler.generate_token(
            data=dict(email=email),
            expires_delta=EXPIRE_TOKEN["RESET_PASSWORD"],
        )
        redis_client = RedisClient()
        redis_client.set(
            key=redis_verify_access_token.format(email=email), value=access_token
        )
        return ForgetUserConfirmData(access_token=access_token)

    def reset_password(self, payload: ForgetUserResetRequest, token):
        if payload.new_password != payload.new_password_retype:
            raise PasswordInvalidException
        auth_handler = AuthHandler()
        token_data: dict = auth_handler.decode_token(token=token)
        email = token_data.get("email")

        redis_client = RedisClient()
        redis_token = redis_client.get(
            key=redis_verify_access_token.format(email=email)
        )
        if token != redis_token:
            raise TokenException

        hash_password = auth_handler.generate_hash_password(
            password=payload.new_password
        )

        self.adapter.update_password_user(email=email, password=hash_password)
        access_token = auth_handler.generate_token(
            data=dict(email=email),
            expires_delta=EXPIRE_TOKEN["SESSION"],
        )
        redis_client.set(
            key=redis_verify_access_token.format(email=email), value=access_token
        )
        return ForgetUserResetData(access_token=access_token)
