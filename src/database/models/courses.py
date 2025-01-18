from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from src.database import Model
from pydantic import BaseModel
from typing import Optional


class CoursesORM(Model):
    __tablename__ = "courses"
    title: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    description: Mapped[str] = mapped_column(Text())
    images_url: Mapped[str] = mapped_column(String)

    def to_read_model(self):
        return CoursesBaseModel(
            pk=self.pk,
            title=self.title,
            description=self.description,
            images_url=self.images_url,
        )


class CoursesBaseModel(BaseModel):
    pk: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    images_url: Optional[str] = None
