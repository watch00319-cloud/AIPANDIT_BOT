from aiogram import F, Router, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.main import States

router = Router()

@router.message(StateFilter(None), F.text)
async def fallback(msg: Message, state: FSMContext):
    current = await state.get_state()
    await msg.answer(f"❓ Samajh nahi aaya.\\nCurrent state: {current or 'None'}\\n/help or /reset.")

# State-specific fallbacks to prevent 'not handled'
@router.message(States.analysis)
async def analysis_fallback(msg: Message, state: FSMContext):
    lower_text = (msg.text or "").strip().lower()
    if len(lower_text) > 0 and 'analyze' in lower_text:
        # Let main handler catch it, but since order, this is safety
        await msg.answer("Analysis processing... (if not triggered, type exactly 'analyze')")
    else:
        await msg.answer("🔮 Free kundali analysis ke liye *ANALYZE* type karein! 🌟")

@router.message(States.analysis, ~F.text)
async def analysis_nontext(msg: Message):
    await msg.answer("📝 Text message bhejiye aur *ANALYZE* type karein.")

@router.message(States.free_question)
async def free_question_fallback(msg: Message, state: FSMContext):
    await msg.answer("Aapka sawaal type karein (5+ words).")

@router.message(States.pitch)
async def pitch_fallback(msg: Message, state: FSMContext):
    await msg.answer("Services dekhne ke liye *PITCH* ya /services type karein.")

@router.message(States.pitch, ~F.text)
async def pitch_nontext(msg: Message):
    await msg.answer("Text type karein: *PITCH* for services.")

