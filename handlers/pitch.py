from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States

router = Router()


# ---------------------------------------------------------------------------
# Service catalog — 4 paid packages
# ---------------------------------------------------------------------------

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
    "━━━━━━━━━━━━━━━━━━━━\n"
    "✅ *Sampuran Kundali Analysis* — aapki janm kundali ka detailed study\n"
    "✅ *Colored PDF Report* — professional design, print-ready\n"
    "✅ *Past Life Analysis* — purane karma + sanskaar\n"
    "✅ *Present Situation* — abhi kya chal raha hai (dasha + transit)\n"
    "✅ *Future Prediction* — agle 2-5 saal ki roadmap\n"
    "✅ *2 Prashn ka Uttar* — aap koi bhi 2 questions pooch sakte hain\n"
    "✅ *Samadhan Vidhi* — un 2 problems ko solve karne ka tareeka\n\n"
    "🎯 *Accuracy: 95%*\n"
    "📧 Delivery: PDF via Email/WhatsApp (24-48 hrs)\n\n"
    "📞 Book now: *+91 62839 41933*\n"
    "💳 Payment: UPI / PhonePe / GPay"
)


SERVICE_B_VEDIC_PREMIUM = (
    "🅱️ *VEDIC KUNDALI — PREMIUM + REMEDIES*\n"
    "💰 *Price: ₹1100 only*\n\n"
    "📜 Basic report ke sab kuch + PLUS:\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "✅ *Complete Colored PDF Report* (extended version)\n"
    "✅ *Mantra & Upay* — aapki specific problems ke liye personalized mantras\n"
    "✅ *Practical Remedies* — daily/weekly routine aur ritual guide\n"
    "✅ *D-Charts Deep Analysis*:\n"
    "   • D-1 (Rashi Chart) — overall life\n"
    "   • D-9 (Navamsa) — marriage + dharma\n"
    "   • D-10 (Dashamsha) — career + success\n"
    "   • D-7 (Saptamsha) — children\n"
    "✅ *Yoga Analysis* — Raj Yog, Dhan Yog, etc.\n"
    "✅ *Dosha Detection* — Mangal, Kaalsarp, Pitru Dosha + remedies\n"
    "✅ *Nakshatra Deep Dive* — your birth star meaning\n"
    "✅ *Sampuran Kundali Jankari* — har pehlu detail mein\n\n"
    "🎯 *Accuracy: 98%*\n"
    "📧 Delivery: Premium PDF (48-72 hrs)\n\n"
    "📞 Book now: *+91 62839 41933*\n"
    "💳 Payment: UPI / PhonePe / GPay"
)


SERVICE_C_NUMEROLOGY_BASIC = (
    "🅲 *NUMEROLOGY — BASIC REPORT*\n"
    "💰 *Price: ₹399 only*\n\n"
    "📜 *Itihaas (History)*:\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "_Ye technique *2000+ saal* purani hai — _\n"
    "_Ancient *Babylonian civilization* ne develop ki thi._\n"
    "_Ye numbers ki *urja (energy)* aur *vibration* par adharit hai,_\n"
    "_na ki varnmala (alphabet) par._\n\n"
    "⚠️ *Galat Dhaarna*:\n"
    "_Aaj bahut log apni DOB ka kul jod nikalke mulank/bhagyank_\n"
    "_bana lete hain — LEKIN YE SAHI NAHI HAI._\n\n"
    "✅ *Sahi Method*:\n"
    "_Hum *Chaldean Chart* use karte hain (original Babylonian system)._\n"
    "_Uske aadhaar par aapka *asli Mulank + Bhagyank* niklega._\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "📦 Aapko kya milega:\n"
    "✅ *Sampuran Analysis* — Chaldean system se\n"
    "✅ *Asli Mulank (Root Number)* — accurate calculation\n"
    "✅ *Asli Bhagyank (Destiny Number)*\n"
    "✅ *Colored PDF Report*\n"
    "✅ *Strong Analysis* — number energies decoded\n"
    "✅ *DOB-based predictions*\n\n"
    "📧 Delivery: PDF via Email/WhatsApp (24 hrs)\n\n"
    "📞 Book now: *+91 62839 41933*\n"
    "💳 Payment: UPI / PhonePe / GPay"
)


SERVICE_D_NUMEROLOGY_PREMIUM = (
    "🅳 *NUMEROLOGY — PREMIUM (UPGRADE)*\n"
    "💰 *Price: ₹1100 only*\n\n"
    "📜 *Sampuran Ank Jyotish* (Chaldean System)\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "✅ *Mulank (Root Number)* — inner self\n"
    "✅ *Bhagyank (Destiny Number)* — life purpose\n"
    "✅ *Personality Analysis* — complete character profile\n"
    "✅ *Love Compatibility* — partner match analysis\n"
    "✅ *Career & Money* — best career paths + earning years\n"
    "✅ *Future Prediction* — next 5 years timeline\n"
    "✅ *Lucky Numbers* — personal lucky numbers\n"
    "✅ *Lucky Colors & Days*\n"
    "✅ *Name Numerology* — should you change your name?\n"
    "✅ *Business Name Check* — lucky or unlucky\n\n"
    "🎯 *Accuracy: 99%*\n"
    "📜 *Chaldean system* — ancient Babylonian technique\n"
    "📧 Delivery: Premium Colored PDF (48 hrs)\n\n"
    "📞 Book now: *+91 62839 41933*\n"
    "💳 Payment: UPI / PhonePe / GPay"
)


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


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------
@router.message(States.pitch)
async def send_pitch(msg: Message, state: FSMContext):
    if (msg.text or "").strip().lower() != "pitch":
        await msg.answer("Pitch dekhne ke liye *PITCH* likhiye.")
        return

    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard())


@router.callback_query(F.data == "svc_a")
async def show_service_a(callback: CallbackQuery):
    await callback.message.answer(SERVICE_A_VEDIC_BASIC, reply_markup=_back_keyboard())
    await callback.answer()


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
        "📞 *Service Book Karne Ke Liye*:\n\n"
        "Direct contact karein:\n\n"
        "📱 WhatsApp / Call: *+91 62839 41933*\n"
        "💳 Payment: UPI / PhonePe / GPay\n\n"
        "Ek baar payment confirm ho jaye, toh aapko:\n"
        "✅ Detailed PDF report 24-72 hrs mein milegi\n"
        "✅ Email / WhatsApp pe delivery\n\n"
        "🙏 *Dhanyavad!* Nayi consultation ke liye /start likhein."
    )
    await state.clear()
    await callback.answer("Contact info bheja gaya 🙏")


@router.message(Command("services"))
async def services_cmd(msg: Message):
    """Allow user to see services anytime via /services command."""
    await msg.answer(PITCH_MAIN, reply_markup=_services_keyboard())
