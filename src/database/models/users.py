from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel
from src.database import Base
from typing import Optional


class User(Base):
    username: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    first_name: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    users_id: Mapped[int] = mapped_column(BigInteger, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)


class UsersModel(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    users_id: Optional[int] = None
    is_admin: Optional[bool] = False
    is_blocked: Optional[bool] = False
