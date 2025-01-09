from pydantic import BaseModel, EmailStr


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
    new_password: str
    new_password_retype: str


class ForgetUserResetServiceResponse(BaseModel):
    status_code: int
    message: str
    data: ForgetUserResetData
