import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States

router = Router()
logger = logging.getLogger(__name__)


SUBSCRIPTION_INFO = (
    "🌟 *Premium Subscription Plans* 🌟\n\n"
    "Hamare subscription plans se aap regular astrology guidance pa sakte hain:\n\n"
    "┌─────────────────────────────┐\n"
    "*📅 MONTHLY PLAN*\n"
    "└─────────────────────────────┘\n"
    "✅ Monthly Kundali Update\n"
    "✅ Weekly Gochara Alerts\n"
    "✅ Priority Support\n"
    "💰 *₹299 / month*\n\n"
    "┌─────────────────────────────┐\n"
    "*📆 YEARLY PLAN*\n"
    "└─────────────────────────────┘\n"
    "✅ Sab kuch Monthly mein +\n"
    "✅ 2 Free Consultations per year\n"
    "✅ Exclusive Remedies Guide\n"
    "💰 *₹2499 / year* _(save 30%)_\n\n"
    "📞 Subscribe karein: *+91 62839 41933*\n"
    "💳 Payment: UPI / PhonePe / GPay"
)


def _subscription_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Monthly — ₹299", callback_data="sub_monthly")],
            [InlineKeyboardButton(text="📆 Yearly — ₹2499", callback_data="sub_yearly")],
            [InlineKeyboardButton(text="📞 Subscribe Now", callback_data="sub_contact")],
        ]
    )


def _back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Plans", callback_data="sub_back")],
            [InlineKeyboardButton(text="📞 Subscribe Now", callback_data="sub_contact")],
        ]
    )


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

@router.message(Command("subscribe"))
async def subscribe_cmd(msg: Message, state: FSMContext):
    """Show subscription plans via /subscribe command."""
    logger.info("User %s requested subscription info", msg.from_user.id)
    await msg.answer(SUBSCRIPTION_INFO, reply_markup=_subscription_keyboard())


@router.callback_query(F.data == "sub_monthly")
async def show_monthly_plan(callback: CallbackQuery):
    await callback.message.answer(
        "📅 *MONTHLY SUBSCRIPTION — ₹299/month*\n\n"
        "Aapko milega:\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *Monthly Kundali Update* — har mahine fresh predictions\n"
        "✅ *Weekly Gochara Alerts* — planetary transit notifications\n"
        "✅ *Priority Support* — 24-hr response guarantee\n"
        "✅ *Monthly Remedy Tips* — personalized upay\n\n"
        "📞 Book now: *+91 62839 41933*\n"
        "💳 Payment: UPI / PhonePe / GPay",
        reply_markup=_back_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "sub_yearly")
async def show_yearly_plan(callback: CallbackQuery):
    await callback.message.answer(
        "📆 *YEARLY SUBSCRIPTION — ₹2499/year*\n\n"
        "Aapko milega:\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *Sab kuch Monthly mein* — poora monthly package\n"
        "✅ *2 Free Consultations* — personal 1-on-1 sessions\n"
        "✅ *Exclusive Remedies Guide* — PDF ebook\n"
        "✅ *Annual Forecast Report* — full year predictions\n"
        "✅ *Festival & Muhurat Alerts* — auspicious dates\n\n"
        "🎯 *Best Value — 30% savings!*\n\n"
        "📞 Book now: *+91 62839 41933*\n"
        "💳 Payment: UPI / PhonePe / GPay",
        reply_markup=_back_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "sub_back")
async def show_subscription_back(callback: CallbackQuery):
    await callback.message.answer(SUBSCRIPTION_INFO, reply_markup=_subscription_keyboard())
    await callback.answer()


@router.callback_query(F.data == "sub_contact")
async def subscription_contact(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📞 *Subscribe Karne Ke Liye*:\n\n"
        "Direct contact karein:\n\n"
        "📱 WhatsApp / Call: *+91 62839 41933*\n"
        "💳 Payment: UPI / PhonePe / GPay\n\n"
        "Payment ke baad aapko:\n"
        "✅ Subscription 24 hrs mein activate ho jayegi\n"
        "✅ Welcome kit WhatsApp pe milegi\n\n"
        "🙏 *Dhanyavad!* Nayi consultation ke liye /start likhein."
    )
    logger.info("User %s initiated subscription contact", callback.from_user.id)
    await callback.answer("Contact info bheja gaya 🙏")
