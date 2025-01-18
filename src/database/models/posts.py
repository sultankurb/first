from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from pydantic import BaseModel
from src.database import Model
from typing import Optional


class PostsORM(Model):
    __tablename__ = "posts"
    title: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    media_url: Mapped[str] = mapped_column(Text(), nullable=True)

    def to_read_model(self):
        return PostsModel(
            pk=self.pk,
            title=self.title,
            description=self.description,
            media_url=self.media_url,
        )


class PostsModel(BaseModel):
    pk: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    media_url: Optional[str] = None
