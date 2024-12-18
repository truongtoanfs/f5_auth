from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    email: EmailStr


class RegisterUserResponse(BaseModel):
    tmp_token: str
    retry_time: int


class RegisterUserServiceResponse(BaseModel):
    status_code: int
    message: str
    data: RegisterUserResponse
