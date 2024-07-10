from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.fabrics.callback_factory import SpecialistsFactory
from bot.filters.admin_filter import IsAdmin
from bot.keyboards.builders import paginator
from db.models import Specialist
from .callback_handlers import admin_id
from .admin_menu import admin_start

router = Router()

specialists: list[Specialist]
file_message_id: int


@router.callback_query(F.data == "specialists_list", IsAdmin())
async def explore_specialists(callback: CallbackQuery,
                              session: AsyncSession):
    global specialists
    specialists = list(await session.scalars(select(Specialist).where(Specialist.status != -1)))
    await callback.answer()
    if len(specialists) == 0:
        await callback.message.answer("На данный момент, в боте нет ни одного специалиста 😢")
        return
    page = 0
    await print_specialist(specialists[page], callback, page)


async def print_specialist(specialist: Specialist,
                           callback: CallbackQuery,
                           page: int):
    global specialists
    global file_message_id
    pattern = (f"<i><b>Специалист</b>: {specialist.surname} {specialist.name}\n"
               f"О себе: {specialist.description} </i>\n\n")

    await callback.bot.send_photo(
        admin_id,
        specialist.photo_id,
        caption=pattern,
        reply_markup=paginator(page, len(specialists))
    )

    file = await callback.bot.send_document(
        chat_id=admin_id,
        document=specialist.file_id
    )
    file_message_id = file.message_id


@router.callback_query(IsAdmin(), SpecialistsFactory.filter(F.action.in_(["prev", "next"])))
async def prev_next(callback: CallbackQuery,
                    callback_data: SpecialistsFactory):
    global specialists
    global file_message_id
    page_num = int(callback_data.page)
    await callback.answer()

    page = page_num - 1 if page_num > 0 else page_num
    if callback_data.action == "next":
        page = page_num + 1 if page_num < len(specialists) - 1 else page_num

    await callback.bot.delete_message(admin_id,
                                      callback.message.message_id)
    await callback.bot.delete_message(admin_id,
                                      file_message_id)
    specialist = specialists[page]
    await print_specialist(specialist, callback, page)


@router.callback_query(IsAdmin(), F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery, session: AsyncSession):
    global file_message_id
    await callback.bot.delete_message(admin_id,
                                      callback.message.message_id)
    await callback.bot.delete_message(admin_id,
                                      file_message_id)
    await admin_start(callback.message, session)
    await callback.answer()
