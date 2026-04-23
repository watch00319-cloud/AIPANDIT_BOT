"""
Vedic Astrology calculation engine using Swiss Ephemeris (pyswisseph).

Provides accurate NASA-grade planetary positions with Lahiri ayanamsa
(standard Indian Vedic sidereal zodiac), true Lagna (Ascendant),
Nakshatra, and Vimshottari Mahadasha.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Tuple

import pytz
import swisseph as swe
from dateutil import parser
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


# ---------------------------------------------------------------------------
# Configure Swiss Ephemeris for Vedic (Lahiri ayanamsa, sidereal zodiac)
# ---------------------------------------------------------------------------
swe.set_sid_mode(swe.SIDM_LAHIRI)
SIDEREAL_FLAG = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED


# ---------------------------------------------------------------------------
# Vedic constants
# ---------------------------------------------------------------------------
RASI_NAMES = [
    "Mesh (Aries)", "Vrishabh (Taurus)", "Mithun (Gemini)", "Kark (Cancer)",
    "Singh (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchik (Scorpio)",
    "Dhanu (Sagittarius)", "Makar (Capricorn)", "Kumbh (Aquarius)", "Meen (Pisces)",
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

# Vimshottari: 27 nakshatras × lords (9-cycle repeats 3 times)
NAK_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
] * 3

DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}  # Total 120 years

DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE,
}

PLANET_HINDI = {
    "Sun": "☉ Surya",
    "Moon": "☾ Chandra",
    "Mars": "♂ Mangal",
    "Mercury": "☿ Budh",
    "Jupiter": "♃ Guru",
    "Venus": "♀ Shukra",
    "Saturn": "♄ Shani",
    "Rahu": "☊ Rahu",
    "Ketu": "☋ Ketu",
}


# ---------------------------------------------------------------------------
# Geocoding + timezone
# ---------------------------------------------------------------------------
_geolocator = Nominatim(user_agent="vedicguru_swisseph_bot")
_tz_finder = TimezoneFinder()


def get_place_coords(place: str) -> Tuple[float, float]:
    """Geocode a place to (lat, lon). Fallback: New Delhi."""
    try:
        loc = _geolocator.geocode(f"{place}, India", timeout=8)
        if loc:
            return float(loc.latitude), float(loc.longitude)
    except Exception:
        pass
    try:
        loc = _geolocator.geocode(place, timeout=8)
        if loc:
            return float(loc.latitude), float(loc.longitude)
    except Exception:
        pass
    return 28.6139, 77.2090


def get_timezone_for_coords(lat: float, lon: float) -> str:
    """Auto-detect IANA timezone. Defaults to Asia/Kolkata."""
    try:
        tz_name = _tz_finder.timezone_at(lat=lat, lng=lon)
        if tz_name:
            return tz_name
    except Exception:
        pass
    return "Asia/Kolkata"


# ---------------------------------------------------------------------------
# Core astronomical calculations
# ---------------------------------------------------------------------------
def parse_birth_to_utc(
    dob_str: str, tob_str: str, tz_name: str = "Asia/Kolkata"
) -> datetime:
    dt_local = parser.parse(f"{dob_str} {tob_str}", dayfirst=True)
    tz = pytz.timezone(tz_name)
    return tz.localize(dt_local).astimezone(pytz.UTC)


def _julian_day(dt_utc: datetime) -> float:
    hour_frac = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_frac)


def _deg_to_rasi_str(deg: float) -> str:
    deg = deg % 360
    idx = int(deg // 30)
    within = deg - idx * 30
    return f"{RASI_NAMES[idx]} {within:.2f}°"


def _nakshatra_from_deg(deg: float) -> Tuple[str, int, int]:
    """Return (nakshatra_name, nakshatra_index 0-26, pada 1-4)."""
    deg = deg % 360
    span = 360.0 / 27.0
    idx = int(deg // span)
    within = deg - idx * span
    pada = int(within // (span / 4.0)) + 1
    return NAKSHATRAS[idx], idx, pada


def _compute_planet_positions(jd: float) -> Dict[str, float]:
    positions: Dict[str, float] = {}
    for name, pid in PLANETS.items():
        result, _ = swe.calc_ut(jd, pid, SIDEREAL_FLAG)
        positions[name] = result[0] % 360
    positions["Ketu"] = (positions["Rahu"] + 180.0) % 360
    return positions


def _compute_lagna(jd: float, lat: float, lon: float) -> float:
    """Sidereal Ascendant (Lagna) using Placidus houses."""
    try:
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b"P", swe.FLG_SIDEREAL)
        return ascmc[0] % 360
    except Exception:
        cusps, ascmc = swe.houses(jd, lat, lon, b"P")
        # subtract ayanamsa manually for sidereal
        ayan = swe.get_ayanamsa_ut(jd)
        return (ascmc[0] - ayan) % 360


def _vimshottari_mahadasha(moon_deg: float, birth_utc: datetime) -> Dict[str, str]:
    """Compute currently-running Vimshottari Mahadasha."""
    span = 360.0 / 27.0
    moon_deg = moon_deg % 360
    nak_idx = int(moon_deg // span)
    within = moon_deg - nak_idx * span
    fraction_elapsed = within / span

    birth_lord = NAK_LORDS[nak_idx]
    total_years = DASHA_YEARS[birth_lord]
    years_remaining_at_birth = total_years * (1.0 - fraction_elapsed)

    now = datetime.now(tz=pytz.UTC)
    elapsed_years = (now - birth_utc).total_seconds() / (365.25 * 24 * 3600)

    lord_cycle_idx = DASHA_ORDER.index(birth_lord)

    if elapsed_years < years_remaining_at_birth:
        running_lord = birth_lord
        time_in_current = elapsed_years
        time_left = years_remaining_at_birth - elapsed_years
    else:
        elapsed_years -= years_remaining_at_birth
        lord_cycle_idx = (lord_cycle_idx + 1) % 9
        while True:
            lord = DASHA_ORDER[lord_cycle_idx]
            yrs = DASHA_YEARS[lord]
            if elapsed_years < yrs:
                running_lord = lord
                time_in_current = elapsed_years
                time_left = yrs - elapsed_years
                break
            elapsed_years -= yrs
            lord_cycle_idx = (lord_cycle_idx + 1) % 9

    end_date = now + timedelta(days=time_left * 365.25)

    return {
        "birth_lord": birth_lord,
        "current_lord": running_lord,
        "elapsed_in_current": f"{time_in_current:.1f} years",
        "remaining_in_current": f"{time_left:.1f} years",
        "current_ends_on": end_date.strftime("%B %Y"),
    }


# ---------------------------------------------------------------------------
# Intelligent concern prediction (rule-based Vedic interpretation)
# ---------------------------------------------------------------------------
DASHA_CONCERNS = {
    "Saturn": [
        "🔸 *Career mein delay* — mehnat ka phal milne mein der ho rahi ho sakti hai",
        "🔸 *Responsibilities ka bojh* badh raha hai, kabhi-kabhi akelapan mehsoos hota hai",
        "🔸 *Health* mein bones, joints ya skin se related issue ho sakti hai",
        "🔸 *Father ya elders* ke saath samay-samay par tension",
    ],
    "Rahu": [
        "🔸 *Confusion + ananya soch* — kya karein, kahaan jaayein samajh nahi aata",
        "🔸 Sudden *ups-downs*, anxiety aur sleep issues",
        "🔸 *Foreign / digital / online* matters mein uljhan ya unexpected events",
        "🔸 Kabhi-kabhi *manipulation* ya dhokha ka samna",
    ],
    "Ketu": [
        "🔸 *Detachment ya isolation* feel hota hai, log-bag se mann nahi lagta",
        "🔸 *Spiritual restlessness* — 'kuch toh missing hai' wala feeling",
        "🔸 *Sudden losses* ya kuch chhoot jane ka ehsaas",
        "🔸 Health mein *mysterious symptoms* jo doctors clearly nahi pakad pate",
    ],
    "Mars": [
        "🔸 *Anger / impatience* — chhoti baaton pe gussa aata hai",
        "🔸 *Conflicts* — partner, siblings ya colleagues se argument",
        "🔸 *Property / land* matters mein dispute ya delay",
        "🔸 *Blood pressure*, accidents ya injury ka risk",
    ],
    "Sun": [
        "🔸 *Authority / boss* ke saath friction, ego clashes",
        "🔸 *Father* ki health ya relationship pe dhyaan",
        "🔸 *Government / job* mein politics ya recognition ki kami",
        "🔸 Self-confidence kabhi up, kabhi down",
    ],
    "Moon": [
        "🔸 *Mood swings*, emotional turbulence",
        "🔸 *Mother* se related chinta ya unka health",
        "🔸 *Mann ashanti* — overthinking, sleep problems",
        "🔸 Relationships mein insecurity",
    ],
    "Mercury": [
        "🔸 *Communication* mein misunderstanding — log galat samajh lete hain",
        "🔸 *Financial decisions* mein confusion ya chhoti galtiyan",
        "🔸 *Studies / skills* mein focus ki kami",
        "🔸 *Nervous system* — tension headaches",
    ],
    "Jupiter": [
        "🔸 *Wisdom + growth* ka samay, lekin kabhi *over-confidence*",
        "🔸 *Children* ya guru se related matters",
        "🔸 *Weight gain*, liver ya digestion",
        "🔸 *Spiritual seeking* badh raha hai",
    ],
    "Venus": [
        "🔸 *Love / marriage* matters mein ups-downs",
        "🔸 *Comforts / luxury* ki ichha vs reality ka gap",
        "🔸 *Partnership* mein trust issues",
        "🔸 *Beauty / art / glamour* field mein opportunities",
    ],
}

# Lagna-specific tendency (broad)
LAGNA_TENDENCIES = {
    0: "Mesh Lagna — aap *naturally aggressive + leader* ho, lekin patience ki kami chinta deti hai",
    1: "Vrishabh Lagna — *security + comfort* prathmikta, lekin change ka dar rehta hai",
    2: "Mithun Lagna — *active mind*, lekin focus ek jagah tikana mushkil",
    3: "Kark Lagna — *emotional + family-oriented*, log aapko hurt karte hain",
    4: "Singh Lagna — *recognition + respect* chahiye, ego hurt hone se taklif",
    5: "Kanya Lagna — *perfectionism* aur over-analysis aapko thaka deti hai",
    6: "Tula Lagna — *relationships + balance* mein toot-phut chinta deti hai",
    7: "Vrishchik Lagna — *secrets + transformation*, trust issues gehre hain",
    8: "Dhanu Lagna — *freedom + truth* chahiye, restrictions chinta dete hain",
    9: "Makar Lagna — *career + status* ke liye over-pressure mehsoos hota hai",
    10: "Kumbh Lagna — *unique soch*, lekin alag hone ka akelapan",
    11: "Meen Lagna — *spiritual + emotional*, duniya ki practicality mushkil lagti hai",
}


def _predict_concerns(
    positions: Dict[str, float],
    lagna_deg: float,
    moon_deg: float,
    dasha: Dict[str, str],
) -> str:
    """Generate an intelligent guess about user's likely concerns
    based on current Mahadasha + Lagna + planetary placements.
    Goal: build trust by showing 'the bot already knows what's bothering you'.
    """
    current_lord = dasha.get("current_lord", "")
    lagna_idx = int(lagna_deg // 30) % 12

    lines = [
        "🔮 *Aapki sambhavit chintayein:*",
        "_(Janm kundali aur abhi chal rahi dasha ke aadhaar par)_",
        "",
        f"💫 Aapki *{current_lord} Mahadasha* chal rahi hai — "
        f"is samay aam taur par ye baatein mehsoos hoti hain:",
        "",
    ]

    # Add 3-4 dasha-specific concerns
    concerns = DASHA_CONCERNS.get(current_lord, [])
    for concern in concerns[:4]:
        lines.append(concern)

    lines.append("")
    lines.append(f"🌟 *Aapka swabhav (Lagna):*")
    lines.append(f"   {LAGNA_TENDENCIES.get(lagna_idx, '')}")

    # Saturn-specific check (most stressful planet)
    saturn_deg = positions.get("Saturn", 0)
    saturn_rasi = int(saturn_deg // 30) % 12
    moon_rasi = int(moon_deg // 30) % 12
    if saturn_rasi in [(moon_rasi - 1) % 12, moon_rasi, (moon_rasi + 1) % 12]:
        lines.append("")
        lines.append("⚠️ *Sade Sati* effect chal raha hai — Shani aapki Chandra rashi ke aas-paas hai.")
        lines.append("   Iska matlab: extra mehnat, akelapan, lekin gehri samajhdari ka samay.")

    # Mars-Saturn or Rahu-Mars proximity = stress markers
    mars_deg = positions.get("Mars", 0)
    rahu_deg = positions.get("Rahu", 0)
    if abs((mars_deg - saturn_deg + 180) % 360 - 180) < 15:
        lines.append("")
        lines.append("⚡ *Mars-Saturn yog* — frustration aur ruke hue kaam ka pattern dikhta hai.")
    if abs((mars_deg - rahu_deg + 180) % 360 - 180) < 15:
        lines.append("")
        lines.append("⚡ *Angarak Yog* (Mars-Rahu) — sudden anger aur impulsive decisions se savdhaan.")

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append(
        "_Agar inn mein se kuch baatein aapko sahi lagi, "
        "toh aap akele nahi hain. Iska *poora samadhan* mil sakta hai._"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public high-level functions (used by handlers)
# ---------------------------------------------------------------------------
def build_kundli_teaser(
    name: str,
    dob: str,
    tob: str,
    lat: float,
    lon: float,
    language: str = "hinglish",
) -> str:
    """Full accurate Vedic kundli snapshot (Swiss Ephemeris + Lahiri)."""
    tz_name = get_timezone_for_coords(lat, lon)
    try:
        dt_utc = parse_birth_to_utc(dob, tob, tz_name=tz_name)
    except Exception:
        return "❌ DOB/TOB format galat hai. Please /reset karein."

    jd = _julian_day(dt_utc)

    try:
        positions = _compute_planet_positions(jd)
        lagna_deg = _compute_lagna(jd, lat, lon)
    except Exception as e:
        return f"⚠️ Calculation error: {e}. Please /reset and try again."

    moon_deg = positions["Moon"]
    moon_nak, _, moon_pada = _nakshatra_from_deg(moon_deg)
    lagna_nak, _, _ = _nakshatra_from_deg(lagna_deg)
    dasha = _vimshottari_mahadasha(moon_deg, dt_utc)

    lines = [
        "🔮 *FREE KUNDLI SNAPSHOT*",
        "_Swiss Ephemeris • Lahiri Ayanamsa_",
        "",
        f"Namaste *{name}* Ji 🙏",
        f"📅 Janam: {dob} at {tob}",
        f"🌐 TZ: {tz_name}",
        f"📍 Sthan: {lat:.4f}°, {lon:.4f}°",
        "",
        "━━━━━━━━━━━━━━━━━━",
        "🌅 *Lagna (Ascendant)*",
        f"   → {_deg_to_rasi_str(lagna_deg)}",
        f"   → Nakshatra: *{lagna_nak}*",
        "",
        "🌙 *Janma Rashi (Moon Sign)*",
        f"   → {_deg_to_rasi_str(moon_deg)}",
        f"   → Nakshatra: *{moon_nak}* (Pada {moon_pada})",
        "",
        "━━━━━━━━━━━━━━━━━━",
        "🪐 *Grah Sthiti*",
    ]

    for planet in ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        lines.append(f"   {PLANET_HINDI[planet]}: {_deg_to_rasi_str(positions[planet])}")

    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━",
        "🕉️ *Vimshottari Mahadasha*",
        f"   Janma Dasha: *{dasha['birth_lord']}*",
        f"   Abhi chal rahi: *{dasha['current_lord']}* Mahadasha",
        f"   Elapsed: {dasha['elapsed_in_current']}",
        f"   Remaining: {dasha['remaining_in_current']}",
        f"   Changes on: *{dasha['current_ends_on']}*",
        "",
        "━━━━━━━━━━━━━━━━━━",
    ]

    # 🔮 Intelligent concern prediction — makes bot feel experienced
    lines.append(_predict_concerns(positions, lagna_deg, moon_deg, dasha))

    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━",
        "_Ye exact astronomical data hai (NASA-grade Swiss Ephemeris). "
        "Full paid reading mein D1/D9 charts, yogas, ashtakvarga, "
        "personalized remedies aur 2 prashn ka uttar milta hai._",
    ]
    return "\n".join(lines)


def daily_gochara_text() -> str:
    """Live planetary transits for current UTC moment."""
    now = datetime.now(tz=pytz.UTC)
    jd = _julian_day(now)
    positions = _compute_planet_positions(jd)

    lines = ["🌙 *Aaj ka Gochara* (Live Transits)\n"]
    for planet in ["Moon", "Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        lines.append(f"{PLANET_HINDI[planet]}: {_deg_to_rasi_str(positions[planet])}")

    lines.append("\n_Guidance: Chandra + Guru ka rhythm dekhte hue patience + clarity rakhein._")
    return "\n".join(lines)


def compatibility_teaser_text() -> str:
    return (
        "💑 *Compatibility Teaser* (Ashtakoot Guna Milan)\n\n"
        "Aap dono ke:\n"
        "• Guna Milan (out of 36)\n"
        "• Chandra compatibility (emotional rhythm)\n"
        "• Budh + Shukra (communication + affection)\n"
        "• Mangal Dosha check\n"
        "• Long-term stability score\n\n"
        "Full report mein detailed points + practical remedies milte hain."
    )


def basic_remedies_text() -> str:
    return (
        "🪔 *Basic Upay (General)*\n\n"
        "1) Somvar ko Shiv mantra *Om Namah Shivaya* 108 baar jap.\n"
        "2) Guruwar pe peele daal + haldi ka daan.\n"
        "3) Har subah 10 min pranayama + Surya arghya.\n"
        "4) Shaam ko ghar mein diya jalakar gratitude practice.\n"
        "5) Shanivar ko kale til + sarson ka tel daan.\n\n"
        "_Personalized remedies ke liye full paid reading karayein._"
    )

def generate_daily_personalized(
    name: str,
    dob: str,
    tob: str,
    lat: float,
    lon: float
) -> str:
    \"\"\"Generate personalized daily horoscope based on kundli + current transits.\"\"\"
    tz_name = get_timezone_for_coords(lat, lon)
    try:
        birth_utc = parse_birth_to_utc(dob, tob, tz_name)
    except Exception:
        return \"Namaste %s ji 🌟\\nAaj positivity aur patience focus karein!\" % name

    jd_birth = _julian_day(birth_utc)
    try:
        positions_birth = _compute_planet_positions(jd_birth)
        moon_deg = positions_birth[\"Moon\"]
        dasha = _vimshottari_mahadasha(moon_deg, birth_utc)
    except Exception:
        return \"Namaste %s ji! 🌟\\nAaj ka din shubh rahe!\" % name

    current_lord = dasha[\"current_lord\"]
    concerns = DASHA_CONCERNS.get(current_lord, [])
    gochara = daily_gochara_text()

    lines = [
        \"🌅 *Namaste %s ji!* 🙏\" % name,
        \"_Aapka *daily personalized horoscope* (kundali based)_ \",
        \"\",
        \"💫 *Chal rahi Dasha:* *%s*\" % current_lord,
        \"⏳ Baaki: %s | Ends: %s\" % (dasha[\"remaining_in_current\"], dasha[\"current_ends_on\"]),
        \"\",
        \"🔮 *Aaj ki chintayein:* \",
    ]

    for concern in concerns[:3]:
        lines.append(\"  • %s\" % concern)

    lines += [
        \" \",
        \"🪐 *Aaj ka Gochara:* \",
    ]

    gochara_parts = gochara.splitlines()
    for part in gochara_parts[1:5]:
        lines.append(\"  %s\" % part)

    lines += [
        \"\",
        \"✨ *Simple upay:* ☀️ Surya ko jal arpan + positive affirmations. \",
        \" \",
        \"_Trusted Vedic calculations se bana. Daily ke liye subscribed rahen!_ 🌟 \"
    ]

    return \"\\n\".join(lines)
