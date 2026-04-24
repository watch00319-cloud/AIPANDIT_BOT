import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram.exceptions import TelegramUnauthorizedError

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers.welcome import router as welcome_router
from handlers.payment import router as payment_router
from handlers.birth_collection import router as birth_collection_router
from handlers.start import router as start_router
from handlers.extras import router as extras_router
from handlers.analysis import router as analysis_router
from handlers.questions import router as questions_router
from handlers.pitch import router as pitch_router




async def main():
    logging.basicConfig(level=logging.INFO)
    
    load_dotenv()
    TOKEN = os.getenv('BOT_TOKEN')
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is missing. Set it in .env or deployment env vars.")

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Validate token
    try:
        me = await bot.get_me()
        logging.info(f"✅ Bot @{me.username} (ID: {me.id}) is ready!")
    except TelegramUnauthorizedError:
        raise ValueError("❌ Invalid BOT_TOKEN. Create new bot with @BotFather and update env var.") from None

    dp = Dispatcher()

    # router connect
    dp.include_router(welcome_router)
    dp.include_router(payment_router)
    dp.include_router(birth_collection_router)
    dp.include_router(start_router)
    dp.include_router(extras_router)
    dp.include_router(analysis_router)
    dp.include_router(questions_router)
    dp.include_router(pitch_router)

    print("🚀 Bot Started...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())