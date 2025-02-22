from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import Update
import telegram.error
from database import add_player, get_players
from game import assign_roles, start_night
from config import TOKEN

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    keyboard = [[InlineKeyboardButton("➕ O‘yinga qo‘shilish", callback_data="join_game")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "🎭 Mafia Baku o‘yiniga xush kelibsiz!\n\n🔹 O‘yin boshlanishi uchun kamida 4 ta o‘yinchi kerak.\n\n👇 O‘yinga qo‘shilish uchun pastdagi tugmani bosing.",
        reply_markup=reply_markup
    )

def join_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    chat_id = query.message.chat.id

    add_player(user.id, user.username, chat_id)
    query.answer("Siz o‘yinga qo‘shildingiz! ⏳ Kuting...")

    players = get_players(chat_id)
    player_list = "\n".join([f"👤 {p[1]}" for p in players])

    keyboard = [[InlineKeyboardButton("🎬 O‘yinni boshlash", callback_data="start_game")]] if len(players) >= 4 else []
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

    try:
        query.message.edit_text(
            f"🎭 O‘yin ishtirokchilari:\n{player_list}",
            reply_markup=reply_markup
        )
    except telegram.error.BadRequest:
        pass

def start_game(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    players = get_players(chat_id)

    if len(players) < 4:
        query.answer("O‘yin boshlash uchun kamida 4 ishtirokchi kerak! 🚫")
        return

    roles = assign_roles(players)
    for user_id, username, role in roles:

        try:
            context.bot.send_message(chat_id=user_id, text=f"🎭 Sizning rolingiz: {role}")
        except telegram.error.Unauthorized:
            print(f"⚠️ Bot foydalanuvchi {username} ({user_id}) tomonidan bloklangan!")
            continue

    query.message.edit_text(" O‘yin boshlandi! Kechasi bo‘ldi🌃...")
    start_night(chat_id, context)

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(join_callback, pattern="join_game"))
dp.add_handler(CallbackQueryHandler(start_game, pattern="start_game"))

print("✅ Bot ishga tushdi...")

updater.start_polling()
updater.idle()
