from sqlalchemy import select, insert, delete, update
from src.settings import async_session_maker
from src.database import Model


class BaseRepository:
    model: Model = None

    async def select_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            result = [row[0].to_read_model() for row in result.all()]
            return result

    async def select_one(self, pk: int):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(pk=pk)
            result = await session.execute(stmt)
            return result.scalar()

    async def insert_data(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data)
            await session.execute(stmt)
            await session.commit()

    async def delete_data(self, pk: int):
        async with async_session_maker() as session:
            stmt = delete(self.model).filter_by(pk=pk)
            await session.execute(stmt)
            await session.commit()

    async def update_data(self, pk: int, data: dict):
        async with async_session_maker() as session:
            stmt = update(self.model).filter_by(pk=pk).values(**data)
            await session.execute(stmt)
            await session.commit()
