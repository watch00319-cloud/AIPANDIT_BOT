import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import welcome, birth_collection, analysis, questions, pitch, extras
from utils.db import init_db


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


async def main() -> None:
    if not TOKEN:
        raise ValueError("BOT_TOKEN missing. Add BOT_TOKEN in .env")

    await init_db()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(welcome.router)
    dp.include_router(birth_collection.router)
    dp.include_router(analysis.router)
    dp.include_router(questions.router)
    dp.include_router(pitch.router)
    dp.include_router(extras.router)

    logging.info("Bot polling started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
