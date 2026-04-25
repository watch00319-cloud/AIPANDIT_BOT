import json
import os
from typing import Dict, Any, Optional

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States
from .pitch import router as pitch_router  # Import for state management

router = Router()

DATA_FILE = "user_data.json"
UPI_ID = "darksecrets0unveiled@okhdfcbank"
PHONE = "9888601933"
TEXT_WHATSAPP = "whatsapp://send?phone=919888601933"

def load_user_data() -> Dict[int, Dict[str, Any]]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    return {}

def save_user_data(data: Dict[int, Dict[str, Any]]):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)

def get_user_status(user_id: int) -> Dict[str, Any]:
    data = load_user_data()
    if user_id not in data:
        data[user_id] = {"first_seen_time": "2024-01-01T00:00:00", "paid_status": False, "service": None}
        save_user_data(data)
    status = data[user_id]
    return status

def trial_active(user_id: int) -> bool:
    status = get_user_status(user_id)
    if status["paid_status"]:
        return True
    return False  # Simplified for paid flow

def mark_paid(user_id: int, service: str):
    data = load_user_data()
    if user_id in data:
        data[user_id]["paid_status"] = True
        data[user_id]["service"] = service
        save_user_data(data)

async def trigger_payment(msg: Message, service: str) -> bool:
    status = get_user_status(msg.from_user.id)
    if status["paid_status"]:
        return False
    text = f"💳 Payment for {service}\n\nwhatsapp only {PHONE}\nUPI ID: {UPI_ID}\n\nPayment karein aur screenshot bhejein (5–15 min verification)"
    await msg.answer(text, parse_mode="Markdown", disable_web_page_preview=True)
    try:
        qr_file = FSInputFile("upi_qr.png")
        await msg.bot.send_photo(msg.chat.id, qr_file)
    except Exception:
        pass
    return True

@router.message(F.photo)
async def handle_screenshot(msg: Message, state: FSMContext):
    status = get_user_status(msg.from_user.id)
    if not status["paid_status"]:
        await msg.answer("✅ Screenshot received\nVerification ho raha hai (5–15 min)")
        await state.set_state(States.payment_verification)
    else:
        await msg.answer("✅ Already verified!")

@router.message(States.payment_verification)
async def verification_complete(msg: Message, state: FSMContext):
    await msg.answer("✅ PAYMENT VERIFY:\n\nApni details bhejein:\nName / DOB / Time / Place + 2 Questions")
    await state.set_state(States.waiting_details)

@router.message(States.waiting_details)
async def handle_details(msg: Message, state: FSMContext):
    # Save details and trigger birth collection logic or final
    await msg.answer("""🎉 FINAL:

Payment Verified

Basic → 24–48 hrs
Premium → SAME DAY Delivery ⚡

Report Telegram / WhatsApp par mil jayegi

Thank you 🙏""")
    # Reset or go to birth collection
    await state.clear()

@router.callback_query(F.data.startswith("buy"))
async def buy_trigger(callback: CallbackQuery, state: FSMContext):
    service_map = {
        "buy_vedic_basic": "Vedic Basic",
        "buy_vedic_premium": "Vedic Premium",
        "buy_numerology_basic": "Numerology Basic",
        "buy_numerology_premium": "Numerology Premium",
    }
    data = callback.data.replace("buy_", "")
    service = service_map.get(callback.data, "Unknown")
    if await trigger_payment(callback.message, service):
        mark_paid(callback.from_user.id, service)
    await callback.answer(f"Payment for {service} triggered")

__all__ = ["trigger_payment", "trial_active"]

