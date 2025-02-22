import random
from database import get_players, save_roles, get_role
from telegram.error import Unauthorized


def send_safe_message(bot, user_id, text):
    try:
        bot.send_message(user_id, text)
    except Unauthorized:
        print(f"⚠️ Bot foydalanuvchi {user_id} bilan aloqa qila olmaydi! U botni bloklagan bo‘lishi mumkin.")

def assign_roles(players):
    if len(players) < 3:
        raise ValueError("O'yinni boshlash uchun kamida 3 ta o'yinchi kerak!")

    roles = ["Mafiya", "Sherif", "Doktor"] + ["Tinch aholi"] * (len(players) - 3)
    random.shuffle(roles)

    assigned = []
    for i, player in enumerate(players):
        user_id, username = player[:2]
        role = roles[i]
        assigned.append((user_id, username, role))

    save_roles([(user_id, role) for user_id, _, role in assigned])
    print("🔹 Belgilangan rollar:", assigned)

    return assigned



def start_night(chat_id, context):
    players = get_players(chat_id)

    mafias = [p for p in players if get_role(p[0]) == "Mafiya"]
    for mafia in mafias:
        send_safe_message(context.bot, mafia[0], "🌃 Kechasi bo‘ldi. Kimni o‘ldirishni tanlang.")

    doctors = [p for p in players if get_role(p[0]) == "Doktor"]
    for doctor in doctors:
        send_safe_message(context.bot, doctor[0], "🩺 Siz doktorsiz. Kimni davolashni tanlang.")

    sherifs = [p for p in players if get_role(p[0]) == "Sherif"]
    for sherif in sherifs:
        send_safe_message(context.bot, sherif[0], "🔍 Siz sherifsiz. Kimni tekshirishni tanlang.")
