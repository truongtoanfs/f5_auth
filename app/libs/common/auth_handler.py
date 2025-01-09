import string
import secrets
import jwt
import bcrypt
from typing import Annotated
from datetime import datetime, timedelta, timezone
from config import apiConfig
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.libs.exception.service import TokenException

ALGORITHM = "HS256"
security = HTTPBearer()


def get_token_client(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    return credentials.credentials


class AuthHandler:

    def generate_random_password(self, password_length: int = 12):
        alphabet = string.ascii_letters + string.digits
        while True:
            password = "".join(secrets.choice(alphabet) for i in range(password_length))
            if (
                any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3
            ):
                break
        return password

    def generate_hash_password(self, password: str):
        return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())

    def verify_hash_password(self, plain_password: str, hashed_password: str):
        return bcrypt.checkpw(
            password=plain_password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8"),
        )

    def generate_token(self, data: dict, expires_delta: timedelta = 30 * 60):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, apiConfig.TOKEN_SECRET_KEY, algorithm=ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str):
        try:
            token = jwt.decode(
                token, apiConfig.TOKEN_SECRET_KEY, algorithms=[ALGORITHM]
            )
            return token
        except InvalidTokenError:
            raise TokenException
