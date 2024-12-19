from sqlmodel import SQLModel, create_engine
from config import apiConfig

engine = create_engine(apiConfig.MYSQL_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
