from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    MENU_STATE = State()
    IN_CHAT = State()


class SpecialistState(StatesGroup):
    MENU_STATE = State()
    AVAILABLE = State()
    IN_CHAT = State()


class SpecialistRegisterState(StatesGroup):
    WAIT_FOR_NAME = State()
    WAIT_FOR_SURNAME = State()
    WAIT_FOR_AGE = State()
    WAIT_FOR_PHOTO = State()
    WAIT_FOR_DESCRIPTION = State()
    WAIT_FOR_RESUME = State()
    WAIT_FOR_MODERATION = State()
