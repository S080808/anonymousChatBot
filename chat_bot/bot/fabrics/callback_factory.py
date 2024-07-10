from typing import Union
from aiogram.filters.callback_data import CallbackData


class CallbackFactory(CallbackData, prefix="fabcall"):
    action: str
    value: Union[int]


class SpecialistsFactory(CallbackData, prefix="fabspec"):
    action: str
    page: int
