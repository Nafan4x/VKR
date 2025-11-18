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
            user = User(tg_id=telegram_id, username=username, full_name=full_name)
            session.add(user)
            is_first = True
        else:
            user.username = username

        await session.commit()
        await session.refresh(user)

        return user, is_first
