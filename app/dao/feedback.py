from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

import os

from app.db.models.feedback import Feedback


class FeedbackDAO:
    @staticmethod
    # async def get_resources(
    #     session: AsyncSession,
    #     type: str,
    # ) -> str:

    #     result = await session.execute(
    #         select(Resources).where(Resources.type == type)
    #     )
    #     if type == 'link':
    #         resource = result.scalar_one_or_none()
    #         link = resource.url
    #         await session.commit()
    #         return link
    #     elif type == 'file':
    #         resources = result.scalars().all()
    #         await session.commit()
    #         if resources:
    #             return [(resource.id, resource.name, resource.url) for resource in resources]
    #     return None

    @staticmethod
    async def create(
        session: AsyncSession,
        from_user_id: int = None,
        question: str = None,
    ):
        if question != '/start':
            feedback = Feedback(from_user_id=from_user_id, question=question, answer=None, is_active=True)
            session.add(feedback)

            await session.commit()
            await session.refresh(feedback)

            return feedback.id
        return False
    
    @staticmethod
    async def check_status_by_id(session: AsyncSession, feedback_id: int) -> bool:
        result = await session.execute(
            select(Feedback).where(Feedback.id == feedback_id)
        )
        feedback = result.scalar_one_or_none()

        if not feedback:
            return False 

        if feedback.is_active:
            return True

        await session.commit()
        return False
    
    @staticmethod
    async def answer_by_id(session: AsyncSession, feedback_id: int, answer: str) -> bool:
        result = await session.execute(
            select(Feedback).where(Feedback.id == feedback_id)
        )
        feedback = result.scalar_one_or_none()

        if not feedback:
            return False 

        feedback.answer = answer
        feedback.is_active = False
        
        await session.commit()
        
        return feedback
