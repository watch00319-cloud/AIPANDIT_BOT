"""
FSM state definitions for the Vedic Astrology Telegram bot.

Uses aiogram 3.x StatesGroup / State to model the conversation flow.
"""

from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    """Top-level FSM state group for the bot conversation flow."""

    # Onboarding
    waiting_consent = State()    # Waiting for the user to accept the disclaimer
    waiting_language = State()   # Waiting for the user to choose a language
