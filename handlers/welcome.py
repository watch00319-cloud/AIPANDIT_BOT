<<<<<<< HEAD
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States
from utils.db import get_profile
from .payment import trigger_payment

router = Router()

WELCOME_MSG = (
    "🔮 Welcome to Decode Your Future  \n"
    "⏳ You have 2 minutes FREE access  \n"
    "Ask any question"
)
=======
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

router = Router()

WELCOME_MSG = """
🔮 *Welcome to Decode Your Future*
>>>>>>> 2fd36d67402011f51df74a20dadb87967d0d8394

✨ Aapke paas FREE trial hai (2 minute)

👉 Aap koi bhi question pooch sakte hain
👉 Sirf 2 minute ke liye free reading milegi

<<<<<<< HEAD
    if await trigger_payment(msg):
        return

    profile = await get_profile(msg.from_user.id)
    remembered = ""
    if profile and profile.name:
        remembered = f"\n\n🧠 Mujhe yaad hai aapka naam *{profile.name}* hai."
=======
⚠️ Uske baad paid service lagegi
>>>>>>> 2fd36d67402011f51df74a20dadb87967d0d8394

Ready ho?
"""

@router.callback_query(lambda c: c.data == "consent_yes")
async def start_reading(callback):
    await callback.message.answer("🧠 Apna sawal likhiye...")
    await callback.answer()

@router.callback_query(lambda c: c.data == "consent_no")
async def cancel(callback):
    await callback.message.answer("👍 Theek hai, jab ready ho tab aa jana.")
    await callback.answer()
