from aiogram import F, Router, StateFilter


from aiogram.types import Message
from aiogram.fsm.context import FSMContext
router = Router()

@router.message(StateFilter(None), F.text)
async def fallback(msg: Message, state: FSMContext):

    current = await state.get_state()
    await msg.answer(f"❓ Samajh nahi aaya.\\nCurrent state: {current or 'None'}\\n/help or /reset.")
