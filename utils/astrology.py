from __future__ import annotations

from datetime import datetime
from math import floor
from typing import Dict, Tuple

import pytz
from dateutil import parser
from geopy.geocoders import Nominatim


RASI_NAMES = [
    "Mesh", "Vrishabh", "Mithun", "Kark", "Singh", "Kanya",
    "Tula", "Vrishchik", "Dhanu", "Makar", "Kumbh", "Meen"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

PLANET_BASE = {
    "Sun": 100.0,
    "Moon": 220.0,
    "Mars": 150.0,
    "Mercury": 90.0,
    "Jupiter": 40.0,
    "Venus": 310.0,
    "Saturn": 280.0,
    "Rahu": 25.0,
    "Ketu": 205.0,
}

PLANET_SPEED = {
    "Sun": 0.9856,
    "Moon": 13.1764,
    "Mars": 0.524,
    "Mercury": 1.2,
    "Jupiter": 0.083,
    "Venus": 1.18,
    "Saturn": 0.033,
    "Rahu": -0.053,
    "Ketu": -0.053,
}


_geolocator = Nominatim(user_agent="vedicguru_simple_bot")


def _deg_to_rasi(deg: float) -> str:
    idx = int((deg % 360) // 30)
    deg_in = (deg % 30)
    return f"{RASI_NAMES[idx]} {deg_in:.1f}°"


def _days_since_epoch(dt: datetime) -> float:
    epoch = datetime(2000, 1, 1, tzinfo=pytz.UTC)
    return (dt - epoch).total_seconds() / 86400.0


def _planet_longitude(planet: str, days: float) -> float:
    return (PLANET_BASE[planet] + PLANET_SPEED[planet] * days) % 360


def _nakshatra_from_deg(deg: float) -> str:
    one = 360.0 / 27.0
    return NAKSHATRAS[int((deg % 360) // one)]


def _dasha_from_moon_deg(moon_deg: float) -> str:
    one = 360.0 / 27.0
    nak_idx = int((moon_deg % 360) // one)
    return DASHA_SEQUENCE[nak_idx % len(DASHA_SEQUENCE)] + " Mahadasha"


def _approx_lagna(dt_local: datetime, lon: float) -> float:
    minutes = dt_local.hour * 60 + dt_local.minute
    # very simplified local sidereal approximation
    return ((minutes / 4.0) + lon) % 360


def parse_birth_to_utc(dob_str: str, tob_str: str, tz_name: str = "Asia/Kolkata") -> datetime:
    dt_local = parser.parse(f"{dob_str} {tob_str}", dayfirst=True)
    tz = pytz.timezone(tz_name)
    return tz.localize(dt_local).astimezone(pytz.UTC)


def get_place_coords(place: str) -> Tuple[float, float]:
    try:
        loc = _geolocator.geocode(f"{place}, India", timeout=8)
        if loc:
            return float(loc.latitude), float(loc.longitude)
    except Exception:
        pass
    return 28.6139, 77.2090  # Delhi fallback


def build_kundli_teaser(name: str, dob: str, tob: str, lat: float, lon: float, language: str = "hinglish") -> str:
    dt_utc = parse_birth_to_utc(dob, tob)
    dt_local = dt_utc.astimezone(pytz.timezone("Asia/Kolkata"))
    days = _days_since_epoch(dt_utc)

    lagna_deg = _approx_lagna(dt_local, lon)
    moon_deg = _planet_longitude("Moon", days)

    positions: Dict[str, str] = {
        p: _deg_to_rasi(_planet_longitude(p, days))
        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    }

    dasha = _dasha_from_moon_deg(moon_deg)
    moon_nakshatra = _nakshatra_from_deg(moon_deg)

    return (
        f"🔮 *Free Kundli Snapshot* (Simplified Vedic Guidance Model)\n\n"
        f"Namaste *{name}* Ji,\n"
        f"🌅 Lagna: *{_deg_to_rasi(lagna_deg)}*\n"
        f"🌙 Chandra Rashi: *{positions['Moon']}*\n"
        f"⭐ Nakshatra: *{moon_nakshatra}*\n"
        f"🕉️ Vimshottari Focus: *{dasha}*\n\n"
        f"☉ Surya: {positions['Sun']}\n"
        f"♂ Mangal: {positions['Mars']}\n"
        f"♃ Guru: {positions['Jupiter']}\n"
        f"♀ Shukra: {positions['Venus']}\n"
        f"♄ Shani: {positions['Saturn']}\n\n"
        f"📍 Birth Place Coordinates: {lat:.2f}, {lon:.2f}\n"
        f"_Yeh free preview hai. Full paid reading mein deeper divisional charts, yogas, timing aur remedies milte hain._"
    )


def daily_gochara_text() -> str:
    now = datetime.now(tz=pytz.UTC)
    days = _days_since_epoch(now)

    saturn = _deg_to_rasi(_planet_longitude("Saturn", days))
    jupiter = _deg_to_rasi(_planet_longitude("Jupiter", days))
    moon = _deg_to_rasi(_planet_longitude("Moon", days))

    return (
        "🌙 *Aaj ka Daily Gochara* (Simplified)\n\n"
        f"♄ Shani Transit: {saturn}\n"
        f"♃ Guru Transit: {jupiter}\n"
        f"☾ Chandra Transit: {moon}\n\n"
        "Guidance: Discipline + patience + mindful communication aaj aapko fayda dega."
    )


def compatibility_teaser_text() -> str:
    return (
        "💑 *Compatibility Teaser*\n\n"
        "Aap dono ke guna-milan, emotional rhythm, communication pattern aur long-term stability ka short diagnostic diya jayega.\n"
        "Full report mein detailed points + practical remedies milte hain."
    )


def basic_remedies_text() -> str:
    return (
        "🪔 *Basic Upay (General)*\n"
        "1) Somvar ko Shiv mantra 108 baar jap.\n"
        "2) Guruwar pe peele daal ka daan.\n"
        "3) Har subah 10 minute deep breathing + Surya arghya.\n"
        "4) Ghar mein shaam ko diya jalakar gratitude practice."
    )
