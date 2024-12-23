from fastapi import Depends
from app.base.api.router import router
from app.core.register.create.models import RegisterUserRequest
from app.core.register.create.ports import RegisterUserUseCase
from app.core.register.create.models import RegisterUserServiceResponse
from app.libs.common.messages import REGISTER
from app.api.register.create.dependencies import get_language, register_user_service

tags = ["register"]


@router.post(
    "/register/create", tags=["register"], response_model=RegisterUserServiceResponse
)
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
