from .ports import LoginUseCase, LoginPort
from .models import LoginlResponseData
from app.libs.exception.service import (
    UserNotExitException,
    PasswordInvalidException
)
from app.libs.common.auth_handler import AuthHandler
from app.libs.mysql.models import User
from app.libs.common.constants import EXPIRE_TOKEN


class LoginService(LoginUseCase):
    def __init__(self, adapter: LoginPort):
        self.adapter = adapter

    def login(self, payload):
        user_info: User = self.adapter.fetch_user_by_email(email=payload.email)
        if not user_info:
            raise UserNotExitException
        
        result = LoginlResponseData(access_token="")
        if not payload.password:
            return result
        
        auth_handler = AuthHandler()
        if not auth_handler.verify_hash_password(
            plain_password=payload.password, hashed_password=user_info.password
        ):
            raise PasswordInvalidException
        
        token = auth_handler.generate_token(data=dict(email=payload.email), expires_delta=EXPIRE_TOKEN["SESSION"],)
        result = LoginlResponseData(access_token=token)

        return result