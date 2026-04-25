from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States

router = Router()

# ---------------------------------------------------------------------------
# Payment details (shown in Buy Now flow)
# ---------------------------------------------------------------------------

UPI_ID = "darksecrets0unveiled@okhdfcbank"
WHATSAPP_LINK = "https://wa.me/919888601933"

# ---------------------------------------------------------------------------
# Main services catalog
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

# ---------------------------------------------------------------------------
# Detailed service descriptions
# ---------------------------------------------------------------------------

SERVICE_A = (
    "🕉 *VEDIC KUNDALI BASIC — ₹499*\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "📋 *Kya milega aapko:*\n\n"
    "✅ Basic Kundali Analysis\n"
    "✅ Personality + Life Overview\n"
    "✅ Present Situation (Dasha + Transit)\n"
    "✅ Future Prediction (2–5 years)\n"
    "✅ 2 Questions Answer\n"
    "✅ Basic Remedies\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "⏱ *Delivery:* 24–48 Hours\n"
    "🎯 *Accuracy:* 95% Guaranteed\n"
    "💰 *Price:* ₹499 Only\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "⭐ *Upgrade Suggestion:*\n"
    "Sirf ₹601 extra mein *Vedic Premium (₹1100)* lein aur paayen:\n"
    "• All D-Charts (D1, D9, D10 etc.)\n"
    "• Dosha Detection (Mangal, Kaal Sarp, Pitru)\n"
    "• Raj Yog / Dhan Yog Analysis\n"
    "• Career + Marriage + Finance Deep Dive\n"
    "• Future Timeline 5–10 years\n"
    "• Premium Colored PDF\n"
    "• SAME DAY Priority Delivery\n"
    "• 99% Accuracy\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "👇 *Abhi order karein ya Premium upgrade karein:*"
)

SERVICE_B = (
    "🕉 *VEDIC KUNDALI PREMIUM — ₹1100*\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "📋 *Kya milega aapko:*\n\n"
    "✅ Complete Detailed Kundali\n"
    "✅ All D-Charts (D1, D9, D10 etc.)\n"
    "✅ Personalized Mantra & Remedies\n"
    "✅ Dosha Detection (Mangal, Kaal Sarp, Pitru)\n"
    "✅ Raj Yog / Dhan Yog Analysis\n"
    "✅ Career + Marriage + Finance Deep Analysis\n"
    "✅ Future Timeline (5–10 years)\n"
    "✅ Premium Colored PDF Report\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "⚡ *Delivery:* SAME DAY (Priority)\n"
    "🎯 *Accuracy:* 99% Guaranteed\n"
    "💰 *Price:* ₹1100 Only\n"
    "💯 *Not Satisfied? 100% Money Back*\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "👇 *Abhi order karein:*"
)

SERVICE_C = (
    "🔢 *NUMEROLOGY BASIC — ₹399*\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "📋 *Kya milega aapko:*\n\n"
    "✅ Mulank & Bhagyank Analysis\n"
    "✅ Personality Overview\n"
    "✅ Career Direction\n"
    "✅ Basic Future Insights\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "⏱ *Delivery:* 24–48 Hours\n"
    "🎯 *Accuracy:* 95% Guaranteed\n"
    "💰 *Price:* ₹399 Only\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "⭐ *Upgrade Suggestion:*\n"
    "Sirf ₹701 extra mein *Numerology Premium (₹1100)* lein aur paayen:\n"
    "• Complete Chaldean Numerology\n"
    "• Love Compatibility Analysis\n"
    "• Career & Money Timeline\n"
    "• Lucky Numbers, Colors & Days\n"
    "• Name Correction Suggestion\n"
    "• Business Name Analysis\n"
    "• SAME DAY Priority Delivery\n"
    "• 99% Accuracy\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "👇 *Abhi order karein ya Premium upgrade karein:*"
)

SERVICE_D = (
    "🔢 *NUMEROLOGY PREMIUM — ₹1100*\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "📋 *Kya milega aapko:*\n\n"
    "✅ Complete Chaldean Numerology\n"
    "✅ Love Compatibility Analysis\n"
    "✅ Career & Money Timeline\n"
    "✅ Lucky Numbers, Colors & Days\n"
    "✅ Name Correction Suggestion\n"
    "✅ Business Name Analysis\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "⚡ *Delivery:* SAME DAY (Priority)\n"
    "🎯 *Accuracy:* 99% Guaranteed\n"
    "💰 *Price:* ₹1100 Only\n"
    "💯 *Not Satisfied? 100% Money Back*\n\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "👇 *Abhi order karein:*"
)

# ---------------------------------------------------------------------------
# Payment instruction message (sent on Buy Now)
# ---------------------------------------------------------------------------

def _payment_text(service_name: str, price: str) -> str:
    return (
        f"💳 *Payment — {service_name}*\n\n"
        f"💰 *Amount:* {price}\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏦 *UPI ID:* `{UPI_ID}`\n\n"
        "📲 *Steps:*\n"
        "1️⃣ Apne UPI app mein UPI ID copy karein\n"
        "2️⃣ Payment karein\n"
        "3️⃣ Screenshot yahan bhejein ✅\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "❓ *Help chahiye?*\n"
        f"[WhatsApp par contact karein]({WHATSAPP_LINK})\n\n"
        "⚡ Payment confirm hote hi aapka report process shuru ho jaayega!"
    )

# ---------------------------------------------------------------------------
# Keyboards
# ---------------------------------------------------------------------------

def _services_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🅐 Vedic Basic — ₹499", callback_data="svc_a")],
            [InlineKeyboardButton(text="🅑 Vedic Premium — ₹1100", callback_data="svc_b")],
            [InlineKeyboardButton(text="🅒 Numerology Basic — ₹399", callback_data="svc_c")],
            [InlineKeyboardButton(text="🅓 Numerology Premium — ₹1100", callback_data="svc_d")],
        ]
    )

def _detail_keyboard_basic(buy_cb: str, upgrade_cb: str) -> InlineKeyboardMarkup:
    """Keyboard for Basic services — Buy Now + Upgrade to Premium + Back."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Buy Now", callback_data=buy_cb)],
            [InlineKeyboardButton(text="⭐ Upgrade to Premium", callback_data=upgrade_cb)],
            [InlineKeyboardButton(text="⬅️ Back to Services", callback_data="svc_back")],
        ]
    )

def _detail_keyboard_premium(buy_cb: str) -> InlineKeyboardMarkup:
    """Keyboard for Premium services — Buy Now + Back."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Buy Now", callback_data=buy_cb)],
            [InlineKeyboardButton(text="⬅️ Back to Services", callback_data="svc_back")],
        ]
    )

def _back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Services", callback_data="svc_back")],
        ]
    )

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

@router.message(States.pitch)
async def send_pitch(msg: Message, state: FSMContext):
    if (msg.text or "").strip().lower() != "pitch":
        await msg.answer("Pitch dekhne ke liye *PITCH* likhiye.")
        return

    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")

# --- Service detail pages ---

@router.callback_query(F.data == "svc_a")
async def show_service_a(callback: CallbackQuery):
    await callback.message.answer(
        SERVICE_A,
        reply_markup=_detail_keyboard_basic("buy_a", "svc_b"),
        parse_mode="Markdown",
    )
    await callback.answer()

@router.callback_query(F.data == "svc_b")
async def show_service_b(callback: CallbackQuery):
    await callback.message.answer(
        SERVICE_B,
        reply_markup=_detail_keyboard_premium("buy_b"),
        parse_mode="Markdown",
    )
    await callback.answer()

@router.callback_query(F.data == "svc_c")
async def show_service_c(callback: CallbackQuery):
    await callback.message.answer(
        SERVICE_C,
        reply_markup=_detail_keyboard_basic("buy_c", "svc_d"),
        parse_mode="Markdown",
    )
    await callback.answer()

@router.callback_query(F.data == "svc_d")
async def show_service_d(callback: CallbackQuery):
    await callback.message.answer(
        SERVICE_D,
        reply_markup=_detail_keyboard_premium("buy_d"),
        parse_mode="Markdown",
    )
    await callback.answer()

# --- Buy Now handlers ---

@router.callback_query(F.data == "buy_a")
async def buy_service_a(callback: CallbackQuery):
    await callback.message.answer(
        _payment_text("Vedic Kundali Basic", "₹499"),
        reply_markup=_back_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
    await callback.answer()

@router.callback_query(F.data == "buy_b")
async def buy_service_b(callback: CallbackQuery):
    await callback.message.answer(
        _payment_text("Vedic Kundali Premium", "₹1100"),
        reply_markup=_back_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
    await callback.answer()

@router.callback_query(F.data == "buy_c")
async def buy_service_c(callback: CallbackQuery):
    await callback.message.answer(
        _payment_text("Numerology Basic", "₹399"),
        reply_markup=_back_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
    await callback.answer()

@router.callback_query(F.data == "buy_d")
async def buy_service_d(callback: CallbackQuery):
    await callback.message.answer(
        _payment_text("Numerology Premium", "₹1100"),
        reply_markup=_back_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
    await callback.answer()

# --- Back to main services menu ---

@router.callback_query(F.data == "svc_back")
async def show_services_back(callback: CallbackQuery):
    await callback.message.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.message(Command("services"))
async def services_cmd(msg: Message):
    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard(), parse_mode="Markdown")
