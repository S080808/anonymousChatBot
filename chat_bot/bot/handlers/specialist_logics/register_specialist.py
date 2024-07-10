from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import SpecialistRegisterState, UserState
from db.models import Specialist

from bot.keyboards.reply import rmk, register_kb

router = Router()


@router.message(F.text == "👨‍⚕️ Я специалист",
                UserState.MENU_STATE)
async def i_am_specialist(message: Message):
    await message.answer(text="<b>Приветствуем вас в разделе регистрации специалистов! 🌟</b>\n<i>Чтобы начать "
                              "помогать другим анонимно, пройдите несколько шагов регистрации.</i>", reply_markup=rmk)
    await message.answer(text="<b>🔹 Как стать специалистом:</b>\n<i>Загрузите ваше фото и документы,"
                              " подтверждающие квалификацию (например, резюме или диплом).</i>")
    await message.answer(text="<b>🔹 Ваши преимущества:\n<u>Вы получите доступ к платформе для оказания поддержки "
                              "и возможность развития своих профессиональных навыков.</u>\nСпасибо за ваш выбор "
                              "помогать через нашего бота! 💖</b>", reply_markup=register_kb)


@router.message(F.text == "💬 Начать регистрацию", UserState.MENU_STATE)
async def register(message: Message, state: FSMContext):
    await message.answer("Прекрасно, начнем регистрацию 😎")
    await message.answer("Введите, пожалуйста, своё имя:", reply_markup=rmk)
    await state.set_state(SpecialistRegisterState.WAIT_FOR_NAME)


@router.message(F.text == "❌ Вернуться в меню")
async def return_to_menu(message: Message, state: FSMContext, session: AsyncSession):
    from bot.handlers.main_menu import start
    await start(message, session, state)


@router.message(SpecialistRegisterState.WAIT_FOR_NAME)
async def name(message: Message, state: FSMContext):
    if message.content_type != "text":
        await message.reply("Введите, пожалуйста, ваше имя 🤔")
        return
    await state.update_data(name=message.text)
    await state.set_state(SpecialistRegisterState.WAIT_FOR_SURNAME)
    await message.answer("Теперь введите вашу фамилию:")


@router.message(SpecialistRegisterState.WAIT_FOR_SURNAME)
async def surname(message: Message, state: FSMContext):
    if message.content_type != "text":
        await message.reply("Введите, пожалуйста, вашу фамилию 🤔")
        return
    await state.update_data(surname=message.text)
    await state.set_state(SpecialistRegisterState.WAIT_FOR_AGE)

    data = await state.get_data()
    await message.reply(f"Отлично, <b>{data['surname']} {data['name']}</b>")

    await message.answer("Введите ваш возраст:")


@router.message(SpecialistRegisterState.WAIT_FOR_AGE)
async def age(message: Message, state: FSMContext):
    if message.content_type != "text" or not message.text.isdigit():
        await message.reply("Введите, пожалуйста, корректный возраст 🤔")
        return
    await state.update_data(age=message.text)
    await state.set_state(SpecialistRegisterState.WAIT_FOR_PHOTO)
    await message.answer("Отправьте, пожалуйста, свою фотографию:")


@router.message(SpecialistRegisterState.WAIT_FOR_PHOTO)
async def photo(message: Message, state: FSMContext):
    if message.content_type != "photo":
        await message.reply("Отправьте, пожалуйста, свою фотографию 🤔")
        return
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(SpecialistRegisterState.WAIT_FOR_DESCRIPTION)
    await message.reply("Расскажите о себе в двух словах 😇")


@router.message(SpecialistRegisterState.WAIT_FOR_DESCRIPTION)
async def description(message: Message, state: FSMContext):
    if message.content_type != "text":
        await message.reply("Расскажите о себе текстом, пожалуйста 🤖")
        return
    await state.update_data(description=message.text)
    await state.set_state(SpecialistRegisterState.WAIT_FOR_RESUME)
    await message.reply("Отправьте, пожалуйста, документ, подтверждающий квалификацию: \n"
                        "<tg-spoiler>(Желательно в формате pdf 💎)</tg-spoiler>")


@router.message(SpecialistRegisterState.WAIT_FOR_RESUME)
async def resume(message: Message, state: FSMContext, session: AsyncSession):
    if message.content_type != "document":
        await message.reply("Некорректный формат документа 😖")
        return
    data = await state.get_data()

    await state.set_state(SpecialistRegisterState.WAIT_FOR_MODERATION)
    await message.answer("Отлично, ваша анкета отправлена на модерацию ✍️")
    await message.answer("Когда она будет подтверждена, Вам придет <b>уведомление</b> 💬")

    session.add(Specialist(id=message.from_user.id,
                           name=data["name"],
                           surname=data["surname"],
                           age=data["age"],
                           photo_id=data["photo"],
                           description=data["description"],
                           file_id=message.document.file_id,
                           status=-1))
    await session.commit()
