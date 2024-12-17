from app.core.register.create.ports import RegisterUserUseCase


class RegisterUserService(RegisterUserUseCase):
    def register(self):
        return "i am implementation"
