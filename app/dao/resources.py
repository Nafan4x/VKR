from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

import os

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
        elif type == 'file':
            resources = result.scalars().all()
            await session.commit()
            if resources:
                return [(resource.id, resource.name, resource.url) for resource in resources]
        return None

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
            if type == 'file':
                await session.commit()
                return False
            resource.url = url

        await session.commit()
        await session.refresh(resource)

        return True
    
    @staticmethod
    async def delete_by_id(session: AsyncSession, resource_id: int) -> bool:
        result = await session.execute(
            select(Resources).where(Resources.id == resource_id)
        )
        resource = result.scalar_one_or_none()

        if not resource:
            return False 

        if resource.type == 'file' and resource.url:
            try:
                if os.path.exists(resource.url):
                    os.remove(resource.url)
            except Exception as e:
                print(f"Ошибка при удалении файла {resource.url}: {e}")

        await session.delete(resource)
        await session.commit()
        return True
