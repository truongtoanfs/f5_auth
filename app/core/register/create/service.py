from datetime import datetime, timezone, timedelta
from app.core.register.create.ports import RegisterUserUseCase, RegisterUserPort
from app.core.register.create.models import RegisterUserRequest, RegisterUserResponse
from app.libs.exception.service import (
    UserExistException,
    UserConfirmedException,
    BlockedEmailException,
    SendEmailTimeException,
)
from app.libs.common.auth_handler import AuthHandler
from app.libs.mail.send_mail import send_mail
from app.libs.common.constants import EXPIRE_TOKEN, RESEND_VERIFICATION
from app.libs.mysql.models import Register
from app.libs.common.utils import check_black_domain
from config import apiConfig
from app.libs.redis.redis_client import RedisClient
from app.libs.redis.constants import (
    redis_register_sended_confirm_count,
    redis_register_sended_confirm_time,
)
from app.libs.common.utils import seconds_left


class RegisterUserService(RegisterUserUseCase):
    def __init__(self, adapter: RegisterUserPort):
        self.adapter = adapter

    def __check_register_count(self, email: str):
        redis_client = RedisClient()

        register_count = redis_client.get(
            key=redis_register_sended_confirm_count.format(email=email)
        )

        register_timestamp = redis_client.get(
            key=redis_register_sended_confirm_time.format(email=email)
        )
        current_timestamp = int(datetime.now(timezone.utc).timestamp())
        if register_count is None:
            redis_client.set(
                key=redis_register_sended_confirm_count.format(email=email),
                value=1,
                ex=seconds_left(),
            )
            redis_client.set(
                key=redis_register_sended_confirm_time.format(email=email),
                value=current_timestamp,
                ex=seconds_left(),
            )
            return

        if int(register_count) > 3:
            raise BlockedEmailException

        # check resend 60s, 90s, 120s
        next_timestamp = int(register_timestamp) + int(register_count) * 30 + 30
        retry_time = next_timestamp - current_timestamp
        if retry_time > 0:
            raise SendEmailTimeException(retry_time=retry_time)

        redis_client.set(
            key=redis_register_sended_confirm_count.format(email=email),
            value=int(register_count) + 1,
            ex=seconds_left(),
        )
        redis_client.set(
            key=redis_register_sended_confirm_time.format(email=email),
            value=current_timestamp,
            ex=seconds_left(),
        )

    def register(self, payload: RegisterUserRequest):
        user = self.adapter.fetch_user_by_email(email=payload.email)
        if user:
            raise UserExistException

        self.__check_register_count(email=payload.email)

        current_time = datetime.now(timezone.utc)
        auth_handler = AuthHandler()
        password = auth_handler.generate_random_password()
        hash_password = auth_handler.generate_hash_password(password=password)

        register: Register = self.adapter.fetch_register_by_email(email=payload.email)
        if register:
            if register.is_confirmed:
                raise UserConfirmedException
            elif (
                register.password_expired_at.replace(tzinfo=timezone.utc) < current_time
            ):

                self.adapter.update_register_password(
                    email=payload.email,
                    hash_password=hash_password,
                    password_expired=current_time
                    + timedelta(seconds=apiConfig.PASSWORD_EXPIRED),
                )
                send_mail(receiver_email=payload.email, password=password)
                access_token = auth_handler.generate_token(
                    data=dict(email=payload.email),
                    expires_delta=EXPIRE_TOKEN["REGISTER"],
                )
                return RegisterUserResponse(
                    tmp_token=access_token,
                    retry_time=RESEND_VERIFICATION["RETRY_AFTER"]["PASSWORD"],
                )
            else:
                access_token = auth_handler.generate_token(
                    data=dict(email=payload.email),
                    expires_delta=EXPIRE_TOKEN["REGISTER"],
                )
                return RegisterUserResponse(
                    tmp_token=access_token,
                    retry_time=RESEND_VERIFICATION["RETRY_AFTER"]["PASSWORD"],
                )

        check_black_domain(email=payload.email)

        data = Register(email=payload.email, password=hash_password)
        register = self.adapter.add_user_to_register(register=data)
        send_mail(receiver_email=payload.email, password=password)
        access_token = auth_handler.generate_token(
            data=dict(email=payload.email),
            expires_delta=EXPIRE_TOKEN["REGISTER"],
        )
        return RegisterUserResponse(
            tmp_token=access_token,
            retry_time=RESEND_VERIFICATION["RETRY_AFTER"]["PASSWORD"],
        )
