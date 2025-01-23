from typing import Annotated
from fastapi import Depends, status
from app.base.api.router import BaseRouter
from app.libs.common.utils import get_language
from app.core.login.models import LoginServiceResponse, LoginRequest
from app.core.login.ports import LoginUseCase
from .dependencies import login_service
from app.libs.common.messages import SUCCESS


router = BaseRouter()

tags = ["login"]

@router.post("/login", tags=tags, response_model=LoginServiceResponse)
def login(
    payload: LoginRequest,
    service: Annotated[LoginUseCase, Depends(login_service)],
    language: Annotated[str, Depends(get_language)],
):
    result = service.login(payload=payload)
    message = SUCCESS["CONFIRM_SUCCESS"][language]
    if payload.password:
        message = SUCCESS["LOGIN"][language]

    response = LoginServiceResponse(status_code=status.HTTP_200_OK, message=message, data=result)

    return response