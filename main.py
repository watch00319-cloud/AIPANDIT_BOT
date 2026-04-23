"""Vedic Astrology Telegram Bot - Main entrypoint."""
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

import handlers.welcome
import handlers.birth_collection
import handlers.analysis
import handlers.pitch
import handlers.subscription
import handlers.extras
import fallback_handler
# Assume questions.py exists
# import handlers.questions
from utils.db import init_db
from scheduler import setup_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode="Markdown"))
    dp = Dispatcher()
    
    # Include all routers
    dp.include_router(welcome.router)
    dp.include_router(birth_collection.router)
    dp.include_router(analysis.router)
    dp.include_router(pitch.router)
    dp.include_router(subscription.router)
    dp.include_router(extras.router)
    dp.include_router(fallback_handler.router)
    # dp.include_router(questions.router) # if exists
    
    # Init
    await init_db()
    logger.info("Initializing database ...")
    
    setup_scheduler(bot)
    
    logger.info("Bot polling started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

