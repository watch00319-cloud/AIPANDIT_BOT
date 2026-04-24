from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States

router = Router()

PITCH_MAIN = """🌟 Decode Your Future — Premium Astrology Bot Flow 🌟

🎯 99% Accurate Report Guarantee
💯 Not satisfied? 100% Money Back Guarantee

━━━━━━━━━━━━━━━━━━━━━━

🔮 MAIN MENU

User ko ye options dikhayein:
A) Vedic Basic — ₹499
B) Vedic Premium — ₹1100
C) Numerology Basic — ₹399
D) Numerology Premium — ₹1100

━━━━━━━━━━━━━━━━━━━━━━"""

SERVICE_A = """🅰️ VEDIC BASIC (₹499)

Features:

* Basic Kundali Analysis
* Personality + Life Overview
* Present Situation (Dasha + Transit)
* Future Prediction (2–5 years)
* 2 Questions Answer
* Basic Remedies
* Delivery: 24–48 hrs
* Accuracy: 95%

👉 Button: Buy Basic

⚡ UPSSELL trigger karein:

"🔥 Upgrade Suggestion:
Premium lene par aapko deep analysis + remedies + 99% accuracy milegi

👉 Sirf ₹600 extra me upgrade karein

Upgrade to Premium / Continue with Basic"

━━━━━━━━━━━━━━━━━━━━━━"""

SERVICE_B = """🅱️ VEDIC PREMIUM (₹1100)

Features:

* Complete Detailed Kundali
* All D-Charts (D1, D9, D10 etc.)
* Personalized Mantra & Remedies
* Dosha Detection (Mangal, Kaal Sarp, Pitru)
* Raj Yog / Dhan Yog
* Career + Marriage + Finance Deep Analysis
* Future Timeline (5–10 years)
* Premium Colored PDF

🎯 Accuracy: 99%
⚡ Delivery: SAME DAY (Priority)

👉 Button: Buy Premium

━━━━━━━━━━━━━━━━━━━━━━"""

SERVICE_C = """🅲 NUMEROLOGY BASIC (₹399)

Features:

* Mulank & Bhagyank
* Personality Overview
* Career Direction
* Basic Future Insights
* Delivery: 24–48 hrs
* Accuracy: 95%

👉 Button: Buy Basic

━━━━━━━━━━━━━━━━━━━━━━"""

SERVICE_D = """🅳 NUMEROLOGY PREMIUM (₹1100)

Features:

* Complete Chaldean Numerology
* Love Compatibility
* Career & Money Timeline
* Lucky Numbers, Colors, Days
* Name Correction Suggestion
* Business Name Analysis

🎯 Accuracy: 99%
⚡ Delivery: SAME DAY (Priority)

👉 Button: Buy Premium

━━━━━━━━━━━━━━━━━━━━━━"""

def _services_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🅰️ Vedic Basic — ₹499", callback_data="svc_a")],
            [InlineKeyboardButton(text="🅱️ Vedic Premium — ₹1100", callback_data="svc_b")],
            [InlineKeyboardButton(text="🅲 Numerology Basic — ₹399", callback_data="svc_c")],
            [InlineKeyboardButton(text="🅳 Numerology Premium — ₹1100", callback_data="svc_d")]
        ]
    )

def _back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="svc_back")],
        ]
    )

def _buy_keyboard(service: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Buy {service}", callback_data=f"buy_{service.lower().replace(' ', '_')}")],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="svc_back")],
        ]
    )

@router.message(States.pitch)
async def send_pitch(msg: Message, state: FSMContext):
    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "svc_a")
async def show_service_a(callback: CallbackQuery):
    await callback.message.answer(SERVICE_A, reply_markup=_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "svc_b")
async def show_service_b(callback: CallbackQuery):
    await callback.message.answer(SERVICE_B, reply_markup=_buy_keyboard("Premium"), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "svc_c")
async def show_service_c(callback: CallbackQuery):
    await callback.message.answer(SERVICE_C, reply_markup=_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "svc_d")
async def show_service_d(callback: CallbackQuery):
    await callback.message.answer(SERVICE_D, reply_markup=_buy_keyboard("Premium"), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "svc_back")
async def show_services_back(callback: CallbackQuery):
    await callback.message.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")
    await callback.answer()

# Upsell handlers (for Vedic Basic)
@router.callback_query(F.data.startswith("buy_svc_a"))
async def upsell_basic(callback: CallbackQuery, state: FSMContext):
    upsell_text = """🔥 Upgrade Suggestion:
Premium lene par aapko deep analysis + remedies + 99% accuracy milegi

👉 Sirf ₹600 extra me upgrade karein

Upgrade to Premium / Continue with Basic"""
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Upgrade to Premium", callback_data="upsell_premium")],
        [InlineKeyboardButton(text="Continue with Basic", callback_data="buy_basic")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="svc_a")]
    ])
    await callback.message.answer(upsell_text, reply_markup=markup, parse_mode="Markdown")
    await callback.answer()
    await state.set_state(States.upsell)

# Placeholder for buy - will trigger payment
@router.callback_query(F.data.startswith("buy"))
async def trigger_buy(callback: CallbackQuery):
    await callback.message.answer("💳 Payment Flow Triggered - See payment handler")
    await callback.answer()

@router.message(Command("services"))
async def services_cmd(msg: Message):
    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")

