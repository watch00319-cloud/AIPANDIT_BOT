"""
Vedic Astrology Telegram Bot — entry point.

Runs aiogram 3.x polling. Works locally (reads .env) and on Railway /
any PaaS (reads platform-injected environment variables).
"""

import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Absolute imports — works when `/app/` (Railway) or the project root
# (local dev) is on sys.path.
from handlers.welcome import router as welcome_router
from handlers.birth_collection import router as birth_collection_router
from handlers.analysis import router as analysis_router
from handlers.questions import router as questions_router
from handlers.pitch import router as pitch_router
from handlers.extras import router as extras_router
from utils.db import init_db


# ---------------------------------------------------------------------------
# Configuration & logging
# ---------------------------------------------------------------------------

# Load .env when running locally. On Railway / any PaaS, environment
# variables are injected directly and this is a harmless no-op.
load_dotenv()

BOT_TOKEN = (os.getenv("BOT_TOKEN") or "").strip()
LOG_LEVEL = (os.getenv("LOG_LEVEL") or "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("vedic_astrology_bot")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main() -> None:
    if not BOT_TOKEN:
        logger.error(
            "BOT_TOKEN is not set. "
            "Local dev: create a `.env` file with BOT_TOKEN=<your_token>. "
            "Railway / PaaS: add BOT_TOKEN under the service's Variables tab, "
            "then redeploy."
        )
        sys.exit(1)

    logger.info("Initializing database ...")
    await init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(welcome_router)
    dp.include_router(birth_collection_router)
    dp.include_router(analysis_router)
    dp.include_router(questions_router)
    dp.include_router(pitch_router)
    dp.include_router(extras_router)

    logger.info("Bot polling started")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except TelegramUnauthorizedError:
        logger.error(
            "BOT_TOKEN was rejected by Telegram (Unauthorized). "
            "The token is invalid or has been revoked. "
            "Generate a new token via @BotFather and update the BOT_TOKEN env var."
        )
        sys.exit(1)
    finally:
        logger.info("Shutting down bot ...")
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user / system")
    except Exception:
        logger.exception("Fatal error: bot crashed")
        sys.exit(1)
