from fastapi import Depends
from app.libs.mysql.session import get_session
from app.core.user.forget.service import ForgetUserService
from app.adapters.user.forget import ForgetUserAdapter


def forget_user_adapter(session=Depends(get_session)):
    return ForgetUserAdapter(session=session)


def forget_user_service(adapter=Depends(forget_user_adapter)):
    return ForgetUserService(adapter=adapter)
