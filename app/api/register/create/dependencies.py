from fastapi import Depends
from app.core.register.create.service import RegisterUserService
from app.adapters.register.create import RegisterUserApdater
from app.libs.mysql.session import get_session


def register_adapter(session=Depends(get_session)):
    return RegisterUserApdater(session=session)


def register_user_service(adapter=Depends(register_adapter)):
    return RegisterUserService(adapter=adapter)
