import pytest

from bot.handlers.specialist_logics.register_specialist import (
    i_am_specialist,
    register,
    name,
    surname,
    age,
    photo,
    description,
    resume
)

from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE

from bot.states import SpecialistRegisterState, UserState
from bot.keyboards.reply import rmk, register_kb


@pytest.mark.asyncio
async def test_i_am_specialist():
    request = MockedBot(MessageHandler(i_am_specialist, state=UserState.MENU_STATE))
    calls = await request.query(message=MESSAGE.as_object(text="👨‍⚕️ Я специалист"))
    answer_message = calls.send_message.fetchmany(3)

    assert answer_message[0].text.startswith("<b>Приветствуем вас в разделе регистрации специалистов!")
    assert answer_message[1].text.startswith("<b>🔹 Как стать специалистом:")
    assert answer_message[2].text.startswith("<b>🔹 Ваши преимущества:")
    assert answer_message[2].reply_markup == register_kb


@pytest.mark.asyncio
async def test_register():
    request = MockedBot(MessageHandler(register, state=UserState.MENU_STATE))
    calls = await request.query(message=MESSAGE.as_object(text="💬 Начать регистрацию"))
    answer_message = calls.send_message.fetchmany(2)

    assert answer_message[0].text == "Прекрасно, начнем регистрацию 😎"
    assert answer_message[1].text == "Введите, пожалуйста, своё имя:"
    assert answer_message[1].reply_markup == rmk


@pytest.mark.asyncio
async def test_name():
    request = MockedBot(MessageHandler(name, state=SpecialistRegisterState.WAIT_FOR_NAME))
    calls = await request.query(message=MESSAGE.as_object(text="Иван"))
    answer_message = calls.send_message.fetchone()

    assert answer_message.text == "Теперь введите вашу фамилию:"


@pytest.mark.asyncio
async def test_surname():
    request = MockedBot(MessageHandler(surname, state=SpecialistRegisterState.WAIT_FOR_SURNAME))
    calls = await request.query(message=MESSAGE.as_object(text="Иванов"))
    answer_message = calls.send_message.fetchmany(2)

    assert answer_message[0].text == "Отлично, <b>Иванов Иван</b>"
    assert answer_message[1].text == "Введите ваш возраст:"


@pytest.mark.asyncio
async def test_age():
    request = MockedBot(MessageHandler(age, state=SpecialistRegisterState.WAIT_FOR_AGE))
    calls = await request.query(message=MESSAGE.as_object(text="30"))
    answer_message = calls.send_message.fetchone()

    assert answer_message.text == "Отправьте, пожалуйста, свою фотографию:"


@pytest.mark.asyncio
async def test_photo():
    request = MockedBot(MessageHandler(photo, state=SpecialistRegisterState.WAIT_FOR_PHOTO))
    photo_message = MESSAGE.as_object(photo=[{"file_id": "12345"}])
    calls = await request.query(message=photo_message)
    answer_message = calls.send_message.fetchone()

    assert answer_message.text == "Расскажите о себе в двух словах 😇"


@pytest.mark.asyncio
async def test_description():
    request = MockedBot(MessageHandler(description, state=SpecialistRegisterState.WAIT_FOR_DESCRIPTION))
    calls = await request.query(message=MESSAGE.as_object(text="Я опытный специалист."))
    answer_message = calls.send_message.fetchone()

    assert answer_message.text.startswith("Отправьте, пожалуйста, документ, подтверждающий квалификацию:")


@pytest.mark.asyncio
async def test_resume():
    request = MockedBot(MessageHandler(resume, state=SpecialistRegisterState.WAIT_FOR_RESUME))
    document_message = MESSAGE.as_object(document={"file_id": "67890"})
    calls = await request.query(message=document_message)
    answer_message = calls.send_message.fetchmany(2)

    assert answer_message[0].text == "Отлично, ваша анкета отправлена на модерацию ✍️"
    assert answer_message[1].text == "Когда она будет подтверждена, Вам придет <b>уведомление</b> 💬"
