from aiogram import Router
from aiogram.types import Message, FSInputFile
import time

router = Router()

# user data memory (simple)
user_data = {}

UPI_ID = "darksecrets0unveiled@okhdfcbank"
MOBILE = "+91 6283941933"
QR_PATH = "qr.png"   # 👉 same folder me QR image daal dena

FREE_TIME = 120  # 2 minute

@router.message()
async def handle_question(msg: Message):
    user_id = msg.from_user.id

    now = time.time()

    if user_id not in user_data:
        user_data[user_id] = now

    elapsed = now - user_data[user_id]

    # FREE TIME
    if elapsed <= FREE_TIME:
        await msg.answer(
            "🔮 Aapka jawab:\n\n"
            "👉 (Yaha tum apna AI answer laga sakte ho)\n\n"
            "⏳ Free time chal raha hai..."
        )
        return

    # AFTER FREE TIME → PAID
    await msg.answer(
        "⛔ Aapka free time khatam ho chuka hai.\n\n"
        "💰 Paid consultation ke liye payment karein:\n\n"
        f"📱 Mobile: {MOBILE}\n"
        f"💳 UPI: {UPI_ID}"
    )

    # QR SEND
    try:
        photo = FSInputFile(QR_PATH)
        await msg.answer_photo(photo, caption="📸 Scan karke payment karein")
    except:
        await msg.answer("⚠️ QR load nahi hua, manually UPI use karein.")
