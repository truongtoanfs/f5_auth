import string
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, AfterValidator, model_validator
from app.libs.common.messages import ERROR


def isValidPassword(password: str):
    if (
        len(password) >= 8
        and any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in string.punctuation for c in password)
    ):
        return password
    raise ValueError(ERROR["PASSWORD_FORMAT_INVALID"]["en"])


class ForgetUserRequest(BaseModel):
    email: EmailStr


class ForgetUserResponse(BaseModel):
    tmp_token: str
    retry_time: int


class ForgetUserServiceResponse(BaseModel):
    status_code: int
    message: str
    data: ForgetUserResponse


# user forget confirm
class ForgetUserConfirmRequest(BaseModel):
    password: str


class ForgetUserConfirmData(BaseModel):
    access_token: str


class ForgetUserConfirmServiceResponse(BaseModel):
    status_code: int
    message: str
    data: ForgetUserConfirmData


# user forget reset
class ForgetUserResetData(BaseModel):
    access_token: str


class ForgetUserResetRequest(BaseModel):
    new_password: Annotated[str, AfterValidator(isValidPassword)]
    new_password_retype: Annotated[str, AfterValidator(isValidPassword)]

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.new_password != self.new_password_retype:
            raise ValueError(ERROR["PASSWORD_RETYPE_INVALID"]["en"])
        return self


class ForgetUserResetServiceResponse(BaseModel):
    status_code: int
    message: str
    data: ForgetUserResetData
