"""
Astrology calculation utilities for the Vedic Astrology Telegram bot.

Provides lightweight helpers for generating kundli teasers, daily Gochara
snippets, and compatibility blurbs without requiring pyswisseph or any
compiled extension.
"""

import logging
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rashi (Moon-sign) lookup — simplified, based on birth month
# ---------------------------------------------------------------------------

_RASHI_BY_MONTH = {
    1: ("Makar", "Capricorn"),
    2: ("Kumbh", "Aquarius"),
    3: ("Meen", "Pisces"),
    4: ("Mesh", "Aries"),
    5: ("Vrishabh", "Taurus"),
    6: ("Mithun", "Gemini"),
    7: ("Kark", "Cancer"),
    8: ("Simha", "Leo"),
    9: ("Kanya", "Virgo"),
    10: ("Tula", "Libra"),
    11: ("Vrishchik", "Scorpio"),
    12: ("Dhanu", "Sagittarius"),
}

_NAKSHATRA_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]


def get_rashi(dob: str) -> tuple[str, str]:
    """Return (hindi_name, english_name) for the Rashi based on birth month.

    *dob* should be in ``YYYY-MM-DD`` format.  Falls back to Mesh/Aries on
    any parse error.
    """
    try:
        birth_date = date.fromisoformat(dob)
        return _RASHI_BY_MONTH.get(birth_date.month, ("Mesh", "Aries"))
    except (ValueError, AttributeError):
        logger.warning("Could not parse dob=%r for rashi lookup", dob)
        return ("Mesh", "Aries")


def get_nakshatra(dob: str) -> str:
    """Return a Nakshatra name derived deterministically from the birth date."""
    try:
        birth_date = date.fromisoformat(dob)
        day_of_year = birth_date.timetuple().tm_yday
        index = day_of_year % len(_NAKSHATRA_LIST)
        return _NAKSHATRA_LIST[index]
    except (ValueError, AttributeError):
        return "Ashwini"


def kundli_teaser(name: str, dob: str, place: Optional[str] = None) -> str:
    """Return a short Vedic kundli teaser message (Hinglish)."""
    rashi_hi, rashi_en = get_rashi(dob)
    nakshatra = get_nakshatra(dob)
    place_str = f" ({place})" if place else ""

    return (
        f"🔮 *{name} Ji ka Vedic Kundli Snapshot*\n\n"
        f"📅 Janma Tithi: `{dob}`{place_str}\n"
        f"♈ Rashi: *{rashi_hi}* ({rashi_en})\n"
        f"⭐ Nakshatra: *{nakshatra}*\n\n"
        f"_Yeh sirf ek teaser hai. Poori kundli ke liye premium consultation lein._"
    )


def daily_gochara_teaser(rashi_hi: str) -> str:
    """Return a short daily Gochara teaser for the given Rashi (Hinglish)."""
    return (
        f"🌙 *Aaj ka Gochara — {rashi_hi} Rashi*\n\n"
        "Aaj Chandra aapke liye shubh samay la raha hai. "
        "Vyapar mein savdhani rakhein aur parivaar ko samay dein.\n\n"
        "_Poori Gochara report ke liye premium plan dekhein._"
    )


def compatibility_teaser(rashi_a: str, rashi_b: str) -> str:
    """Return a short compatibility teaser between two Rashis (Hinglish)."""
    return (
        f"💑 *Compatibility: {rashi_a} × {rashi_b}*\n\n"
        "Aapka milan 72% compatible hai. Kuch chhote matabed ho sakte hain, "
        "lekin pyaar aur samajh se sab theek ho sakta hai.\n\n"
        "_Detailed compatibility report ke liye premium plan lein._"
    )
