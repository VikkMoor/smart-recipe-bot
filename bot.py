from telegram.ext import ApplicationBuilder, MessageHandler, filters

from config import BOT_TOKEN
from handlers.text_handler import handle_message
from handlers.image_handler import handle_photo

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.Document.ALL, handle_photo))

print("Bot is running...")
app.run_polling()