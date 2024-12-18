from app.core.register.create.ports import RegisterUserPort


class RegisterUserApdater(RegisterUserPort):
    def __init__(self, session):
        self.session = session

    async def fetch_user_by_email(self, email: str):
        pass

    async def fetch_register_by_email(self, email: str):
        pass
