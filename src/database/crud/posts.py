from src.database.models import PostsORM
from .base import BaseRepository


class PostsRepository(BaseRepository):
    model = PostsORM
