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


@router.message(Command("start"))
async def start_cmd(msg: Message, state: FSMContext):
    await state.clear()

    if await trigger_payment(msg):
        return

    profile = await get_profile(msg.from_user.id)
    remembered = ""
    if profile and profile.name:
        remembered = f"\n\n🧠 Mujhe yaad hai aapka naam *{profile.name}* hai."

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Haan Ji, Shuru Karein", callback_data="consent_yes")],
            [InlineKeyboardButton(text="❌ Abhi Nahi", callback_data="consent_no")],
        ]
    )
    await msg.answer(WELCOME_MSG + remembered, reply_markup=kb)
    await state.set_state(States.waiting_consent)


@router.callback_query(States.waiting_consent, F.data == "consent_yes")
async def consent_yes(callback: CallbackQuery, state: FSMContext):
    # Default to hinglish — skip language prompt for faster flow
    await state.update_data(language="hinglish")
    await callback.message.answer(
        "🙏 *Bahut badhiya!*\n\n"
        "Sabse pehle, kripya apna *poora naam* batayein:"
    )
    await state.set_state(States.waiting_name)
    await callback.answer()


@router.callback_query(States.waiting_consent, F.data == "consent_no")
async def consent_no(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "🙏 Koi baat nahi. Jab ready ho, /start likh dena.\n"
        "Aapka future aapka intezaar kar raha hai. 🌟"
    )
    await callback.answer()


@router.callback_query(States.waiting_language, F.data.in_({"lang_hi", "lang_hinglish"}))
async def set_language(callback: CallbackQuery, state: FSMContext):
    """Legacy handler — kept for backward compatibility."""
    language = "hindi" if callback.data == "lang_hi" else "hinglish"
    await state.update_data(language=language)
    await callback.message.answer("🙏 Apna *poora naam* batayein:")
    await state.set_state(States.waiting_name)
    await callback.answer()
