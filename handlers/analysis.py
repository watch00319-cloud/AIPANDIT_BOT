from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States
from utils.astrology import build_kundli_teaser, basic_remedies_text

router = Router()


@router.message(States.analysis)
async def show_free_analysis(msg: Message, state: FSMContext):
    if (msg.text or "").strip().lower() != "analyze":
        await msg.answer("Analysis shuru karne ke liye *ANALYZE* likhiye.")
        return

    data = await state.get_data()

    chart = build_kundli_teaser(
        name=data.get("name", "Mitra"),
        dob=data.get("dob", "01/01/2000"),
        tob=data.get("tob", "12:00"),
        lat=float(data.get("lat", 28.6139)),
        lon=float(data.get("lon", 77.2090)),
        language=data.get("language", "hinglish"),
    )

    msg_text = (
        f"{chart}\n\n"
        f"{basic_remedies_text()}\n\n"
        "Step 6/6 ✅ Free preview complete.\n"
        "Ab main aapse 5 life questions loonga, fir final premium recommendation dunga."
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌙 Daily Gochara", callback_data="gochara")],
            [InlineKeyboardButton(text="💑 Compatibility Teaser", callback_data="compat")],
        ]
    )

    await msg.answer(msg_text, reply_markup=kb)
    await msg.answer("Q1/5: Career ya business mein aapki sabse badi chinta kya hai?")
    await state.set_state(States.question_1)

