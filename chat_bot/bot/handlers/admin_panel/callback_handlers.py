from aiogram import Router, F, Dispatcher
from aiogram.types import CallbackQuery

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin_filter import IsAdmin
from bot.keyboards.reply import main_specialist_kb, main_user_kb
from bot.keyboards.builders import approve_dismiss, no_applications_kb
from bot.states import SpecialistState, UserState
from db.methods import set_status

from db.models import Specialist
from bot.config_reader import config
from bot.fabrics.callback_factory import CallbackFactory
from .admin_menu import admin_start

admin_id = config.ADMIN_ID.get_secret_value()
router = Router()


@router.callback_query(IsAdmin(), F.data == 'update')
async def update(callback: CallbackQuery,
                 session: AsyncSession):
    await callback.answer()
    await callback.bot.delete_message(admin_id, callback.message.message_id)
    await admin_start(callback.message, session)


@router.callback_query(IsAdmin(), CallbackFactory.filter(F.action == 'approve'))
async def approve_specialist(callback: CallbackQuery,
                             callback_data: CallbackFactory,
                             session: AsyncSession,
                             dispatcher: Dispatcher) -> None:
    user_id = callback_data.value
    await callback.message.answer(
        text='Специалист был успешно добавлен 👍'
    )

    specialist = await session.scalar(select(Specialist).where(Specialist.id == user_id))

    if specialist.status == -1:
        await callback.bot.send_message(
            user_id,
            "<b>Поздравляем, ваша анкета прошла модерацию</b> 🎉")
        await dispatcher.fsm.get_context(callback.bot,
                                         user_id,
                                         user_id).set_state(SpecialistState.MENU_STATE)
        await callback.bot.send_message(
            user_id,
            "Готовы начать? Отправьте /work, чтобы присоединиться к очереди. 😊🚀",
            reply_markup=main_specialist_kb
        )
    await set_status(session, user_id, 0)
    await new_applications(callback, session)


@router.callback_query(IsAdmin(), CallbackFactory.filter(F.action == 'dismiss'))
async def dismiss_specialist(callback: CallbackQuery,
                             callback_data: CallbackFactory,
                             session: AsyncSession,
                             dispatcher: Dispatcher) -> None:
    user_id = callback_data.value
    await callback.message.answer(
        text='Вы отклонили заявку специалиста ❌'
    )

    await session.execute(delete(Specialist).where(Specialist.id == user_id))
    await session.commit()

    await callback.bot.send_message(
        user_id,
        "<b>Ваша заявка была отклонена ❌</b>\n"
        "<tg-spoiler>Однако вы ещё можете пользоваться ботом как обычный пользователь 😌</tg-spoiler>")
    await dispatcher.fsm.get_context(callback.bot,
                                     user_id,
                                     user_id).set_state(UserState.MENU_STATE)

    specialists = await session.scalars(select(Specialist).where(Specialist.status == 1))
    await callback.bot.send_message(
        user_id,
        f"<i>Отправь /chat когда будешь готов начать.\n"
        f"Специалистов в сети:</i> <code>{len(specialists.fetchall())}</code>",
        reply_markup=main_user_kb
    )
    await new_applications(callback, session)


@router.callback_query(IsAdmin(), F.data == "new_application")
async def new_applications(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    specialist = await session.scalar(select(Specialist).where(Specialist.status == -1))
    if specialist is None:
        await callback.bot.send_animation(
            admin_id,
            animation='CgACAgQAAxkBAAIL2GY-PEbEkP-pe4VITOH_VzjxIh3qAALRAgACBqMVU32UxOd7SfRSNQQ',
            caption='Нет новых заявок от специалистов 💤',
            reply_markup=no_applications_kb()
        )
        return

    await callback.bot.send_document(
        chat_id=admin_id,
        document=specialist.file_id
    )

    pattern = (f"<i><b>Специалист</b>: {specialist.surname} {specialist.name}\n"
               f"О себе: {specialist.description} </i>\n\n")

    await callback.bot.send_photo(
        admin_id,
        specialist.photo_id,
        caption=pattern,
        reply_markup=approve_dismiss(specialist)
    )


@router.callback_query(IsAdmin(), F.data == "nothing")
async def total(callback: CallbackQuery):
    await callback.answer()
