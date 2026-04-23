from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
router = Router()

@router.message(F.text)
async def fallback(msg: Message, state: FSMContext):
    current = await state.get_state()
    await msg.answer(f"❓ Samajh nahi aaya.\\nCurrent state: {current or 'None'}\\n/help or /reset.")

