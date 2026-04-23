from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from states.main import States
from utils.astrology import build_kundli_teaser, basic_remedies_text

router = Router()


@router.message(States.analysis)
async def show_free_analysis(msg: Message, state: FSMContext):
    if (msg.text or "").strip().lower() != "analyze":
        await msg.answer("Analysis shuru karne ke liye *ANALYZE* likhiye.")
        return

    data = await state.get_data()

    chart = build_kundli_teaser(
        name=data.get("name", "Mitra"),
        dob=data.get("dob", "01/01/2000"),
        tob=data.get("tob", "12:00"),
        lat=float(data.get("lat", 28.6139)),
        lon=float(data.get("lon", 77.2090)),
        language=data.get("language", "hinglish"),
    )

    msg_text = (
        f"{chart}\n\n"
        "✅ Aapka free kundali analysis ready hai.\n\n"
        "**FREE TRIAL**\n"
        "Ab aap apne past, present, ya future se juda koi bhi ek sawaal bilkul free mein pooch sakte hain.\n\n"
        "Hamare expert astrologer aapke graho ki sthiti ka analysis karke aapko sateek jawaab denge aur uska kaaran bhi batayenge.\n\n"
        "** Apna sawaal neeche type karein:**"
    )

    await msg.answer(msg_text)
    await state.set_state(States.free_question)


@router.message(States.free_question)
async def handle_free_question(msg: Message, state: FSMContext):
    question = (msg.text or "").strip()
    if len(question) < 5:
        await msg.answer("Kripya apna sawaal vistar se likhein.")
        return

    # Placeholder for astrologer's answer
    answer = (
        "**Aapke sawaal ka jawaab:**\n\n"
        "Hamare jyotishiyon ne aapki kundali ka gehraai se vishleshan kiya hai. "
        "Aapke graho ki sthiti ke anusaar, [yahan jyotishi ka jawaab aayega]...\n\n"
        "**Kya aap is pareshani ka samaadhaan chahte hain?**\n"
        "Agar aap is samasya se raahat paana chahte hain, to hamari paid services aapki madad kar sakti hain. "
        "₹499 ya ₹1100 ki maamuli fees aapki pareshani se badi nahi hai. "
        "Hum aapko 100% sateek upaay denge aur aapki samasya ka samaadhaan hamari pehli prathmikta hogi.\n\n"
        "Type karein: *SERVICES*"
    )

    await msg.answer(answer)
    await state.set_state(States.pitch)

