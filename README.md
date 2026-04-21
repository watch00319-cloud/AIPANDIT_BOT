# VedicGuru AI - Simplified Windows-Friendly Telegram Bot 🌟🔮

Production-ready but simplified Vedic Astrology Telegram bot with:
- aiogram 3.x (async)
- SQLite + SQLAlchemy (no migrations)
- FSM-based 6-step consultation flow
- No `pyswisseph`, no Rust/Cargo, no C++ build tools required

## Features Included

- Maharishi AstroGuru Ji persona (Hindi + Hinglish tone)
- Birth details collection (name, DOB, TOB, place)
- Free partial kundli snapshot (simplified guidance engine)
- Daily Gochara button
- Compatibility teaser
- 5 life questions collection
- Value-building + premium pitch
- **100% Money-Back Guarantee** messaging
- Direct contact routing to **6283941933**
- Basic remedies
- User memory persistence (SQLite)
- Disclaimer messaging

---

## 1-Minute Setup (Windows)

### 1) Open terminal and go to project
```bat
cd c:\Users\thenu\OneDrive\Desktop\your_life_solution\vedic_astrology_bot
```

### 2) (Recommended) create and activate virtual environment
```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3) Install dependencies
```bat
pip install -r requirements.txt
```

### 4) Create `.env` file
Create a file named `.env` in `vedic_astrology_bot` folder:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
```

### 5) Run bot
```bat
python main.py
```

---

## Bot Commands

- `/start` → Start full consultation flow
- `/help` → Show help
- `/reset` → Reset current session state

---

## Project Structure

```text
vedic_astrology_bot/
├── main.py
├── requirements.txt
├── README.md
├── handlers/
│   ├── __init__.py
│   ├── welcome.py
│   ├── birth_collection.py
│   ├── analysis.py
│   ├── questions.py
│   ├── pitch.py
│   └── extras.py
├── states/
│   ├── __init__.py
│   └── main.py
└── utils/
    ├── __init__.py
    ├── astrology.py
    └── db.py
```

---

## Notes

- The astrology engine is intentionally simplified for zero-build Windows compatibility.
- Outputs are guidance-oriented and deterministic, suitable for lead-generation flow.
- For strict classical precision ephemeris, heavy native dependencies are usually required (intentionally avoided here for easy install).

---

## Disclaimer

Astrology content is for spiritual guidance and self-reflection only.  
Not a substitute for legal, medical, or financial advice.
