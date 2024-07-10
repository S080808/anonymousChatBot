import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.middlewares import SessionMiddleware
from config_reader import config
from db.base import Base
from bot.handlers import setup_handlers

dp = None

async def on_startup(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def on_shutdown(session: AsyncSession) -> None:
    await session.close()


async def main() -> None:
    engine = create_async_engine(config.DATABASE_URL.get_secret_value())
    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

    bot = Bot(token=config.BOT_TOKEN.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    global dp
    dp = Dispatcher(engine=engine)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(SessionMiddleware(session_maker))
    dp.callback_query.middleware(SessionMiddleware(session_maker))
    routers = setup_handlers()
    dp.include_router(routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
