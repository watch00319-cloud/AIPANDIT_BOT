import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import db
from utils.astrology import build_kundli_teaser, daily_gochara_text


async def get_daily_horoscope(user_id: int) -> str:
    profile = await db.get_profile(user_id)
    if profile and profile.name and profile.dob and profile.tob and profile.lat and profile.lon:
        return build_kundli_teaser(profile.name, profile.dob, profile.tob, profile.lat, profile.lon)
    return daily_gochara_text()



async def send_daily_horoscope(bot: Bot) -> None:
    users = await db.get_subscribed_users()
    for user in users:
        horoscope = await get_daily_horoscope(user.user_id)
        await bot.send_message(chat_id=user.user_id, text=horoscope)


def setup_scheduler(bot: Bot) -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_horoscope, "cron", hour=8, minute=0, args=[bot])
    scheduler.start()

