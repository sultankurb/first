from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean
from src.database import Model
from pydantic import BaseModel
from typing import Optional


class EventORM(Model):
    __tablename__ = "event"
    title: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    media_url: Mapped[str] = mapped_column(Text())
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    def to_read_model(self):
        return EventModel(
            pk=self.pk,
            title=self.title,
            description=self.description,
            media_url=self.media_url,
        )


class EventModel(BaseModel):
    pk: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    media_url: Optional[str] = None
    active: Optional[bool] = None
