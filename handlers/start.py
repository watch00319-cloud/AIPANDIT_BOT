from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

# ===== STATE =====
class UserData(StatesGroup):
    name = State()
    dob = State()
    time = State()
    place = State()


# ===== START COMMAND =====
@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()

    text = """
🔮 Welcome to *Decode Your Future*

🎁 FREE TRIAL ACTIVE
⏳ Aapke paas sirf *2 minutes free* hain

👉 Is time me aap koi bhi question pooch sakte ho

📌 Continue karne ke liye apni details dein

👤 Aapka naam kya hai?
"""
    await message.answer(text, parse_mode="Markdown")

    await state.set_state(UserData.name)


# ===== NAME =====
@router.message(UserData.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("📅 Date of Birth likhein (DD/MM/YYYY)")
    await state.set_state(UserData.dob)


# ===== DOB =====
@router.message(UserData.dob)
async def get_dob(message: types.Message, state: FSMContext):
    await state.update_data(dob=message.text)

    await message.answer("⏰ Birth Time likhein (HH:MM)")
    await state.set_state(UserData.time)


# ===== TIME =====
@router.message(UserData.time)
async def get_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)

    await message.answer("📍 Birth Place likhein")
    await state.set_state(UserData.place)


# ===== PLACE =====
@router.message(UserData.place)
async def get_place(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data["place"] = message.text

    await state.clear()

    await message.answer("""
✅ Details saved!

💬 Ab apna question pucho

⏳ Yaad rahe:
FREE trial sirf 2 minute ka hai
""")
