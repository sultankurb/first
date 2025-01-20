from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from src.database import Base


class Event(Base):
    title: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    media_url: Mapped[str] = mapped_column(String(length=1024), nullable=True)
