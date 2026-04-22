"""
Questions handler — collects answers to 5 life-area questions.

States handled:
  - States.waiting_question_answer

After all 5 answers are collected the user is moved to the pitch flow.
"""

import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.main import States
from utils.db import upsert_profile

logger = logging.getLogger(__name__)
router = Router(name="questions")

# The five life-area questions (Hinglish)
QUESTIONS = [
    (
        "🌟 *Sawaal 1 / 5*\n\n"
        "Aapke jeevan mein abhi sabse badi chunauti kya hai?\n"
        "_(Khulkar likhein — yeh sirf aapke liye hai)_"
    ),
    (
        "💼 *Sawaal 2 / 5*\n\n"
        "Aapka career ya vyapar kaisa chal raha hai?\n"
        "Koi pareshani ya sapna jo share karna chahein?"
    ),
    (
        "❤️ *Sawaal 3 / 5*\n\n"
        "Rishton mein — parivaar, dost, ya partner — koi takleef hai?"
    ),
    (
        "💰 *Sawaal 4 / 5*\n\n"
        "Aarthik sthiti (finances) ke baare mein kya soch rahe hain?\n"
        "Koi wishesh lakshya ya chinta?"
    ),
    (
        "🌱 *Sawaal 5 / 5*\n\n"
        "Agle 1 saal mein aap apni zindagi mein kya badlav chahte hain?"
    ),
]


@router.message(States.waiting_question_answer)
async def collect_answer(msg: Message, state: FSMContext) -> None:
    answer = (msg.text or "").strip()
    if not answer:
        await msg.answer("🙏 Kripya apna jawab likhein:")
        return

    data = await state.get_data()
    index: int = data.get("question_index", 0)
    answers: list = data.get("answers", [])

    answers.append(answer)
    index += 1

    await state.update_data(question_index=index, answers=answers)

    # Persist answers as notes
    notes_text = "\n".join(f"Q{i+1}: {a}" for i, a in enumerate(answers))
    await upsert_profile(msg.from_user.id, notes=notes_text)

    if index < len(QUESTIONS):
        # Ask next question
        await msg.answer(QUESTIONS[index])
        logger.info(
            "User %s answered question %d/%d", msg.from_user.id, index, len(QUESTIONS)
        )
    else:
        # All questions answered — move to pitch
        await msg.answer(
            "🙏 Bahut shukriya! Aapne bahut khulkar share kiya.\n\n"
            "Main aapke jawaabon ka vishleshan kar raha hoon... 🔮"
        )
        await state.set_state(States.waiting_pitch)
        logger.info("User %s completed all questions", msg.from_user.id)
