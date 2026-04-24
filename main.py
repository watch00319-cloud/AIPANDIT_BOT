```python
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers.onboarding import router as onboarding_router

TOKEN = "YOUR_BOT_TOKEN_HERE"  # <-- yaha apna token daalo

async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    # ✅ IMPORTANT: onboarding router connect
    dp.include_router(onboarding_router)

    print("✅ Bot is running...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```
