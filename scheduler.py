import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from vedic_astrology_bot.utils import db


async def get_daily_horoscope(user_id: int) -> str:
    # TODO: Implement the logic to get the daily horoscope from an external API
    return "Here is your daily horoscope!"


async def send_daily_horoscope(bot: Bot) -> None:
    users = await db.get_subscribed_users()
    for user in users:
        horoscope = await get_daily_horoscope(user.user_id)
        await bot.send_message(chat_id=user.user_id, text=horoscope)


def setup_scheduler(bot: Bot) -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_horoscope, "cron", hour=8, minute=0, args=[bot])
    scheduler.start()
