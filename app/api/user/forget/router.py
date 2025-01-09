from fastapi import Depends, status
from app.base.api.router import BaseRouter
from app.core.user.forget.models import (
    ForgetUserServiceResponse,
    ForgetUserRequest,
    ForgetUserConfirmRequest,
    ForgetUserConfirmServiceResponse,
    ForgetUserResetRequest,
    ForgetUserResetServiceResponse,
)
from app.core.user.forget.ports import UserForgetUseCase
from app.libs.common.utils import get_language
from app.libs.common.messages import SUCCESS
from .dependencies import forget_user_service
from app.libs.common.auth_handler import get_token_client


router = BaseRouter()


tag = ["user"]


@router.post("/user/forget", tags=tag, response_model=ForgetUserServiceResponse)
def forget_user(
    payload: ForgetUserRequest,
    service: UserForgetUseCase = Depends(forget_user_service),
    language: str = Depends(get_language),
):
    result = service.get_confirm_code(payload=payload)

    response = ForgetUserServiceResponse(
        status_code=status.HTTP_200_OK,
        message=SUCCESS["GET_CONFIRM_CODE_SUCCESS"][language],
        data=result,
    )
    return response


@router.post(
    "/user/forget/confirm", tags=tag, response_model=ForgetUserConfirmServiceResponse
)
def forget_user_confirm(
    payload: ForgetUserConfirmRequest,
    service: UserForgetUseCase = Depends(forget_user_service),
    token: str = Depends(get_token_client),
    language: str = Depends(get_language),
):
    result = service.confirm_code(payload=payload, token=token)

    response = ForgetUserConfirmServiceResponse(
        status_code=status.HTTP_200_OK,
        message=SUCCESS["CONFIRM_SUCCESS"][language],
        data=result,
    )
    return response


@router.post(
    "/user/forget/reset", tags=tag, response_model=ForgetUserResetServiceResponse
)
def forget_user_reset(
    payload: ForgetUserResetRequest,
    service: UserForgetUseCase = Depends(forget_user_service),
    token: str = Depends(get_token_client),
    language: str = Depends(get_language),
):
    result = service.reset_password(payload=payload, token=token)

    response = ForgetUserResetServiceResponse(
        status_code=status.HTTP_200_OK,
        message=SUCCESS["CHANGE_PASSWORD"][language],
        data=result,
    )
    return response
