import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

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
        data[user_id] = {"first_seen_time": datetime.utcnow().isoformat(), "paid_status": False}
        save_user_data(data)
    status = data[user_id]
    if isinstance(status.get("first_seen_time"), str):
        status["first_seen_time"] = datetime.fromisoformat(status["first_seen_time"])
    return status

def trial_active(user_id: int) -> bool:
    status = get_user_status(user_id)
    if status["paid_status"]:
        return True
    first_seen = status["first_seen_time"]
    return (datetime.utcnow() - first_seen) < timedelta(minutes=2)

def mark_paid(user_id: int):
    data = load_user_data()
    if user_id in data:
        data[user_id]["paid_status"] = True
        save_user_data(data)

async def trigger_payment(msg: Message) -> bool:
    status = get_user_status(msg.from_user.id)
    if status["paid_status"]:
        return False
    if trial_active(msg.from_user.id):
        return False
    text = (
        "💳 Payment Required\n"
        "Your free trial is over\n\n"
        f"UPI ID: {UPI_ID}\n"
        f"Phone: 9888601933\n"
        f"[WhatsApp]({TEXT_WHATSAPP})\n\n"
        "To continue, use paid service\n"
        "Send payment screenshot after payment"
    )
    await msg.answer(text, parse_mode="Markdown", disable_web_page_preview=True)
    try:
        qr_file = FSInputFile("upi_qr.png")
        await msg.bot.send_photo(msg.chat.id, qr_file)
    except Exception:
        pass  # Silent if no QR
    return True

@router.message(F.photo)
async def handle_screenshot(msg: Message):
    status = get_user_status(msg.from_user.id)
    if not status["paid_status"]:
        mark_paid(msg.from_user.id)
        await msg.answer("✅ Payment received\n🔓 Full access unlocked")
    else:
        await msg.answer("✅ Already unlocked!")

__all__ = ["trigger_payment", "trial_active"]
