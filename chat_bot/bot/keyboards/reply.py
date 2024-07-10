from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

rmk = ReplyKeyboardRemove()

main_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="☕ Искать специалиста")],
        [KeyboardButton(text="👨‍⚕️ Я специалист")],
        [KeyboardButton(text="💬 Искусственный интелект")]
    ],
    resize_keyboard=True
)

main_specialist_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="☕ Начать поиск пользователей")]
    ],
    resize_keyboard=True
)

leave_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Завершить беседу")]
    ],
    resize_keyboard=True
)

register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Начать регистрацию")],
        [KeyboardButton(text="❌ Вернуться в меню")]
    ],
    resize_keyboard=True
)
