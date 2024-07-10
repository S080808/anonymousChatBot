from aiogram import Router, F
from aiogram.types import Message
from bot.states.states import UserState

router = Router()


@router.message(F.text == '💬 Искусственный интелект', UserState.MENU_STATE)
async def ai(message: Message):
    await message.answer(f"<i>Попробуйте нашего чат-бота с <b>искусственным интеллектом!</b></i>")
    await message.answer_photo(
        photo='AgACAgIAAxkBAAIIxWY5awjotAZD2Wsm1rYVIK1FPGNTAAKj2TEbR8nRSaPNV6VM6IpYAQADAgADeAADNQQ',
        caption=f"<i>Что умеет бот:</i>\n"
                f"- <b>Расшифровывать и анализировать голосовые сообщения.</b>\n"
                f"- <b>Вести дневник настроения.</b>\n"
                f"- <b>Проводить медитационные сеансы.</b>\n\n"
                f"<i>Нажми <a href='https://t.me/MindMate_robot?start'>сюда</a>"
                f" и переходи к <b>Бамбучо</b>.</i>"
    )
