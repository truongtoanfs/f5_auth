from sqlmodel import select, Session
from app.core.register.create.ports import RegisterUserPort
from app.libs.mysql.models.user import User
from app.libs.mysql.models import Register


class RegisterUserApdater(RegisterUserPort):
    def __init__(self, session: Session):
        self.session = session

    def fetch_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        return result

    def fetch_register_by_email(self, email: str):
        statement = select(Register).where(Register.email == email)
        result = self.session.exec(statement).first()
        return result

    def add_user_to_register(self, register: Register):
        self.session.add(register)
        self.session.commit()
        self.session.refresh(register)
        return register

    def update_register_password(self, email, hash_password, password_expired):
        statement = select(Register).where(Register.email == email)
        register_user = self.session.exec(statement).one()
        register_user.password = hash_password
        register_user.password_expired_at = password_expired
        self.session.add(register_user)
        self.session.commit()
