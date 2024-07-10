import random
from aiogram import Router, F, Dispatcher
from aiogram.types import Message
from aiogram.filters import and_f, or_f, Command
from aiogram.fsm.context import FSMContext

from db import Chat, Specialist
from db.methods import get_specialists_by_status, set_status

from bot.states import UserState, SpecialistState

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.reply import main_user_kb, leave_kb, rmk

router = Router()


@router.message(
    and_f(
        or_f(F.text == "☕ Искать специалиста", Command("chat")),
        UserState.MENU_STATE
    )
)
async def start_chat_user(message: Message,
                          state: FSMContext,
                          session: AsyncSession,
                          dispatcher: Dispatcher):
    user_id = message.from_user.id
    specialists = (await get_specialists_by_status(session, 1)).fetchall()
    if len(specialists) == 0:
        await message.answer('<b>💤 К сожалению, на данный момент нет свободных специалистов 😢</b>\n',
                             reply_markup=main_user_kb)
        specialists = await session.scalars(select(Specialist).where(Specialist.status == 1))
        await message.answer(
            f"<i>Отправь /chat когда будешь готов начать.\n"
            f"Специалистов в сети:</i> <code>{len(specialists.fetchall())}</code>",
            reply_markup=main_user_kb
        )
        return
    random_specialist = random.choice(specialists)
    random_specialist.status = 2
    await message.answer('Вы начали поиск специалиста 💬', reply_markup=rmk)

    pattern = (f"<i><b>Специалист</b>: {random_specialist.surname} {random_specialist.name}\n"
               f"О себе: {random_specialist.description} </i>\n\n"
               f"<b>Расскажите, что вас тревожит - {random_specialist.name} готов вам помочь 🤗</b>")

    await message.answer_photo(
        random_specialist.photo_id,
        caption=pattern,
        reply_markup=leave_kb
    )
    await message.bot.send_message(random_specialist.id, '💬 Пользователь найден, начинайте общение',
                                   reply_markup=leave_kb)

    session.add(Chat(user_id=user_id, specialist_id=random_specialist.id))
    await session.commit()
    await state.set_state(UserState.IN_CHAT)
    await dispatcher.fsm.get_context(message.bot,
                                     random_specialist.id,
                                     random_specialist.id).set_state(SpecialistState.IN_CHAT)


@router.message(
    and_f(
        or_f(F.text == "☕ Начать поиск пользователей", Command("work")),
        SpecialistState.MENU_STATE
    )
)
async def start_chat_specialist(message: Message,
                                state: FSMContext,
                                session: AsyncSession):
    user_id = message.from_user.id
    await message.reply(
            "<b>☕ Начали поиск пользователей</b>\n"
            "<i>Используйте команду /stop, чтобы остановить поиск.</i>",
            reply_markup=rmk)
    await set_status(session, user_id, 1)
    await state.set_state(SpecialistState.AVAILABLE)
