from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import logging

from states.main import States

logger = logging.getLogger(__name__)
router = Router()

# Payment details — single source of truth
UPI_ID = "darksecrets0unveiled@okhdfcbank"
CONTACT_PHONE = "+91 9888601933"

# [All PITCH_MAIN, SERVICE_*, keyboards unchanged - omitted for brevity, same as original]

PITCH_MAIN = (
    "🌟 *Maharishi AstroGuru Ji — Premium Services* 🌟\n\n"
    "Aapka *FREE preview* complete hua ✅\n"
    "Ab aap in 4 paid services mein se koi bhi choose kar sakte hain:\n\n"
    "┌─────────────────────────────┐\n"
    "*🕉️ VEDIC KUNDALI SERVICES*\n"
    "└─────────────────────────────┘\n"
    "🅰️ *Vedic Basic* — ₹499\n"
    "🅱️ *Vedic Premium + Remedies* — ₹1100\n\n"
    "┌─────────────────────────────┐\n"
    "*🔢 NUMEROLOGY SERVICES*\n"
    "└─────────────────────────────┘\n"
    "🅲 *Numerology Basic* — ₹399\n"
    "🅳 *Numerology Premium* — ₹1100\n\n"
    "👇 *Niche button dabakar* details dekhein:"
)

SERVICE_A_VEDIC_BASIC = (
    "🅰️ *VEDIC KUNDALI — BASIC REPORT*\n"
    "💰 *Price: ₹499 only*\n\n"
    "📜 Aapko kya milega:\n"
    " [same as original]"
)  # Omitted long text for brevity, copy from original

# ... other SERVICE_*, _services_keyboard, _back_keyboard same as original

def _services_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🅰️ Vedic Basic — ₹499", callback_data="svc_a")],
            [InlineKeyboardButton(text="🅱️ Vedic Premium — ₹1100", callback_data="svc_b")],
            [InlineKeyboardButton(text="🅲 Numerology Basic — ₹399", callback_data="svc_c")],
            [InlineKeyboardButton(text="🅳 Numerology Premium — ₹1100", callback_data="svc_d")],
            [InlineKeyboardButton(text="📞 Book Now", callback_data="svc_book")],
        ]
    )

def _back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Services", callback_data="svc_back")],
            [InlineKeyboardButton(text="📞 Book This Service", callback_data="svc_book")],
        ]
    )

@router.message(States.pitch)
async def send_pitch(msg: Message, state: FSMContext):
    lower_text = (msg.text or "").strip().lower()
    logger.info(f"[{msg.from_user.id}] Pitch handler fired for text: '{msg.text}'")
    
    if len(lower_text) < 3 or 'pitch' not in lower_text:
        await msg.answer("Services dekhne ke liye *PITCH* likhiye (ya /services).")
        return

    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard())

# All callback_query handlers same

@router.callback_query(F.data == "svc_a")
async def show_service_a(callback: CallbackQuery):
    await callback.message.answer(SERVICE_A_VEDIC_BASIC, reply_markup=_back_keyboard())
    await callback.answer()

# [repeat for b,c,d, back, book - same as original]

@router.callback_query(F.data == "svc_b")
async def show_service_b(callback: CallbackQuery):
    await callback.message.answer(SERVICE_B_VEDIC_PREMIUM, reply_markup=_back_keyboard())
    await callback.answer()

@router.callback_query(F.data == "svc_c")
async def show_service_c(callback: CallbackQuery):
    await callback.message.answer(SERVICE_C_NUMEROLOGY_BASIC, reply_markup=_back_keyboard())
    await callback.answer()

@router.callback_query(F.data == "svc_d")
async def show_service_d(callback: CallbackQuery):
    await callback.message.answer(SERVICE_D_NUMEROLOGY_PREMIUM, reply_markup=_back_keyboard())
    await callback.answer()

@router.callback_query(F.data == "svc_back")
async def show_services_back(callback: CallbackQuery):
    await callback.message.answer(PITCH_MAIN, reply_markup=_services_keyboard())
    await callback.answer()

@router.callback_query(F.data == "svc_book")
async def book_service(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📞 *Service Book Karne Ka Process*\n"
        " [same as original]"
    )
    await state.clear()
    await callback.answer("Payment details bheja gaya 🙏")

@router.message(Command("services"))
async def services_cmd(msg: Message):
    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard())

