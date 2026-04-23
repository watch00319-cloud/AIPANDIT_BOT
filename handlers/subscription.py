from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..utils import db

router = Router()


@router.message(Command("subscribe"))
async def subscribe(message: Message) -> None:
    user_id = message.from_user.id
    await db.upsert_profile(user_id, {"horoscope_subscribed": True})
    await message.reply("✅ *Subscribed to free daily horoscope!* 🌅\nHar subah aapka personalized kundali based message milega.\n/unsubscribe to stop.")


@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message) -> None:
    user_id = message.from_user.id
    await db.upsert_profile(user_id, {"horoscope_subscribed": False})
    await message.reply("❌ *Unsubscribed from daily horoscope.*\nKoi baat nahi, jab chahiye /subscribe kar lena.")

