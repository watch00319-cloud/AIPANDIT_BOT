<<<<<<< HEAD
import asyncio
import argparse
import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from scheduler import send_daily_horoscope

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def test_notification(user_id: int = None):
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found in .env")
        return
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
    try:
        if user_id:
            print(f"Sending test notification to user {user_id}...")
            await bot.send_message(chat_id=user_id, text="🌅 *Test Daily Horoscope!*\\nThis is a test notification. Full personalized version sends daily at 8AM to subscribers.")
        else:
            print("Sending to all subscribed users...")
            await send_daily_horoscope(bot)
        print("Test complete!")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Telegram notifications")
    parser.add_argument("user_id", nargs="?", type=int, help="Specific user ID for test")
    args = parser.parse_args()
    asyncio.run(test_notification(args.user_id))

=======
import asyncio
import argparse
import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from scheduler import send_daily_horoscope

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def test_notification(user_id: int = None):
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found in .env")
        return
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
    try:
        if user_id:
            print(f"Sending test notification to user {user_id}...")
            await bot.send_message(chat_id=user_id, text="🌅 *Test Daily Horoscope!*\\nThis is a test notification. Full personalized version sends daily at 8AM to subscribers.")
        else:
            print("Sending to all subscribed users...")
            await send_daily_horoscope(bot)
        print("Test complete!")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Telegram notifications")
    parser.add_argument("user_id", nargs="?", type=int, help="Specific user ID for test")
    args = parser.parse_args()
    asyncio.run(test_notification(args.user_id))

>>>>>>> 40b3d60c9adedf500ad2701085ecaf61dba3ab37
