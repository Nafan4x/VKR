from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserDAO:
    @staticmethod
    async def update_or_create(
        session: AsyncSession,
        telegram_id: int,
        username: str = None,
        full_name: str = None
    ) -> tuple[User, bool]:

        result = await session.execute(
            select(User).where(User.tg_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        is_first = False

        if not user:
            user = User(
                tg_id=telegram_id,
                username=username if username else None,
                full_name=full_name if full_name else None
            )
            session.add(user)
            is_first = True
        else:
            user.username = username

        await session.commit()
        await session.refresh(user)

        return user, is_first

    @staticmethod
    async def get_all_users_ids(
        session: AsyncSession,
    ) -> list:

        result = await session.execute(
            select(User.tg_id)
        )
        user_ids = result.scalars().all()
        return user_ids

    @staticmethod
    async def get_user_by_id(session: AsyncSession, tg_id: int) -> User | None:
        """Возвращает объект User по Telegram ID"""
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()  # возвращает объект User или None
        return user

    @staticmethod
    async def get_all_users_info(
        session: AsyncSession,
    ) -> list:

        result = await session.execute(
            select(User)
        )
        users = result.scalars().all()
        users_data = []
        for user in users:
            user_dict = {
                'ID': user.id,
                'tg_id': user.tg_id,
                'Username': user.username,
                'Fullname': user.full_name,
                'is_banned': user.is_banned
            }

            users_data.append(user_dict)

        return users_data

    @staticmethod
    async def is_banned(
        session: AsyncSession,
        tg_id: int
    ) -> bool:

        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalars().first()
        if user.is_banned:
            return True
        else:
            return False
    
    @staticmethod
    async def ban_user(
        session: AsyncSession,
        tg_id: int
    ) -> bool:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalars().first()

        if user:
            user.is_banned = True
            await session.commit()
            return True
        return False
