from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Integer


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    pk: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
