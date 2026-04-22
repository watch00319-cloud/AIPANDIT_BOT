<<<<<<< HEAD
=======
"""
FSM state definitions for the Vedic Astrology Telegram bot.

Uses aiogram 3.x StatesGroup / State to model the conversation flow.
"""

>>>>>>> 787eb0e8a61139f475f447423ce6b7e0c7e3793e
from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
<<<<<<< HEAD
    # Step 1: Consent & language
    waiting_consent = State()
    waiting_language = State()

    # Step 2: Birth details collection
    waiting_name = State()
    waiting_dob = State()
    waiting_tob = State()
    waiting_place = State()

    # Step 3: Free analysis shown
    analysis = State()

    # Step 4: 5 life questions
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()

    # Step 5: Pitch
    pitch = State()

    # Step 6: Extras
    compatibility = State()
=======
    """Top-level FSM state group for the bot conversation flow."""

    # Onboarding
    waiting_consent = State()    # Waiting for the user to accept the disclaimer
    waiting_language = State()   # Waiting for the user to choose a language
>>>>>>> 787eb0e8a61139f475f447423ce6b7e0c7e3793e
