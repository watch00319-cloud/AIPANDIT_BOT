from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from states.main import States

router = Router()

PITCH_MAIN = """🌟 Decode Your Future — Premium Astrology Bot Flow 🌟

🎯 99% Accurate Report Guarantee
💯 Not satisfied? 100% Money Back Guarantee

━━━━━━━━━━━━━━━━━━━━━━

🔮 MAIN MENU

User ko ye options dikhayein:

🅰️ Vedic Basic — ₹499
🅱️ Vedic Premium — ₹1100
🅲 Numerology Basic — ₹399
🅳 Numerology Premium — ₹1100

👇 Apni service select karein

⚡ Premium highlight:
Fast Delivery + High Accuracy + Better Value
"""

SERVICE_A = """🅰️ VEDIC BASIC (₹499)

Features:

✅ Basic Kundali Analysis
✅ Personality + Life Overview
✅ Present Situation (Dasha + Transit)
✅ Future Prediction (2–5 years)
✅ 2 Questions Answer
✅ Basic Remedies
📄 Delivery: 24–48 hrs
🎯 Accuracy: 95%

👉 Button: Buy Basic
"""

SERVICE_A_UPSELL = """🔥 Upgrade Suggestion:

Premium lene par aapko milega:

✅ Deep Analysis
✅ Personalized Remedies
✅ Same Day Priority Delivery
✅ 99% Accuracy Report

👉 Sirf ₹600 extra me upgrade karein
"""

SERVICE_B = """🅱️ VEDIC PREMIUM (₹1100)

Features:

✅ Complete Detailed Kundali
✅ All D-Charts (D1, D9, D10 etc.)
✅ Personalized Mantra & Remedies
✅ Dosha Detection (Mangal, Kaal Sarp, Pitru)
✅ Raj Yog / Dhan Yog
✅ Career + Marriage + Finance Deep Analysis
✅ Future Timeline (5–10 years)
✅ Premium Colored PDF

🎯 Accuracy: 99%
⚡ Delivery: SAME DAY Priority

👉 Button: Buy Premium
"""

SERVICE_C = """🅲 NUMEROLOGY BASIC (₹399)

Features:

✅ Mulank & Bhagyank
✅ Personality Overview
✅ Career Direction
✅ Basic Future Insights

📄 Delivery: 24–48 hrs
🎯 Accuracy: 95%

👉 Button: Buy Basic

⚡ Optional Upsell:
Premium lene par same day report + advanced analysis milega
"""

SERVICE_D = """🅳 NUMEROLOGY PREMIUM (₹1100)

Features:

✅ Complete Chaldean Numerology
✅ Love Compatibility
✅ Career & Money Timeline
✅ Lucky Numbers, Colors, Days
✅ Name Correction Suggestion
✅ Business Name Analysis
✅ Premium PDF Report

🎯 Accuracy: 99%
⚡ Delivery: SAME DAY Priority

👉 Button: Buy Premium
"""


def _services_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🅰️ Vedic Basic — ₹499", callback_data="svc_a")],
            [InlineKeyboardButton(text="🅱️ Vedic Premium — ₹1100", callback_data="svc_b")],
            [InlineKeyboardButton(text="🅲 Numerology Basic — ₹399", callback_data="svc_c")],
            [InlineKeyboardButton(text="🅳 Numerology Premium — ₹1100", callback_data="svc_d")],
        ]
    )


def _back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="svc_back")],
        ]
    )


def _buy_keyboard(service_key: str, label: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=f"buy_{service_key}")],
            [InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="svc_back")],
        ]
    )


def _upsell_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Upgrade to Premium", callback_data="buy_vedic_premium")],
            [InlineKeyboardButton(text="Continue with Basic", callback_data="buy_vedic_basic")],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="svc_a")],
        ]
    )


async def send_services_menu(message: Message, state: FSMContext | None = None) -> None:
    if state is not None:
        await state.set_state(States.pitch)
    await message.answer(PITCH_MAIN, reply_markup=_services_keyboard())


@router.message(States.pitch)
async def send_pitch(msg: Message, state: FSMContext):
    await send_services_menu(msg, state)


@router.callback_query(F.data == "svc_a")
async def show_service_a(callback: CallbackQuery):
    await callback.message.answer(
        SERVICE_A,
        reply_markup=_buy_keyboard("vedic_basic_offer", "Buy Basic"),
    )
    await callback.answer()


@router.callback_query(F.data == "svc_b")
async def show_service_b(callback: CallbackQuery):
    await callback.message.answer(
        SERVICE_B,
        reply_markup=_buy_keyboard("vedic_premium", "Buy Premium"),
    )
    await callback.answer()


@router.callback_query(F.data == "svc_c")
async def show_service_c(callback: CallbackQuery):
    await callback.message.answer(
        SERVICE_C,
        reply_markup=_buy_keyboard("numerology_basic", "Buy Basic"),
    )
    await callback.answer()


@router.callback_query(F.data == "svc_d")
async def show_service_d(callback: CallbackQuery):
    await callback.message.answer(
        SERVICE_D,
        reply_markup=_buy_keyboard("numerology_premium", "Buy Premium"),
    )
    await callback.answer()


@router.callback_query(F.data == "svc_back")
async def show_services_back(callback: CallbackQuery):
    await callback.message.answer(PITCH_MAIN, reply_markup=_services_keyboard())
    await callback.answer()


@router.callback_query(F.data == "buy_vedic_basic_offer")
async def upsell_basic(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.upsell)
    await callback.message.answer(SERVICE_A_UPSELL, reply_markup=_upsell_keyboard())
    await callback.answer()


@router.message(Command("services"))
async def services_cmd(msg: Message, state: FSMContext):
    await send_services_menu(msg, state)
