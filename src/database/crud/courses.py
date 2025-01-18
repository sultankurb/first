from src.database.models import CoursesORM
from .base import BaseRepository


class CoursesRepository(BaseRepository):
    model = CoursesORM
