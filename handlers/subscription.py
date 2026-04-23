from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from vedic_astrology_bot.utils import db

router = Router()


@router.message(Command("subscribe"))
async def subscribe(message: Message) -> None:
    user_id = message.from_user.id
    await db.upsert_profile(user_id, {"horoscope_subscribed": True})
    await message.reply("You have subscribed to daily horoscopes!")


@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message) -> None:
    user_id = message.from_user.id
    await db.upsert_profile(user_id, {"horoscope_subscribed": False})
    await message.reply("You have unsubscribed from daily horoscopes.")
