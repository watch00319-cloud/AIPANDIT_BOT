from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States

router = Router()

# --------------------------------------------------------------------------- 
# NEW Premium Services Catalog
# ---------------------------------------------------------------------------

PITCH_MAIN = (
    "🔮 *Astro Insight Premium Services*\n\n"
    "✨ *99% Accurate Personalized Report Guarantee*\n"
    "💯 *Not Satisfied? Get 100% Money Back — No Questions Asked*\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "आपका *FREE Preview* सफलतापूर्वक पूरा हो चुका है ✅\n"
    "अब आप अपनी जरूरत के अनुसार हमारी Premium Services चुन सकते हैं:\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "🕉 *VEDIC KUNDALI ANALYSIS*\n\n"
    "🅐 *Basic Report* — ₹499\n"
    "• Complete Kundali Overview\n"
    "• Career & Relationship Insights\n\n"
    "🅑 *Premium + Remedies* — ₹1100\n"
    "• Detailed Life Analysis\n"
    "• Accurate Predictions\n"
    "• Personalized Remedies (Upay)\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "🔢 *NUMEROLOGY ANALYSIS*\n\n"
    "🅒 *Basic Report* — ₹399\n"
    "• Name & DOB Analysis\n"
    "• Personality & Luck Insights\n\n"
    "🅓 *Premium Report* — ₹1100\n"
    "• Advanced Numerology Reading\n"
    "• Career, Finance & Relationship Guidance\n"
    "• Powerful Remedies\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "👇 *Service select karne ke liye niche button par click karein*"
)

def _services_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🅐 Vedic Basic — ₹499", callback_data="svc_a")],
            [InlineKeyboardButton(text="🅑 Vedic Premium — ₹1100", callback_data="svc_b")],
            [InlineKeyboardButton(text="🅒 Numerology Basic — ₹399", callback_data="svc_c")],
            [InlineKeyboardButton(text="🅓 Numerology Premium — ₹1100", callback_data="svc_d")],
        ]
    )

def _back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Services", callback_data="svc_back")],
        ]
    )

@router.message(States.pitch)
async def send_pitch(msg: Message, state: FSMContext):
    if (msg.text or "").strip().lower() != "pitch":
        await msg.answer("Pitch dekhne ke liye *PITCH* likhiye.")
        return

    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "svc_a")
async def show_service_a(callback: CallbackQuery):
    await callback.message.answer("🅐 *VEDIC KUNDALI BASIC* details...", reply_markup=_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "svc_b")
async def show_service_b(callback: CallbackQuery):
    await callback.message.answer("🅑 *VEDIC KUNDALI PREMIUM* details...", reply_markup=_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "svc_c")
async def show_service_c(callback: CallbackQuery):
    await callback.message.answer("🅒 *NUMEROLOGY BASIC* details...", reply_markup=_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "svc_d")
async def show_service_d(callback: CallbackQuery):
    await callback.message.answer("🅓 *NUMEROLOGY PREMIUM* details...", reply_markup=_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "svc_back")
async def show_services_back(callback: CallbackQuery):
    await callback.message.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.message(Command("services"))
async def services_cmd(msg: Message):
    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")
