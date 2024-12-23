from sqlmodel import select
from app.core.register.create.ports import RegisterUserPort
from app.libs.mysql.models.user import User


class RegisterUserApdater(RegisterUserPort):
    def __init__(self, session):
        self.session = session

    async def fetch_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        return result

    async def fetch_register_by_email(self, email: str):
        pass
