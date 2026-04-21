import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import welcome, birth_collection, analysis, questions, pitch, extras
from utils.db import init_db


# Load .env if present (local dev). On Railway / any PaaS, env vars are
# injected by the platform directly, so missing .env is fine.
load_dotenv()
TOKEN = (os.getenv("BOT_TOKEN") or "").strip()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not TOKEN:
        logger.error(
            "BOT_TOKEN is not set. "
            "Local dev: create a `.env` file with BOT_TOKEN=<your_token>. "
            "Railway / PaaS: add BOT_TOKEN under the service's Variables tab, "
            "then redeploy."
        )
        sys.exit(1)

    await init_db()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(welcome.router)
    dp.include_router(birth_collection.router)
    dp.include_router(analysis.router)
    dp.include_router(questions.router)
    dp.include_router(pitch.router)
    dp.include_router(extras.router)

    logger.info("Bot polling started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
