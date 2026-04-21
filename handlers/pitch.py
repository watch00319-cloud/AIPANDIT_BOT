from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from states import States

router = Router()

PITCH_TEXT = (
    "🌟 *Maharishi AstroGuru Ji Premium Reading* 🌟\n\n"
    "Aapke answers aur kundli snapshot ke base par next step:\n\n"
    "✅ Career, marriage, health, finance ka deep-dive\n"
    "✅ Personal timing windows (short-term + long-term)\n"
    "✅ Practical remedies and action plan\n"
    "✅ One-to-one guidance support\n\n"
    "💯 *100% Money-Back Guarantee* agar aapko value na mile.\n\n"
    "📞 Direct Contact: *6283941933*\n"
    "WhatsApp: https://wa.me/916283941933\n\n"
    "*Disclaimer:* Astrology guidance is for spiritual/self-reflection use."
)


@router.message(States.pitch)
async def send_pitch(msg: Message, state: FSMContext):
    if (msg.text or "").strip().lower() != "pitch":
        await msg.answer("Aage badhne ke liye *PITCH* likhiye.")
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📱 WhatsApp Now", url="https://wa.me/916283941933")],
            [InlineKeyboardButton(text="🌙 Daily Gochara", callback_data="gochara")],
            [InlineKeyboardButton(text="💑 Compatibility Teaser", callback_data="compat")],
        ]
    )

    await msg.answer(PITCH_TEXT, reply_markup=kb)
