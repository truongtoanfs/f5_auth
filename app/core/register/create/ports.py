from typing import Protocol


class RegisterUserUseCase(Protocol):
    def register(self):
        raise NotImplementedError()


class RegisterUserPort(Protocol):
    async def fetch_user_by_email(self, email: str):
        raise NotImplementedError()
