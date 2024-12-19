from sqlmodel import Field, SQLModel, create_engine


class Register(SQLModel, table=True): ...
