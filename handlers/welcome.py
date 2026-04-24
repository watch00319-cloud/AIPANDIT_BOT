from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States

router = Router()

WELCOME_MSG = (
    "🔮 *Welcome to Decode Your Future*\n\n"
    "✨ Main aapki *Janam Kundali* ke base par analysis karta hoon\n\n"
    "📊 Aapko milega:\n"
    "• Aapki rashi aur grah sthiti\n"
    "• Aapka personality analysis\n"
    "• Current life situation (dasha)\n\n"
    "🎁 Aapko *FREE trial (2 min)* mil raha hai\n\n"
    "👉 Shuru karne ke liye niche click karein"
)

kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Haan Ji, Shuru Karein", callback_data="start_onboarding")]
    ]
)

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(WELCOME_MSG, reply_markup=kb)
    await state.set_state(States.waiting_name)


@router.callback_query(F.data == "start_onboarding")
async def start_onboarding(callback, state: FSMContext):
    await callback.message.answer("🧑 Aapka naam kya hai?")
    await state.set_state(States.waiting_name)
    await callback.answer()