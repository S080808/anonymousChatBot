from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Specialist, Chat


async def get_role(session: AsyncSession, user_id: int) -> str:
    exists = await session.scalar(select(Specialist).where(Specialist.id == user_id))
    if exists:
        return 'specialist'
    else:
        return 'user'


async def get_partner_id(session: AsyncSession, user_id: int) -> int:
    role = await get_role(session, user_id)
    if role == 'specialist':
        chat = await session.scalar(select(Chat).where(Chat.specialist_id == user_id))
        if chat is not None:
            return chat.user_id
    if role == 'user':
        chat = await session.scalar(select(Chat).where(Chat.user_id == user_id))
        if chat is not None:
            return chat.specialist_id


async def set_status(session: AsyncSession, user_id: int, status: int) -> None:
    specialist = await session.scalar(select(Specialist).where(Specialist.id == user_id))
    specialist.status = status
    await session.commit()


async def get_specialists_by_status(session: AsyncSession, status: Union[list[int], int]):
    if isinstance(status, int):
        return await session.scalars(select(Specialist).where(Specialist.status == status))
    else:
        return await session.scalars(select(Specialist).where(Specialist.status.in_(status)))
