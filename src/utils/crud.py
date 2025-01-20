from sqlalchemy import select, insert, delete, update
from src.settings import async_session_maker


async def select_all(model):
    async with async_session_maker() as session:
        stmt = select(model)
        result = await session.execute(stmt)
        return result.scalars().all()


async def select_one(model, pk: int):
    async with async_session_maker() as session:
        stmt = select(model).filter_by(pk=pk)
        result = await session.execute(stmt)
        return result.scalar()


async def insert_one(model, data: dict):
    async with async_session_maker() as session:
        stmt = insert(model).values(**data)
        await session.execute(stmt)
        await session.commit()


async def delete_one(model, pk: int):
    async with async_session_maker() as session:
        stmt = delete(model).filter_by(pk=pk)
        await session.execute(stmt)
        await session.commit()


async def update_one(model, data: dict, pk: int):
    async with async_session_maker() as session:
        stmt = update(model).filter_by(pk=pk).values(**data)
        await session.execute(stmt)
        await session.commit()
