from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

router = Router()

WELCOME_MSG = """
🔮 *Welcome to Decode Your Future*

✨ Aapke paas FREE trial hai (2 minute)

👉 Aap koi bhi question pooch sakte hain
👉 Sirf 2 minute ke liye free reading milegi

⚠️ Uske baad paid service lagegi

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
