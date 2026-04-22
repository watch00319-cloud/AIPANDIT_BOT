"""
Birth data collection handler.

Collects name → date of birth → time of birth → place of birth,
then transitions to the analysis step.

States handled:
  - States.waiting_name
  - States.waiting_dob
  - States.waiting_tob
  - States.waiting_place
"""

import logging
import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.main import States
from utils.db import upsert_profile

logger = logging.getLogger(__name__)
router = Router(name="birth_collection")

# Simple date pattern: DD/MM/YYYY or YYYY-MM-DD
_DATE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}|\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})$"
)
# Simple time pattern: HH:MM or HH:MM AM/PM
_TIME_RE = re.compile(
    r"^\d{1,2}:\d{2}(\s*(AM|PM|am|pm))?$"
)


def _normalise_date(raw: str) -> str:
    """Try to convert common date formats to YYYY-MM-DD."""
    raw = raw.strip()
    for sep in ("/", "-", "."):
        parts = raw.split(sep)
        if len(parts) == 3:
            if len(parts[0]) == 4:
                # YYYY-MM-DD already
                return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
            else:
                # DD/MM/YYYY
                return f"{parts[2].zfill(4)}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
    return raw


# ---------------------------------------------------------------------------
# Name
# ---------------------------------------------------------------------------


@router.message(States.waiting_name)
async def collect_name(msg: Message, state: FSMContext) -> None:
    name = msg.text.strip() if msg.text else ""
    if not name or len(name) < 2:
        await msg.answer("🙏 Kripya apna *poora naam* likhein (kam se kam 2 akshar):")
        return

    await upsert_profile(msg.from_user.id, name=name)
    await state.update_data(name=name)

    await msg.answer(
        f"🙏 Namaskar *{name} Ji*!\n\n"
        "Ab apni *janma tithi* (date of birth) batayein.\n"
        "Format: `DD/MM/YYYY`  ya  `YYYY-MM-DD`"
    )
    await state.set_state(States.waiting_dob)
    logger.info("User %s provided name=%r", msg.from_user.id, name)


# ---------------------------------------------------------------------------
# Date of birth
# ---------------------------------------------------------------------------


@router.message(States.waiting_dob)
async def collect_dob(msg: Message, state: FSMContext) -> None:
    raw = (msg.text or "").strip()
    if not _DATE_RE.match(raw):
        await msg.answer(
            "⚠️ Yeh format samajh nahi aaya.\n"
            "Kripya is format mein likhein: `DD/MM/YYYY`  ya  `YYYY-MM-DD`"
        )
        return

    dob = _normalise_date(raw)
    await upsert_profile(msg.from_user.id, dob=dob)
    await state.update_data(dob=dob)

    await msg.answer(
        "⏰ Ab apna *janma samay* (time of birth) batayein.\n"
        "Format: `HH:MM`  (24-hour)  ya  `HH:MM AM/PM`\n\n"
        "_Agar pata nahi, toh '12:00' likh dein._"
    )
    await state.set_state(States.waiting_tob)
    logger.info("User %s provided dob=%r", msg.from_user.id, dob)


# ---------------------------------------------------------------------------
# Time of birth
# ---------------------------------------------------------------------------


@router.message(States.waiting_tob)
async def collect_tob(msg: Message, state: FSMContext) -> None:
    raw = (msg.text or "").strip()
    if not _TIME_RE.match(raw):
        await msg.answer(
            "⚠️ Yeh format samajh nahi aaya.\n"
            "Kripya is format mein likhein: `HH:MM`  ya  `HH:MM AM/PM`"
        )
        return

    tob = raw
    await upsert_profile(msg.from_user.id, tob=tob)
    await state.update_data(tob=tob)

    await msg.answer(
        "📍 Ab apna *janma sthan* (place of birth) batayein.\n"
        "Udaharan: `Mumbai`, `Delhi`, `Patna, Bihar`"
    )
    await state.set_state(States.waiting_place)
    logger.info("User %s provided tob=%r", msg.from_user.id, tob)


# ---------------------------------------------------------------------------
# Place of birth
# ---------------------------------------------------------------------------


@router.message(States.waiting_place)
async def collect_place(msg: Message, state: FSMContext) -> None:
    place = (msg.text or "").strip()
    if not place or len(place) < 2:
        await msg.answer("🙏 Kripya apna *janma sthan* likhein (kam se kam 2 akshar):")
        return

    await upsert_profile(msg.from_user.id, place=place)
    await state.update_data(place=place)

    await msg.answer(
        f"✅ Shukriya! Aapki janma-jankari mil gayi:\n"
        f"📍 Sthan: *{place}*\n\n"
        "🔮 Ab main aapki kundli taiyaar kar raha hoon..."
    )
    await state.set_state(States.waiting_analysis)
    logger.info("User %s provided place=%r → moving to analysis", msg.from_user.id, place)
