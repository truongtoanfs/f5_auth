from fastapi import APIRouter
from .register.create.router import router as register_create_router
from .register.confirm.router import router as register_confirm_router
from .user.forget.router import router as forget_user_router
from .login.router import router as login_router


router = APIRouter()

routes = [register_create_router, register_confirm_router, forget_user_router, login_router]

for r in routes:
    router.include_router(r)
