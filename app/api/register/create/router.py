from app.base.api.router import router
from app.core.register.create.models import RegisterUserRequest


tags = ["register"]


@router.post(
    "/register/create",
    tags=tags,
)
def register(payload: RegisterUserRequest):
    return "ok"
