from aiogram import Router, F, Dispatcher
from aiogram.types import Message
from aiogram.filters import and_f, or_f, Command
from aiogram.fsm.context import FSMContext

from db import Chat
from db.models import Specialist
from db.methods import get_partner_id, get_role, set_status

from bot.states import UserState, SpecialistState

from sqlalchemy import or_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.reply import rmk, main_user_kb

router = Router()


@router.message(
    and_f(
        or_f(Command('leave'), F.text == '💬 Завершить беседу'),
        or_f(UserState.IN_CHAT, SpecialistState.IN_CHAT))
    )
async def end_chat(message: Message,
                   state: FSMContext,
                   session: AsyncSession,
                   dispatcher: Dispatcher):
    user_id = message.from_user.id
    partner_id = await get_partner_id(session, user_id)

    role = await get_role(session=session, user_id=user_id)
    await session.execute(delete(Chat).where(or_(Chat.user_id == user_id, Chat.specialist_id == user_id)))
    await session.commit()

    if role == 'user':
        await message.answer('💤 Вы завершили чат 💤', reply_markup=rmk)
        await message.bot.send_message(partner_id, '💤 Пользователь завершил чат 💤')
        await message.bot.send_message(partner_id, '☕ <b>Продолжается поиск пользователей...</b>',
                                       reply_markup=rmk)
        await state.set_state(UserState.MENU_STATE)
        from .start_search import start
        await set_status(session, partner_id, 1)

        await dispatcher.fsm.get_context(message.bot,
                                         partner_id,
                                         partner_id).set_state(SpecialistState.AVAILABLE)
        await start(message, session, state)
    elif role == 'specialist':
        await message.answer('💤 Вы завершили чат 💤')
        await message.answer('Продолжается поиск 🔍')
        await message.bot.send_message(partner_id, '💤 Специалист завершил чат 💤')

        await set_status(session, user_id, 1)
        specialists = await session.scalars(select(Specialist).where(Specialist.status == 1))
        await message.bot.send_message(partner_id, f"<i>Отправь /chat когда будешь готов начать новый чат.\n"
                                                   f"Специалистов в сети:</i> "
                                                   f"<code>{len(specialists.fetchall())}</code>",
                                       reply_markup=main_user_kb)

        await state.set_state(SpecialistState.AVAILABLE)
        await dispatcher.fsm.get_context(message.bot,
                                         partner_id,
                                         partner_id).set_state(UserState.MENU_STATE)


@router.message(
    and_f(
        or_f(UserState.IN_CHAT, SpecialistState.IN_CHAT),
        F.content_type.in_(
            [
                "text", "photo", "video",
                "audio", "voice", "document",
                "sticker", "animation"
            ]
        )
    )
)
async def chat(message: Message,
               session: AsyncSession):
    user_id = message.from_user.id
    partner_id = await get_partner_id(session, user_id)
    if message.content_type == "text":
        reply = None
        if message.reply_to_message:
            if message.reply_to_message.from_user.id == message.from_user.id:
                reply = message.reply_to_message.message_id + 1
            else:
                reply = message.reply_to_message.message_id - 1

        await message.bot.send_message(
            partner_id,
            message.text,
            entities=message.entities,
            reply_to_message_id=reply,
            parse_mode=None
        )
    if message.content_type == "photo":
        await message.bot.send_photo(
            partner_id,
            message.photo[-1].file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            parse_mode=None,
            has_spoiler=True
        )
    if message.content_type == "video":
        await message.bot.send_video(
            partner_id,
            message.video.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            parse_mode=None,
            has_spoiler=True
        )
    if message.content_type == "audio":
        await message.bot.send_audio(
            partner_id,
            message.audio.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            parse_mode=None
        )
    if message.content_type == "voice":
        await message.bot.send_voice(
            partner_id,
            message.voice.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            parse_mode=None
        )
    if message.content_type == "document":
        await message.bot.send_document(
            partner_id,
            message.document.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            parse_mode=None
        )
    if message.content_type == "sticker":
        await message.bot.send_sticker(
            partner_id,
            message.sticker.file_id
        )
    if message.content_type == "animation":
        await message.bot.send_animation(
            partner_id,
            message.animation.file_id
        )
