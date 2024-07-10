from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from bot.config_reader import config


class IsAdmin(BaseFilter):
    async def __call__(self, message_or_callback: Union[Message, CallbackQuery]) -> bool:
        admin_id = config.ADMIN_ID.get_secret_value()
        return str(message_or_callback.from_user.id) == admin_id
