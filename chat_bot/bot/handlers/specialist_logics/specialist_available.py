from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db.methods import set_status

from bot.states import SpecialistState

from sqlalchemy.ext.asyncio import AsyncSession


from bot.handlers.main_menu import start
router = Router()


@router.message(Command('stop'), SpecialistState.AVAILABLE)
async def end_search(message: Message, state: FSMContext, session: AsyncSession):
    await set_status(session, message.from_user.id, 0)
    await message.reply("<b>💤 Вы завершили поиск 💤</b>")
    await start(message, session, state)


@router.message(SpecialistState.AVAILABLE)
async def wrong_text(message: Message):
    await message.answer('Нет такого варианта 🤔')

