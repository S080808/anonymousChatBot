from aiogram import Router, F
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.models import Specialist
from bot.filters.admin_filter import IsAdmin
from bot.keyboards.builders import admin_menu_kb

router = Router()


@router.message(IsAdmin())
async def admin_start(message: Message, session: AsyncSession):
    new_applications = await session.scalars(select(Specialist).where(Specialist.status == -1))
    all_specialists = await session.scalars(select(Specialist).where(Specialist.status != -1))
    online_specialists = await session.scalars(select(Specialist).where(Specialist.status.in_([1, 2])))
    await message.answer_animation(
        animation='CgACAgIAAxkBAAILAAFmPPO33yz1nqmYipZbZhebsKvxTQACh0kAAp5n4EnNff8ph7FcATUE',
        caption=f'Привет, самый красивый человек на свете 😎\n'
                f'Специалистов в боте: <code>{len(all_specialists.fetchall())}</code>\n'
                f'Из которых в сети: <code>{len(online_specialists.fetchall())}</code>\n'
                f'Новых заявок: <code>{len(new_applications.fetchall())}</code>',
        reply_markup=admin_menu_kb()
    )
