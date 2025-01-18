from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer


class Model(DeclarativeBase):
    __abstract__ = True
    pk: Mapped[int] = mapped_column(Integer, primary_key=True)
