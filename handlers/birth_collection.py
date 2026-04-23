from datetime import datetime
import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.main import States
from utils.astrology import get_place_coords
from utils.db import upsert_profile

logger = logging.getLogger(__name__)
router = Router()


def _valid_dob(value: str) -> bool:
    try:
        datetime.strptime(value.strip(), "%d/%m/%Y")
        return True
    except ValueError:
        return False


def _valid_tob(value: str) -> bool:
    try:
        datetime.strptime(value.strip(), "%H:%M")
        return True
    except ValueError:
        return False


@router.message(States.waiting_name)
async def collect_name(msg: Message, state: FSMContext):
    name = (msg.text or "").strip()
    if len(name) < 2:
        await msg.answer("Naam thoda clearly likhiye (minimum 2 characters).")
        return

    await state.update_data(name=name)
    await msg.answer("📅 Aapki date of birth? (DD/MM/YYYY)")
    await state.set_state(States.waiting_dob)


@router.message(States.waiting_dob)
async def collect_dob(msg: Message, state: FSMContext):
    dob = (msg.text or "").strip()
    if not _valid_dob(dob):
        await msg.answer("DOB format galat hai. Example: *24/10/1998*")
        return

    await state.update_data(dob=dob)
    await msg.answer("⏰ Janam ka samay? (HH:MM)")
    await state.set_state(States.waiting_tob)


@router.message(States.waiting_tob)
async def collect_tob(msg: Message, state: FSMContext):
    tob = (msg.text or "").strip()
    if not _valid_tob(tob):
        await msg.answer("Time format galat hai. Example: *14:35*")
        return

    await state.update_data(tob=tob)
    await msg.answer("📍 Janam sthal?")
    await state.set_state(States.waiting_place)


@router.message(States.waiting_place)
async def collect_place(msg: Message, state: FSMContext):
    place = (msg.text or "").strip()
    if len(place) < 2:
        await msg.answer("City name valid format mein bhejiye.")
        return

    lat, lon = get_place_coords(place)
    await state.update_data(place=place, lat=lat, lon=lon)

    data = await state.get_data()
    await upsert_profile(
        user_id=msg.from_user.id,
        data={
            "name": data.get("name"),
            "dob": data.get("dob"),
            "tob": data.get("tob"),
            "place": place,
            "lat": lat,
            "lon": lon,
            "language": data.get("language", "hinglish"),
            "horoscope_subscribed": True,
        },
    )

    logger.info(f"User Data: {{'chatId': {msg.chat.id}, 'userId': {msg.from_user.id}, 'data': {data}}}")

    await msg.answer(
        "✅ *Details saved!* 🌟\n\n"
        "🎁 *Auto subscribed* free **daily personalized horoscope** (name ke according kundali analysis)!\n"
        "/unsubscribe anytime.\n\n"
        "🔮 Ab *ANALYZE* type karein!"
    )
    await state.set_state(States.analysis)

