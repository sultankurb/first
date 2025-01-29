from src.settings import async_session_maker, settings
from src.utils.crud import insert_one
from src.database.models import User
from sqlalchemy import select, update
from typing import Optional


class UsersManager:
    model = User

    async def select_user_by(
            self,
            users_id: int
    ):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(users_id=users_id)
            result = await session.execute(stmt)
            return result.scalar()

    async def add_user(self, data: dict):
        await insert_one(model=self.model, data=data)

    async def update_user_status(self, user_id: int, data: dict):
        async with async_session_maker() as session:
            stmt = update(self.model).filter_by(users_id=user_id).values(**data)
            await session.execute(stmt)
            await session.commit()

    async def check_user(self, data: dict, users_id: int) -> None:
        user = await self.select_user_by(users_id=users_id)
        if user is None:
            if users_id == settings.ADMIN_ID:
                data.update(is_admin=True)
            await self.add_user(data=data)
            return
        if user is not None:
            if user.is_blocked:
                await self.update_user_status(user_id=users_id, data={"is_blocked": False})
                return
        return
