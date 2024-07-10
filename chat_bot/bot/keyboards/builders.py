from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from db.models import Specialist
from bot.fabrics.callback_factory import CallbackFactory, SpecialistsFactory


def approve_dismiss(specialist: Specialist):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Утвердить анкету",
        callback_data=CallbackFactory(action='approve', value=specialist.id)
    )
    builder.button(
        text="Отклонить анкету",
        callback_data=CallbackFactory(action='dismiss', value=specialist.id)
    )
    builder.adjust(2)
    return builder.as_markup()


def admin_menu_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Новые заявки", callback_data="new_application")
    keyboard.button(text="Cпециалисты", callback_data="specialists_list")
    keyboard.button(text="Обновить", callback_data='update')
    keyboard.adjust(2)
    return keyboard.as_markup()


def paginator(page: int, total: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅", callback_data=SpecialistsFactory(action="prev", page=page))
    keyboard.button(text=f"{page + 1}/{total}", callback_data='nothing')
    keyboard.button(text="➡", callback_data=SpecialistsFactory(action="next", page=page))
    keyboard.button(text="Вернуться в меню", callback_data="admin_menu")
    keyboard.adjust(3)
    return keyboard.as_markup()


def no_applications_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Вернуться в меню", callback_data='update')
    return keyboard.as_markup()
