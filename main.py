"""
Vedic Astrology Telegram Bot — entry point.

Runs aiogram 3.x polling. Works locally (reads .env) and on Railway /
any PaaS (reads platform-injected environment variables).
"""

import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.filters import StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

# Relative imports
from states.main import States
from utils.db import get_profile, init_db
from dotenv import load_dotenv

from handlers.welcome import router as welcome_router, WELCOME_MSG
from handlers.birth_collection import router as birth_collection_router
from handlers.analysis import router as analysis_router
from handlers.pitch import router as pitch_router
from handlers.extras import router as extras_router
from handlers.subscription import router as subscription_router
from vedic_astrology_bot.scheduler import setup_scheduler
from fallback_handler import router as fallback_router

from fallback_handler import router as fallback_router


# Configuration & logging
load_dotenv()

BOT_TOKEN = (os.getenv("BOT_TOKEN") or "").strip()
LOG_LEVEL = (os.getenv("LOG_LEVEL") or "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("vedic_astrology_bot")


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

    @dp.message(StateFilter(None), F.text & ~F.text.startswith("/"))
    async def auto_start_flow(msg: Message, state: FSMContext):
        """Auto-trigger welcome on any non-command text when no state active."""
        await state.clear()

        profile = await get_profile(msg.from_user.id)
        remembered = ""
        if profile and profile.name:
            remembered = f"\n\n🧠 Mujhe yaad hai aapka naam *{profile.name}* hai."

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Haan Ji, Shuru Karein", callback_data="consent_yes")],
                [InlineKeyboardButton(text="❌ Abhi Nahi", callback_data="consent_no")],
            ]
        )
        await msg.answer(WELCOME_MSG + remembered, reply_markup=kb)
        await state.set_state(States.waiting_consent)

    dp.include_router(welcome_router)
    dp.include_router(birth_collection_router)
    dp.include_router(analysis_router)
    dp.include_router(pitch_router)
    dp.include_router(extras_router)
    dp.include_router(subscription_router)
    dp.include_router(fallback_router)

    @dp.message(Command("myid"))
    async def myid_cmd(msg: Message):
        await msg.answer(f"🆔 Your user ID: `{msg.from_user.id}`\\nUse for test notifications.")

    @dp.message(Command("status"))
    async def status_cmd(msg: Message, state: FSMContext):
        current = await state


# Configuration & logging
load_dotenv()

BOT_TOKEN = (os.getenv("BOT_TOKEN") or "").strip()
LOG_LEVEL = (os.getenv("LOG_LEVEL") or "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("vedic_astrology_bot")


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

    @dp.message(StateFilter(None), F.text & ~F.text.startswith("/"))
    async def auto_start_flow(msg: Message, state: FSMContext):
        """Auto-trigger welcome on any non-command text when no state active."""
        await state.clear()

        profile = await get_profile(msg.from_user.id)
        remembered = ""
        if profile and profile.name:
            remembered = f"\n\n🧠 Mujhe yaad hai aapka naam *{profile.name}* hai."

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Haan Ji, Shuru Karein", callback_data="consent_yes")],
                [InlineKeyboardButton(text="❌ Abhi Nahi", callback_data="consent_no")],
            ]
        )
        await msg.answer(WELCOME_MSG + remembered, reply_markup=kb)
        await state.set_state(States.waiting_consent)

    dp.include_router(welcome_router)
    dp.include_router(birth_collection_router)
    dp.include_router(analysis_router)
    dp.include_router(pitch_router)
    dp.include_router(extras_router)
    dp.include_router(subscription_router)

    setup_scheduler(bot)
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
aftefixfix
