from onboarding import start_onboarding, handle_onboarding, is_user_ready, is_free_time_valid

@bot.message_handler(commands=['start'])
def start(message):
    reply = start_onboarding(message.chat.id)
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda msg: True)
def all_messages(message):
    user_id = message.chat.id

    # 🔥 अगर onboarding complete नहीं
    if not is_user_ready(user_id):
        reply = handle_onboarding(user_id, message.text)
        bot.send_message(user_id, reply)
        return

    # 🔥 free time check
    if is_free_time_valid(user_id):
        # 👉 यहाँ अपना AI response डालो
        bot.send_message(user_id, f"🔮 Aapka jawab:\n\n{message.text} (AI response yaha ayega)")
    else:
        bot.send_message(
            user_id,
            "⛔ Free time khatam ho gaya hai.\n\n💳 Paid service use kare.\nUPI: darksecrets0unveiled@okhdfcbank"
        )
