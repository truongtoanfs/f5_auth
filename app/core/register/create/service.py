from app.core.register.create.ports import RegisterUserUseCase, RegisterUserPort
from app.core.register.create.models import RegisterUserRequest


class RegisterUserService(RegisterUserUseCase):

    def __init__(self, adapter: RegisterUserPort):
        self.adapter = adapter

    def register(self, payload: RegisterUserRequest):
        user = self.adapter.fetch_user_by_email(email=payload.email)
        if user is None:
            raise "UserExistsException"
        return "i am implementation"
