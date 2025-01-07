from fastapi import Depends
from app.core.register.confirm.service import RegisterConfirmService
from app.adapters.register.confirm import RegisterConfirmApdater
from app.libs.mysql.session import get_session


def register_confirm_adapter(session=Depends(get_session)):
    return RegisterConfirmApdater(session=session)


def register_confirm_service(adapter=Depends(register_confirm_adapter)):
    return RegisterConfirmService(adapter=adapter)
