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

router = BaseRouter()


tags = ["register"]


@router.post("/register/create", tags=tags, response_model=RegisterUserServiceResponse)
async def register(
    payload: RegisterUserRequest,
    service: RegisterUserUseCase = Depends(register_user_service),
    language: str = Depends(get_language),
):
    result = await service.register(payload)
    response = RegisterUserServiceResponse(
        status_code=201, message=REGISTER["CREATE_SUCCESS"][language], data=result
    )
    return response
