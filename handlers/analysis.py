"""
Analysis handler — generates and sends the free Vedic kundli teaser.

States handled:
  - States.waiting_analysis  (entry point after birth data is collected)

After sending the teaser the handler moves the user into the questions flow.
"""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from states.main import States
from utils.astrology import kundli_teaser
from utils.db import get_profile

logger = logging.getLogger(__name__)
router = Router(name="analysis")

ANALYZE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔮 Meri Kundli Dikhao", callback_data="show_kundli")],
    ]
)

QUESTIONS_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Haan, Poochho", callback_data="start_questions")],
        [InlineKeyboardButton(text="⏭ Baad Mein", callback_data="skip_questions")],
    ]
)


# ---------------------------------------------------------------------------
# Entry: user lands in waiting_analysis state
# ---------------------------------------------------------------------------


@router.message(States.waiting_analysis)
async def prompt_analysis(msg: Message, state: FSMContext) -> None:
    """Prompt the user to trigger kundli generation."""
    await msg.answer(
        "🌟 Aapki janma-jankari taiyaar hai!\n\n"
        "Neeche button dabayein aur apni *Vedic Kundli Teaser* dekhein:",
        reply_markup=ANALYZE_KB,
    )


@router.callback_query(F.data == "show_kundli", States.waiting_analysis)
async def show_kundli(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer("🔮 Kundli taiyaar ho rahi hai...")
    await cb.message.edit_reply_markup(reply_markup=None)

    profile = await get_profile(cb.from_user.id)
    if not profile or not profile.dob:
        await cb.message.answer(
            "⚠️ Janma-jankari nahi mili. Kripya /start se dobara shuru karein."
        )
        await state.clear()
        return

    teaser = kundli_teaser(
        name=profile.name or "Aap",
        dob=profile.dob,
        place=profile.place,
    )
    await cb.message.answer(teaser)

    await cb.message.answer(
        "🙏 Kya aap apne jeevan ke baare mein kuch sawaal poochna chahte hain?\n"
        "Main aapke liye 5 vishesh sawaal poochunga.",
        reply_markup=QUESTIONS_KB,
    )
    await state.set_state(States.waiting_questions_start)
    logger.info("User %s received kundli teaser", cb.from_user.id)


@router.callback_query(F.data == "start_questions", States.waiting_questions_start)
async def start_questions(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await cb.message.edit_reply_markup(reply_markup=None)
    await state.update_data(question_index=0)
    await state.set_state(States.waiting_question_answer)
    # Trigger first question via a synthetic message-like flow
    await cb.message.answer(
        "🌟 *Sawaal 1 / 5*\n\n"
        "Aapke jeevan mein abhi sabse badi chunauti kya hai?\n"
        "_(Khulkar likhein — yeh sirf aapke liye hai)_"
    )
    logger.info("User %s started questions flow", cb.from_user.id)


@router.callback_query(F.data == "skip_questions", States.waiting_questions_start)
async def skip_questions(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await cb.message.edit_reply_markup(reply_markup=None)
    await state.set_state(States.waiting_pitch)
    await cb.message.answer(
        "🙏 Theek hai! Aapke liye ek vishesh offer hai..."
    )
    logger.info("User %s skipped questions", cb.from_user.id)
