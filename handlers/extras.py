from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.main import States
from utils.astrology import daily_gochara_text, compatibility_teaser_text

router = Router()


@router.callback_query(F.data == "gochara")
async def gochara_callback(callback: CallbackQuery):
    await callback.message.answer(daily_gochara_text())
    await callback.answer()


@router.callback_query(F.data == "compat")
async def compat_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        compatibility_teaser_text()
        + "\n\nAgar full compatibility reading chahiye, seedha WhatsApp karein: 6283941933"
    )
    await state.set_state(States.compatibility)
    await callback.answer()


@router.message(States.compatibility)
async def compatibility_input(msg: Message, state: FSMContext):
    await msg.answer(
        "Details receive ho gayi.\n"
        "Teaser complete ✅\n"
        "Full compatibility session ke liye contact karein: *6283941933*"
    )
    await state.set_state(States.pitch)


@router.message(Command("help"))
async def help_cmd(msg: Message):
    await msg.answer(
        "Commands:\n"
        "/start - Nayi consultation shuru karein\n"
        "/reset - Current session reset\n"
        "/help - Ye help text"
    )


@router.message(Command("reset"))
async def reset_cmd(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Session reset ho gaya. Dobara shuru karne ke liye /start likhiye.")
