from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import Specialist
from db.methods import get_role, get_specialists_by_status
from bot.states import UserState, SpecialistState

from bot.keyboards.reply import main_user_kb, main_specialist_kb
router = Router()


@router.message(CommandStart)
async def start(message: Message,
                session: AsyncSession,
                state: FSMContext) -> None:
    user_id = message.from_user.id
    role = await get_role(session=session, user_id=user_id)
    if role == 'specialist':
        specialist = await session.scalar(select(Specialist).where(Specialist.id == message.from_user.id))
        if specialist.status == -1:
            await message.reply('<i>Ваша анкета находится на модерации.\n'
                                'Пожалуйста дождитесь <b>уведомления</b> 🤖</i>')
            return

        await state.set_state(SpecialistState.MENU_STATE)
        user = await session.scalar(select(Specialist).where(Specialist.id == user_id))
        await message.answer(
            f"<b>Здравствуйте, {user.surname} {user.name}!</b>\n"
            "Готовы начать? Отправьте /work, чтобы присоединиться к очереди. 😊🚀",
            reply_markup=main_specialist_kb
        )
    elif role == 'user':
        specialists = await get_specialists_by_status(session, 1)
        await message.reply(
            "<b>Привет! 👋👋👋</b>\n\n"
            "<i>Я твой анонимный психологический помощник. 😊</i>\n\n"
            "<b>💔 Проблемы в отношениях?\n"
            "😔 Стресс и тревога?\n"
            "💼 Работа и карьера?\n"
            "🤯 Эмоциональное выгорание?\n"
            "🎭 Личностные проблемы?</b>\n\n"
            "<i>Здесь ты можешь высказаться и не бояться быть осужденным 😇</i>\n")
        await message.answer(
            f"<i>Отправь /chat когда будешь готов начать.\n"
            f"Специалистов в сети:</i> <code>{len(specialists.fetchall())}</code>",
            reply_markup=main_user_kb
        )
        await state.set_state(UserState.MENU_STATE)
