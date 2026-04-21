from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
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
