from sqlmodel import select, Session
from app.core.register.confirm.ports import RegisterConfirmPort
from app.libs.mysql.models import Register, User


class RegisterConfirmApdater(RegisterConfirmPort):
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

    def add_user_to_user(self, user):
        self.session.add(user)
        self.session.commit()

    def delete_register_by_email(self, email):
        statement = select(Register).where(Register.email == email)
        register_user = self.session.exec(statement).one()
        self.session.delete(register_user)
        self.session.commit()
