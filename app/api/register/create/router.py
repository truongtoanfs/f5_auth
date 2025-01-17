from typing import Annotated
from fastapi import Depends
from app.base.api.router import BaseRouter
from app.core.register.create.ports import RegisterUserUseCase
from app.core.register.create.models import (
    RegisterUserRequest,
    RegisterUserServiceResponse,
)
from app.libs.common.messages import REGISTER
from app.libs.common.utils import get_language
from app.api.register.create.dependencies import register_user_service
from app.libs.common.auth_handler import verify_captcha


router = BaseRouter()


tags = ["register"]


@router.post("/register/create", tags=tags, response_model=RegisterUserServiceResponse)
def register(
    payload: RegisterUserRequest,
    service: Annotated[RegisterUserUseCase, Depends(register_user_service)],
    language: Annotated[str, Depends(get_language)],
    captcha: Annotated[bool, Depends(verify_captcha)],
):
    result = service.register(payload)
    response = RegisterUserServiceResponse(
        status_code=201, message=REGISTER["CREATE_SUCCESS"][language], data=result
    )
    return response
