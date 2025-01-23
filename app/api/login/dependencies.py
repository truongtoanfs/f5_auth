from fastapi import Depends
from app.core.login.services import LoginService
from app.libs.mysql.session import get_session
from app.adapters.login import LoginAdapter

def login_adapter(session=Depends(get_session)):
    return LoginAdapter(session=session)

def login_service(adapter=Depends(login_adapter)):
    return LoginService(adapter=adapter)