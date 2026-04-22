from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.main import States

router = Router()

PITCH_TEXT = (
    "🌟 *Maharishi AstroGuru Ji Premium Reading* 🌟\n\n"
    "Aapke answers aur kundli snapshot ke base par next step:\n\n"
    "✅ Career, marriage, health, finance ka deep-dive\n"
    "✅ Personalized remedies & timing\n"
    "✅ 45-min voice/video session\n\n"
    "Price: ₹999 only (50% off first 100 users)\n\n"
    "Contact: *+91 62839 41933*\n"
    "Payment: UPI / PhonePe"
)

@router.message(States.pitch)
async def send_pitch(msg: Message, state: FSMContext):
    if (msg.text or "").strip().lower() != "pitch":
        await msg.answer("Pitch dekhne ke liye *PITCH* likhiye.")
        return

    await msg.answer(PITCH_TEXT)
    await state.clear()
    await msg.answer(
        "/start - Nayi consultation shuru karein\n"
        "/reset - Current session reset\n"
        "/help - Ye help text"
    )

