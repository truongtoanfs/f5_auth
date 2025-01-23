from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: Optional[str]
    service: Optional[str]

class LoginlResponseData(BaseModel):
    access_token: str

class LoginServiceResponse(BaseModel):
    status_code: int
    message: str
    data: LoginlResponseData