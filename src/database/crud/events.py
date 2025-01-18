from sqlalchemy import select

from src.database.models import EventORM
from .base import BaseRepository
from src.settings import async_session_maker


class EventsRepository(BaseRepository):
    model = EventORM

    async def filtered_search(self):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(active=True)
            result = await session.execute(stmt)
            result = [row[0].to_read_model() for row in result.all()]
            return result
