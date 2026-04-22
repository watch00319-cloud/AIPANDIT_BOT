"""
Extras handler — /help, /reset, daily Gochara teaser, compatibility teaser.

These are utility commands and inline-button callbacks that can be triggered
from any state.
"""

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from states.main import States
from utils.astrology import compatibility_teaser, daily_gochara_teaser, get_rashi
from utils.db import get_profile

logger = logging.getLogger(__name__)
router = Router(name="extras")

EXTRAS_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌙 Aaj ka Gochara", callback_data="gochara"),
            InlineKeyboardButton(text="💑 Compatibility", callback_data="compatibility"),
        ],
        [InlineKeyboardButton(text="🔄 Restart", callback_data="restart")],
    ]
)

HELP_MSG = (
    "🌟 *Maharishi AstroGuru Ji — Help* 🌟\n\n"
    "Yahan jo commands available hain:\n\n"
    "• /start — Nayi consultation shuru karein\n"
    "• /help  — Yeh message dikhayein\n"
    "• /reset — Apna session reset karein\n\n"
    "Aap neeche ke buttons se bhi kuch dekh sakte hain:"
)


# ---------------------------------------------------------------------------
# /help
# ---------------------------------------------------------------------------


@router.message(Command("help"))
async def cmd_help(msg: Message) -> None:
    await msg.answer(HELP_MSG, reply_markup=EXTRAS_KB)
    logger.info("User %s requested /help", msg.from_user.id)


# ---------------------------------------------------------------------------
# /reset
# ---------------------------------------------------------------------------


@router.message(Command("reset"))
async def cmd_reset(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        "🔄 Aapka session reset ho gaya.\n"
        "Dobara shuru karne ke liye /start likhein. 🙏"
    )
    logger.info("User %s reset their session", msg.from_user.id)


# ---------------------------------------------------------------------------
# Gochara teaser callback
# ---------------------------------------------------------------------------


@router.callback_query(F.data == "gochara")
async def gochara_callback(cb: CallbackQuery) -> None:
    await cb.answer()
    profile = await get_profile(cb.from_user.id)

    if profile and profile.dob:
        rashi_hi, _ = get_rashi(profile.dob)
    else:
        rashi_hi = "Aapki"

    teaser = daily_gochara_teaser(rashi_hi)
    await cb.message.answer(teaser)
    logger.info("User %s requested gochara teaser", cb.from_user.id)


# ---------------------------------------------------------------------------
# Compatibility teaser callback
# ---------------------------------------------------------------------------


@router.callback_query(F.data == "compatibility")
async def compatibility_callback(cb: CallbackQuery) -> None:
    await cb.answer()
    profile = await get_profile(cb.from_user.id)

    if profile and profile.dob:
        rashi_hi, _ = get_rashi(profile.dob)
    else:
        rashi_hi = "Aapki Rashi"

    # Use a generic partner rashi for the teaser
    teaser = compatibility_teaser(rashi_hi, "Vrishabh")
    await cb.message.answer(teaser)
    logger.info("User %s requested compatibility teaser", cb.from_user.id)
