import json
import time

USER_FILE = "user_data.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def start_onboarding(user_id):
    users = load_users()

    users[str(user_id)] = {
        "step": "name",
        "name": "",
        "dob": "",
        "time": "",
        "place": "",
        "free_start": None,
        "completed": False
    }

    save_users(users)

    return "🙏 Namaste!\n\nAapka naam bataye?"

def handle_onboarding(user_id, message):
    users = load_users()
    user = users.get(str(user_id))

    if not user:
        return start_onboarding(user_id)

    step = user["step"]

    if step == "name":
        user["name"] = message
        user["step"] = "dob"
        save_users(users)
        return "📅 Apni Date of Birth bataye (DD-MM-YYYY)"

    elif step == "dob":
        user["dob"] = message
        user["step"] = "time"
        save_users(users)
        return "⏰ Birth Time bataye (HH:MM AM/PM)"

    elif step == "time":
        user["time"] = message
        user["step"] = "place"
        save_users(users)
        return "📍 Birth Place bataye"

    elif step == "place":
        user["place"] = message
        user["step"] = "done"
        user["completed"] = True
        user["free_start"] = time.time()
        save_users(users)

        return (
            f"✅ Details saved!\n\n"
            f"Naam: {user['name']}\n"
            f"DOB: {user['dob']}\n"
            f"Time: {user['time']}\n"
            f"Place: {user['place']}\n\n"
            f"⏳ Aapka FREE 2 minute start ho chuka hai.\n"
            f"👉 Ab apna sawal puchiye"
        )

    return "❌ Error, please restart with /start"

def is_free_time_valid(user_id):
    users = load_users()
    user = users.get(str(user_id))

    if not user or not user.get("free_start"):
        return False

    return (time.time() - user["free_start"]) <= 120

def is_user_ready(user_id):
    users = load_users()
    user = users.get(str(user_id))
    return user and user.get("completed")
