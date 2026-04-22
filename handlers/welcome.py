from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States
from utils.db import get_profile

router = Router()

WELCOME_MSG = (
    "🌟 *Namaskar Beta/Beti!* 🌟\n\n"
    "Main hoon *Maharishi AstroGuru Ji*.\n"
    "Aaj hum aapki janma-jankari ke aadhaar par Vedic guidance lenge.\n\n"
    "*Disclaimer:* Yeh spiritual/astrology guidance hai, medical ya financial advice nahi.\n\n"
    "Kya shuru karein?"
)


@router.message(Command("start"))
async def start_cmd(msg: Message, state: FSMContext):
    await state.clear()

    profile = await get_profile(msg.from_user.id)
    remembered = ""
    if profile and profile.name:
        remembered = f"\n\n🧠 Mujhe yaad hai aapka naam *{profile.name}* hai."

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Haan Ji, Shuru Karein", callback_data="consent_yes")],
            [InlineKeyboardButton(text="❌ Nahi", callback_data="consent_no")],
        ]
    )
    await msg.answer(WELCOME_MSG + remembered, reply_markup=kb)
    await state.set_state(States.waiting_consent)


@router.callback_query(States.waiting_consent, F.data == "consent_yes")
async def consent_yes(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Hindi", callback_data="lang_hi")],
            [InlineKeyboardButton(text="Hinglish", callback_data="lang_hinglish")],
        ]
    )
    await callback.message.answer("Bahut badhiya. Language choose kariye:", reply_markup=kb)
    await state.set_state(States.waiting_language)
    await callback.answer()


@router.callback_query(States.waiting_consent, F.data == "consent_no")
async def consent_no(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Theek hai. Jab ready ho, /start likh dena.")
    await callback.answer()


@router.callback_query(States.waiting_language, F.data.in_({"lang_hi", "lang_hinglish"}))
async def set_language(callback: CallbackQuery, state: FSMContext):
    language = "hindi" if callback.data == "lang_hi" else "hinglish"
    await state.update_data(language=language)
    await callback.message.answer("🙏 Namaskar! Aapka naam kya hai?")
    await state.set_state(States.waiting_name)
    await callback.answer()

