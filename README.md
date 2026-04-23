# VedicGuru AI — Vedic Astrology Telegram Bot 🌟🔮

Production-ready Vedic Astrology Telegram bot built with **aiogram 3.x**.

- Async aiogram 3.x with FSM-based 6-step consultation flow
- SQLite + SQLAlchemy async (zero-config, wheel-friendly — no Rust/C++ toolchain)
- Lightweight astrology engine (no `pyswisseph`)
- Ready to deploy on Railway / any Python PaaS

---

## Features

- Maharishi AstroGuru Ji persona (Hindi + Hinglish)
- Birth details collection (name, DOB, TOB, place)
- Free partial kundli snapshot
- Daily Gochara + Compatibility teaser buttons
- 5 life-questions flow
- Value-building + premium pitch
- WhatsApp CTA routing (9888601933)
- User memory persistence (SQLite; optional persistent volume)
- Explicit disclaimer messaging

---

## Project Structure

```text
vedic_astrology_bot/
├── main.py                 # entry point (loads env, sets up logging, starts polling)
├── Procfile                # worker: python main.py  (Railway / Heroku)
├── requirements.txt
├── .gitignore
├── .env                    # LOCAL ONLY — never commit
├── handlers/
│   ├── __init__.py
│   ├── welcome.py          # /start, consent, language
│   ├── birth_collection.py # name, DOB, TOB, place
│   ├── analysis.py         # ANALYZE → kundli teaser
│   ├── questions.py        # Q1..Q5
│   ├── pitch.py            # PITCH → premium CTA
│   └── extras.py           # /help, /reset, gochara, compatibility
├── states/
│   ├── __init__.py
│   └── main.py             # FSM States
└── utils/
    ├── __init__.py
    ├── astrology.py        # teaser/remedy/gochara helpers
    └── db.py               # async SQLAlchemy models + helpers
```

All runtime imports are **absolute** (`from handlers.welcome import router`, `from states.main import States`, `from utils.db import init_db`). The project root (`vedic_astrology_bot/` locally, `/app/` on Railway) is on `sys.path`, so these work identically in both environments.

---

## 1) Local Setup (Windows)

```bat
cd vedic_astrology_bot

:: create & activate venv
python -m venv .venv
.venv\Scripts\activate

:: install deps
pip install -r requirements.txt
```

Create a `.env` file next to `main.py`:

```env
BOT_TOKEN=123456:your-telegram-bot-token-from-BotFather
LOG_LEVEL=INFO
# optional, only if you mount a persistent volume:
# DATABASE_URL=sqlite+aiosqlite:///./bot_users.db
```

Run:

```bat
python main.py
```

Expected log:

```
... | INFO | vedic_astrology_bot | Initializing database ...
... | INFO | vedic_astrology_bot | Bot polling started
```

Press `Ctrl+C` to stop.

---

## 2) Deploy to Railway

1. **Push this repo to GitHub** (the repo root must contain `main.py`, `handlers/`, `states/`, `utils/`, `requirements.txt`, `Procfile`).
2. In Railway, **New Project → Deploy from GitHub** → pick this repo.
3. Go to the service's **Variables** tab and add:

   | Key | Value |
   |---|---|
   | `BOT_TOKEN` | your Telegram bot token from @BotFather |
   | `LOG_LEVEL` | `INFO` (optional) |
   | `DATABASE_URL` | *(optional)* e.g. `sqlite+aiosqlite:////data/bot_users.db` if you mount a persistent volume at `/data` |

4. Railway auto-detects the `Procfile` and runs: `python main.py`.
5. Check **Deploy Logs**. You should see:
   ```
   Bot polling started
   ```
6. Message your bot on Telegram — it should reply to `/start`.

### Start Command

`python main.py` (set by `Procfile`). If your platform ignores `Procfile`, configure the start command manually to `python main.py`.

### ⚠️ Security

If `BOT_TOKEN` was ever committed (even once) in git history, **rotate it immediately** via @BotFather, and only put the new token in Railway's Variables tab. `.env` is git-ignored now.

---

## 3) Bot Commands

| Command | Purpose |
|---|---|
| `/start` | Start / restart the consultation flow |
| `/help`  | Show available commands |
| `/reset` | Reset current session state |

---

## Troubleshooting

| Symptom in Railway logs | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'handlers'` | `handlers/`, `states/`, or `utils/` not in the repo | Make sure those folders (with `__init__.py`) are committed & pushed |
| `BOT_TOKEN is not set.` | No `BOT_TOKEN` env var | Add `BOT_TOKEN` in Railway → Variables, then redeploy |
| `TelegramUnauthorizedError` | Token revoked / wrong | Generate new token via @BotFather, update `BOT_TOKEN` |
| Two instances of bot running (`Conflict: terminated by other getUpdates request`) | Local dev and Railway both polling same token | Stop one. Use separate tokens for dev vs prod |

---

## Disclaimer

Astrology content here is for spiritual guidance and self-reflection only.  
Not a substitute for legal, medical, or financial advice.
