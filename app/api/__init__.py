from app.base.api.router import BaseRouter
from app.api.register.create.router import router as register_create_router
from app.api.register.confirm.router import router as register_confirm_router


router = BaseRouter()

routes = [register_create_router, register_confirm_router]

for r in routes:
    router.include_router(r)
