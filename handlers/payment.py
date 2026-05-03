import json
from pathlib import Path
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from states.main import States

router = Router()

DATA_FILE = Path(__file__).resolve().parents[1] / "user_data.json"
QR_FILE = Path(__file__).resolve().parents[1] / "upi_qr.png"
UPI_ID = "darksecrets0unveiled@okhdfcbank"
PHONE = "9888601933"

SERVICE_LABELS = {
    "vedic_basic": "Vedic Basic",
    "vedic_premium": "Vedic Premium",
    "numerology_basic": "Numerology Basic",
    "numerology_premium": "Numerology Premium",
}


def load_user_data() -> dict[str, dict[str, Any]]:
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_user_data(data: dict[str, dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def update_user_record(user_id: int, **fields: Any) -> dict[str, Any]:
    data = load_user_data()
    key = str(user_id)
    record = data.get(key, {})
    record.update(fields)
    data[key] = record
    save_user_data(data)
    return record


def get_user_record(user_id: int) -> dict[str, Any]:
    data = load_user_data()
    return data.get(str(user_id), {})


async def trigger_payment(msg: Message, service_key: str) -> None:
    service_name = SERVICE_LABELS[service_key]
    update_user_record(
        msg.from_user.id,
        selected_service=service_name,
        selected_service_key=service_key,
        payment_status="pending",
    )

    text = (
        "💳 PAYMENT FLOW\n\n"
        f"Selected Service: {service_name}\n"
        f"UPI ID: {UPI_ID}\n"
        f"WhatsApp Support: {PHONE}\n\n"
        "💳 Payment karein aur screenshot yahan bhejein\n"
        "⏳ Verification Time: 5–15 min"
    )
    await msg.answer(text)

    if QR_FILE.exists():
        await msg.answer_photo(FSInputFile(str(QR_FILE)))


@router.callback_query(F.data.startswith("buy_"))
async def buy_trigger(callback: CallbackQuery, state: FSMContext):
    service_key = callback.data.removeprefix("buy_")
    if service_key not in SERVICE_LABELS:
        await callback.answer("Unknown service", show_alert=True)
        return

    await state.set_state(States.payment_verification)
    await trigger_payment(callback.message, service_key)
    await callback.answer(f"Payment started for {SERVICE_LABELS[service_key]}")


@router.message(F.photo)
async def handle_screenshot(msg: Message, state: FSMContext):
    record = get_user_record(msg.from_user.id)
    if not record.get("selected_service"):
        await msg.answer("Pehle apni service select karke payment flow start karein.")
        return

    update_user_record(msg.from_user.id, payment_status="verified")
    await msg.answer(
        "✅ Screenshot received\n"
        "⏳ Verification ho raha hai (5–15 min)\n"
        "🙏 Please wait..."
    )
    await msg.answer(
        "✅ PAYMENT VERIFY\n\n"
        "Apni details bhejein:\n\n"
        "👤 Name\n"
        "📅 DOB\n"
        "⏰ Time\n"
        "📍 Place\n"
        "❓ 2 Questions"
    )
    await state.set_state(States.waiting_details)


@router.message(States.waiting_details)
async def handle_details(msg: Message, state: FSMContext):
    record = get_user_record(msg.from_user.id)
    service_name = record.get("selected_service", "Selected Service")
    is_premium = "Premium" in service_name
    delivery_line = (
        "⚡ Premium Report → SAME DAY Delivery"
        if is_premium
        else "📄 Basic Report → 24–48 hrs"
    )

    update_user_record(
        msg.from_user.id,
        payment_status="details_received",
        submitted_details=(msg.text or "").strip(),
    )

    await msg.answer(
        "🎉 FINAL MESSAGE\n\n"
        "Payment Verified ✅\n\n"
        f"{delivery_line}\n\n"
        "Report Telegram / WhatsApp par mil jayegi\n\n"
        "🙏 Thank you for trusting Decode Your Future"
    )
    await state.clear()
