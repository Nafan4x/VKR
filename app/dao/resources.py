from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.resources import Resources


class ResourcesDAO:
    @staticmethod
    async def get_resources(
        session: AsyncSession,
        type: str,
    ) -> str:

        result = await session.execute(
            select(Resources).where(Resources.type == type)
        )
        if type == 'link':
            resource = result.scalar_one_or_none()
            link = resource.url
            await session.commit()
            return link
        
        resources = result.all()
        await session.commit()

        return resources

    @staticmethod
    async def update_or_create(
        session: AsyncSession,
        type: str = None,
        name: str = None,
        url: str = None
    ) -> bool:

        result = await session.execute(
            select(Resources).where(Resources.type == type).where(Resources.name == name)
        )
        resource = result.scalar_one_or_none()

        if not resource:
            resource = Resources(type=type, name=name, url=url)
            session.add(resource)
        else:
            resource.url = url

        await session.commit()
        await session.refresh(resource)

        return True
