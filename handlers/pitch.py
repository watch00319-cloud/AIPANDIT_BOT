"""
Pitch handler — presents the premium consultation offer and WhatsApp CTA.

States handled:
  - States.waiting_pitch
"""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from states.main import States
from utils.db import get_profile

logger = logging.getLogger(__name__)
router = Router(name="pitch")

WHATSAPP_NUMBER = "6283941933"
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}"

PITCH_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📲 WhatsApp Par Sampark Karein",
                url=WHATSAPP_URL,
            )
        ],
        [InlineKeyboardButton(text="🔄 Dobara Shuru Karein", callback_data="restart")],
    ]
)


PITCH_MSG = (
    "🌟 *Maharishi AstroGuru Ji ka Vishesh Offer* 🌟\n\n"
    "Aapki kundli aur jawaabon ke aadhaar par mujhe lagta hai ki "
    "aapko *ek gehri, vyaktigat Vedic consultation* ki zaroorat hai.\n\n"
    "✨ *Premium Consultation mein milega:*\n"
    "• Poori Janam Kundli (Lagna, Rashi, Nakshatra)\n"
    "• Dasha-Antardasha vishleshan\n"
    "• Gochara (current planetary transits)\n"
    "• 5 jeevan-kshetron mein upay (remedies)\n"
    "• Compatibility report (rishte ke liye)\n\n"
    "📲 Abhi WhatsApp par sampark karein aur apna slot book karein:"
)


# ---------------------------------------------------------------------------
# Entry: user lands in waiting_pitch state
# ---------------------------------------------------------------------------


@router.message(States.waiting_pitch)
async def show_pitch(msg: Message, state: FSMContext) -> None:
    profile = await get_profile(msg.from_user.id)
    name = profile.name if profile and profile.name else "Aap"

    personalised = (
        f"🙏 *{name} Ji*, aapka intezaar khatam hua!\n\n" + PITCH_MSG
    )
    await msg.answer(personalised, reply_markup=PITCH_KB)
    logger.info("User %s received pitch", msg.from_user.id)


@router.callback_query(F.data == "restart")
async def restart(cb: CallbackQuery, state: FSMContext) -> None:
    """Allow the user to restart the flow from any state."""
    await cb.answer()
    await state.clear()
    await cb.message.answer(
        "🔄 Nayi shuruat! /start likhein ya button dabayein."
    )
    logger.info("User %s restarted the flow", cb.from_user.id)
