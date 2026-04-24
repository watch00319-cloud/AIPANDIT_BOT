"""
Astrobot — aiogram 3.x entry point.

Environment variables required:
    BOT_TOKEN   — Telegram bot token from @BotFather
"""
from __future__ import annotations

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import welcome, birth_collection, analysis, pitch, extras, questions
from utils.db import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set.")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Register all routers
    dp.include_router(welcome.router)
    dp.include_router(birth_collection.router)
    dp.include_router(analysis.router)
    dp.include_router(pitch.router)
    dp.include_router(extras.router)
    dp.include_router(questions.router)

    # Initialise database tables
    await init_db()

    logger.info("Starting bot polling…")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except TelegramUnauthorizedError:
        logger.error("Invalid BOT_TOKEN — TelegramUnauthorizedError. Check your token.")
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
from handlers.start import router as start_router

dp.include_router(start_router)
