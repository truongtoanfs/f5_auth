from datetime import datetime, timezone
from sqlmodel import Session, select
from app.core.user.forget.ports import UserForgetPort
from app.libs.mysql.models import Register, User
from app.libs.exception.service import UserNotExitException


class ForgetUserAdapter(UserForgetPort):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email):
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        return result

    def get_register_by_email(self, email):
        statement = select(Register).where(Register.email == email)
        result = self.session.exec(statement).first()
        return result

    def update_password_register(self, email, password):
        statement = select(Register).where(Register.email == email)
        register_user = self.session.exec(statement).first()
        if register_user is None:
            raise UserNotExitException
        register_user.password = password

        self.session.add(register_user)
        self.session.commit()

    def update_password_user(self, email, password):
        statement = select(User).where(User.email == email)
        user = self.session.exec(statement).first()
        if user is None:
            raise UserNotExitException
        user.password = password
        user.password_updated_at = datetime.now(timezone.utc)

        self.session.add(user)
        self.session.commit()
