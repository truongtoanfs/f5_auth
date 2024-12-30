from datetime import datetime, timezone, timedelta
from app.core.register.create.ports import RegisterUserUseCase, RegisterUserPort
from app.core.register.create.models import RegisterUserRequest, RegisterUserResponse
from app.libs.exception.service import UserExistException, UserConfirmedException
from app.libs.common.auth_handler import AuthHandler
from app.libs.mail.send_mail import send_mail
from app.libs.common.constants import EXPIRE_TOKEN, RESEND_VERIFICATION
from app.libs.mysql.models import Register
from app.libs.common.utils import check_black_domain
from config import apiConfig


class RegisterUserService(RegisterUserUseCase):

    def __init__(self, adapter: RegisterUserPort):
        self.adapter = adapter

    async def register(self, payload: RegisterUserRequest):
        user = await self.adapter.fetch_user_by_email(email=payload.email)
        if user:
            raise UserExistException

        current_time = datetime.now(timezone.utc)

        auth_handler = AuthHandler()
        password = auth_handler.generate_random_password()
        hash_password = auth_handler.generate_hash_password(password=password)

        register = await self.adapter.fetch_register_by_email(email=payload.email)
        if register:
            if register.is_confirmed:
                raise UserConfirmedException
            elif (
                register.password_expired_at.replace(tzinfo=timezone.utc) < current_time
            ):
                await self.adapter.update_register_password(
                    email=payload.email,
                    hash_password=hash_password,
                    password_expired=current_time
                    + timedelta(seconds=apiConfig.PASSWORD_EXPIRED),
                )
                await send_mail(receiver_email=payload.email, password=password)
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

        data = Register(email=payload.email, password=password)
        register = await self.adapter.add_user_to_register(register=data)
        await send_mail(receiver_email=payload.email, password=password)
        access_token = auth_handler.generate_token(
            data=dict(email=payload.email),
            expires_delta=EXPIRE_TOKEN["REGISTER"],
        )
        return RegisterUserResponse(
            tmp_token=access_token,
            retry_time=RESEND_VERIFICATION["RETRY_AFTER"]["PASSWORD"],
        )
