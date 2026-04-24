from aiogram import Router
<<<<<<< HEAD
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.main import States
from utils.db import save_answers
from .payment import trigger_payment
=======
from aiogram.types import Message, FSInputFile
import time
>>>>>>> 2fd36d67402011f51df74a20dadb87967d0d8394

router = Router()

# user data memory (simple)
user_data = {}

<<<<<<< HEAD
@router.message(States.question_1)
async def q1(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q1=(msg.text or "").strip())
    await msg.answer("Q2/5: Vivah/relationship ko lekar aap kya guidance chahte hain?")
    await state.set_state(States.question_2)
=======
UPI_ID = "darksecrets0unveiled@okhdfcbank"
MOBILE = "+91 6283941933"
QR_PATH = "qr.png"   # 👉 same folder me QR image daal dena
>>>>>>> 2fd36d67402011f51df74a20dadb87967d0d8394

FREE_TIME = 120  # 2 minute

<<<<<<< HEAD
@router.message(States.question_2)
async def q2(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q2=(msg.text or "").strip())
    await msg.answer("Q3/5: Health ya stress ke kis area par clarity chahiye?")
    await state.set_state(States.question_3)
=======
@router.message()
async def handle_question(msg: Message):
    user_id = msg.from_user.id
>>>>>>> 2fd36d67402011f51df74a20dadb87967d0d8394

    now = time.time()

<<<<<<< HEAD
@router.message(States.question_3)
async def q3(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q3=(msg.text or "").strip())
    await msg.answer("Q4/5: Finance/wealth growth mein abhi sabse bada concern kya hai?")
    await state.set_state(States.question_4)
=======
    if user_id not in user_data:
        user_data[user_id] = now
>>>>>>> 2fd36d67402011f51df74a20dadb87967d0d8394

    elapsed = now - user_data[user_id]

<<<<<<< HEAD
@router.message(States.question_4)
async def q4(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q4=(msg.text or "").strip())
    await msg.answer("Q5/5: Koi specific prashna jo aap turant solve karna chahte hain?")
    await state.set_state(States.question_5)
=======
    # FREE TIME
    if elapsed <= FREE_TIME:
        await msg.answer(
            "🔮 Aapka jawab:\n\n"
            "👉 (Yaha tum apna AI answer laga sakte ho)\n\n"
            "⏳ Free time chal raha hai..."
        )
        return
>>>>>>> 2fd36d67402011f51df74a20dadb87967d0d8394

    # AFTER FREE TIME → PAID
    await msg.answer(
        "⛔ Aapka free time khatam ho chuka hai.\n\n"
        "💰 Paid consultation ke liye payment karein:\n\n"
        f"📱 Mobile: {MOBILE}\n"
        f"💳 UPI: {UPI_ID}"
    )

<<<<<<< HEAD
@router.message(States.question_5)
async def q5(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q5=(msg.text or "").strip())
    data = await state.get_data()
    await save_answers(msg.from_user.id, {
        "q1": data.get("q1"),
        "q2": data.get("q2"),
        "q3": data.get("q3"),
        "q4": data.get("q4"),
        "q5": data.get("q5"),
    })
    await state.set_state(States.pitch)
    await msg.answer("Type karein: *PITCH*")
=======
    # QR SEND
    try:
        photo = FSInputFile(QR_PATH)
        await msg.answer_photo(photo, caption="📸 Scan karke payment karein")
    except:
        await msg.answer("⚠️ QR load nahi hua, manually UPI use karein.")
>>>>>>> 2fd36d67402011f51df74a20dadb87967d0d8394
