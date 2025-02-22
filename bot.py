from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from handlers import start_game, join_callback,start

TOKEN = "6494372838:AAGbqZDk1Mu7I0QJUVeezO9l2zV65gfzCHA"

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(join_callback, pattern="join"))
dp.add_handler(CallbackQueryHandler(start_game, pattern="start_game"))

print("✅ Bot ishga tushdi!")
updater.start_polling()
updater.idle()






