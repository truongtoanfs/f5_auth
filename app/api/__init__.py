from app.base.api.router import BaseRouter
from app.api.register.create.router import router as register_create_router

router = BaseRouter()

routes = [
    register_create_router
]

for r in routes:
    router.include_router(r)