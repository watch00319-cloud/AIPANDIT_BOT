"""
Welcome handler — /start command, consent flow, and language selection.

Conversation steps handled here:
  1. /start  → show disclaimer + consent keyboard
  2. consent_yes callback → ask for language preference
  3. consent_no  callback → polite goodbye
  4. lang_hi / lang_en callbacks → set language, hand off to birth_collection
"""

import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from states.main import States
from utils.db import get_profile, upsert_profile

logger = logging.getLogger(__name__)
router = Router(name="welcome")

# ---------------------------------------------------------------------------
# Copy / keyboard helpers
# ---------------------------------------------------------------------------

WELCOME_MSG = (
    "🌟 *Namaskar Beta/Beti!* 🌟\n\n"
    "Main hoon *Maharishi AstroGuru Ji*.\n"
    "Aaj hum aapki janma-jankari ke aadhaar par Vedic guidance lenge.\n\n"
    "*Disclaimer:* Yeh spiritual/astrology guidance hai, "
    "medical ya financial advice nahi.\n\n"
    "Kya shuru karein?"
)

CONSENT_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Haan Ji, Shuru Karein", callback_data="consent_yes")],
        [InlineKeyboardButton(text="❌ Nahi", callback_data="consent_no")],
    ]
)

LANGUAGE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇮🇳 Hindi / Hinglish", callback_data="lang_hi")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
    ]
)


# ---------------------------------------------------------------------------
# /start
# ---------------------------------------------------------------------------


@router.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext) -> None:
    await state.clear()

    profile = await get_profile(msg.from_user.id)
    remembered = ""
    if profile and profile.name:
        remembered = f"\n\n🧠 Mujhe yaad hai aapka naam *{profile.name}* hai."

    await msg.answer(WELCOME_MSG + remembered, reply_markup=CONSENT_KB)
    await state.set_state(States.waiting_consent)
    logger.info("User %s started the bot", msg.from_user.id)


# ---------------------------------------------------------------------------
# Consent callbacks
# ---------------------------------------------------------------------------


@router.callback_query(F.data == "consent_yes", States.waiting_consent)
async def consent_yes(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "🙏 Bahut achha! Pehle batayein — aap kis bhasha mein baat karna chahte hain?",
        reply_markup=LANGUAGE_KB,
    )
    await state.set_state(States.waiting_language)


@router.callback_query(F.data == "consent_no", States.waiting_consent)
async def consent_no(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "🙏 Theek hai. Jab bhi taiyaar hon, /start karein. Jai Shri Krishna! 🌸"
    )
    await state.clear()


# ---------------------------------------------------------------------------
# Language selection callbacks
# ---------------------------------------------------------------------------


@router.callback_query(F.data.in_({"lang_hi", "lang_en"}), States.waiting_language)
async def choose_language(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    lang = "hi" if cb.data == "lang_hi" else "en"
    await upsert_profile(cb.from_user.id, language=lang)
    await state.update_data(language=lang)

    await cb.message.edit_reply_markup(reply_markup=None)

    if lang == "hi":
        prompt = "👍 Hindi/Hinglish mein baat karenge!\n\nAb aapka *poora naam* batayein:"
    else:
        prompt = "👍 We'll chat in English!\n\nPlease share your *full name*:"

    await cb.message.answer(prompt)
    await state.set_state(States.waiting_name)
    logger.info("User %s chose language=%s", cb.from_user.id, lang)
