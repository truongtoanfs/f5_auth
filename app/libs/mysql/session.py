from sqlmodel import Session, create_engine
from config import apiConfig

engine = create_engine(apiConfig.MYSQL_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
