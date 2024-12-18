from fastapi import Request, Depends
from app.core.register.create.service import RegisterUserService
from app.adapters.register.create import RegisterUserApdater


def register_adapter(session=Depends()):
    return RegisterUserApdater(session=session)


def register_user_service(adapter=Depends(register_adapter)):
    return RegisterUserService(adapter=adapter)


def get_language(request: Request):
    accept_language = request.headers.get("accept-language")
    if accept_language and "en" in accept_language:
        return "en"
    return "vi"
