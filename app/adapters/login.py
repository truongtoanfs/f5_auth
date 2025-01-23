from sqlmodel import Session, select
from app.core.login.ports import LoginPort
from app.libs.mysql.models import User

class LoginAdapter(LoginPort):
    def __init__(self, session: Session):
        self.session = session

    def fetch_user_by_email(self, email):
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        return result