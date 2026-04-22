"""
FSM state definitions for the Vedic Astrology Telegram bot.

Uses aiogram 3.x StatesGroup / State to model the conversation flow.
"""

from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    """Top-level FSM state group for the bot conversation flow."""

    # Onboarding
    waiting_consent = State()           # Waiting for the user to accept the disclaimer
    waiting_language = State()          # Waiting for the user to choose a language

    # Birth data collection
    waiting_name = State()              # Waiting for the user's full name
    waiting_dob = State()               # Waiting for date of birth
    waiting_tob = State()               # Waiting for time of birth
    waiting_place = State()             # Waiting for place of birth

    # Analysis
    waiting_analysis = State()          # Kundli teaser generation step

    # Questions flow
    waiting_questions_start = State()   # Prompt to start or skip the 5-question flow
    waiting_question_answer = State()   # Collecting individual question answers

    # Premium pitch
    waiting_pitch = State()             # Showing the premium consultation offer
