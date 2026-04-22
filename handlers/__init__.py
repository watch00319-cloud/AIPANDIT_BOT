"""
Handlers package for the Vedic Astrology Telegram bot.

Each sub-module defines an aiogram Router that is included into the
Dispatcher in main.py.
"""

from handlers.welcome import router as welcome_router
from handlers.birth_collection import router as birth_collection_router
from handlers.analysis import router as analysis_router
from handlers.questions import router as questions_router
from handlers.pitch import router as pitch_router
from handlers.extras import router as extras_router

__all__ = [
    "welcome_router",
    "birth_collection_router",
    "analysis_router",
    "questions_router",
    "pitch_router",
    "extras_router",
]
