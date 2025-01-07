from pydantic import BaseModel


class RegisterConfirmRequest(BaseModel):
    password: str


class RegisterConfirmResponseData(BaseModel):
    access_token: str


class RegisterConfirmServiceResponse(BaseModel):
    status_code: int
    message: str
    data: RegisterConfirmResponseData
