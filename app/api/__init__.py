from fastapi import APIRouter
from app.api.register.create.router import router as register_create_router
from app.api.register.confirm.router import router as register_confirm_router
from app.api.user.forget.router import router as forget_user_router

router = APIRouter()

routes = [register_create_router, register_confirm_router, forget_user_router]

for r in routes:
    router.include_router(r)
