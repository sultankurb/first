from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from src.database import Base


class Course(Base):
    title: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    media_url: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    price: Mapped[int] = mapped_column(Integer, default=0)
