from app.core.register.create.ports import RegisterUserUseCase, RegisterUserPort


class RegisterUserService(RegisterUserUseCase):

    def __init__(self, adapter: RegisterUserPort):
        self.adapter = adapter

    def register(self):
        return "i am implementation"
