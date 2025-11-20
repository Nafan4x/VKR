from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.social import Social


class SocialDAO:
    @staticmethod
    async def get_socials(
        session: AsyncSession,
    ) -> list:

        result = await session.execute(
            select(Social)
        )
        socials = result.scalars().all()
        await session.commit()
        if socials:
            return [(event.id, event.name, event.description) for event in socials]
        return None

    @staticmethod
    async def get_by_id(session: AsyncSession, social_id: int) -> bool:
        result = await session.execute(
            select(Social).where(Social.id == social_id)
        )
        social = result.scalar_one_or_none()

        await session.commit()
        return (social.id, social.name, social.description)

    @staticmethod
    async def update_or_create(
        session: AsyncSession,
        name: str = None,
        description: str = None,
    ) -> bool:

        result = await session.execute(
            select(Social).where(Social.name == name)
        )
        event = result.scalar_one_or_none()

        if not event:
            event = Social(name=name, description=description)
            session.add(event)
        else:
            event.description = description

        await session.commit()
        await session.refresh(event)

        return True

    @staticmethod
    async def delete_by_id(session: AsyncSession, social_id: int) -> bool:
        result = await session.execute(
            select(Social).where(Social.id == social_id)
        )
        event = result.scalar_one_or_none()

        if not event:
            return False

        await session.delete(event)
        await session.commit()
        return True
