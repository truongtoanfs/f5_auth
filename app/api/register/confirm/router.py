from fastapi import Depends
from app.base.api.router import BaseRouter
from app.core.register.confirm.models import (
    RegisterConfirmServiceResponse,
    RegisterConfirmRequest,
)
from app.core.register.confirm.ports import RegisterConfirmUseCase
from app.libs.common.messages import REGISTER
from app.libs.common.utils import get_language
from app.libs.common.auth_handler import get_token_client
from app.api.register.confirm.dependencies import register_confirm_service

router = BaseRouter()

tags = ["register"]


@router.post(
    "/register/confirm", tags=tags, response_model=RegisterConfirmServiceResponse
)
def confirm_register(
    payload: RegisterConfirmRequest,
    service: RegisterConfirmUseCase = Depends(register_confirm_service),
    token: str = Depends(get_token_client),
    language: str = Depends(get_language),
):
    result = service.confirm_register(payload=payload, token=token)
    response = RegisterConfirmServiceResponse(
        status_code=201, message=REGISTER["CONFIRM_SUCCESS"][language], data=result
    )
    return response
