from telegram.ext import ApplicationBuilder, MessageHandler, filters

from config import BOT_TOKEN
from handlers.text_handler import handle_message
from handlers.image_handler import handle_photo
from handlers.document_handler import handle_document

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Text messages
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

# Photos
app.add_handler(
    MessageHandler(filters.PHOTO, handle_photo)
)

# Documents
app.add_handler(
    MessageHandler(filters.Document.IMAGE, handle_document)
)

print("Bot is running...")
app.run_polling()