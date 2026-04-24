from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.main import States
from utils.db import save_answers
from .payment import trigger_payment

router = Router()


@router.message(States.question_1)
async def q1(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q1=(msg.text or "").strip())
    await msg.answer("Q2/5: Vivah/relationship ko lekar aap kya guidance chahte hain?")
    await state.set_state(States.question_2)


@router.message(States.question_2)
async def q2(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q2=(msg.text or "").strip())
    await msg.answer("Q3/5: Health ya stress ke kis area par clarity chahiye?")
    await state.set_state(States.question_3)


@router.message(States.question_3)
async def q3(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q3=(msg.text or "").strip())
    await msg.answer("Q4/5: Finance/wealth growth mein abhi sabse bada concern kya hai?")
    await state.set_state(States.question_4)


@router.message(States.question_4)
async def q4(msg: Message, state: FSMContext):
    if await trigger_payment(msg):
        return
    await state.update_data(q4=(msg.text or "").strip())
    await msg.answer("Q5/5: Koi specific prashna jo aap turant solve karna chahte hain?")
    await state.set_state(States.question_5)


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
