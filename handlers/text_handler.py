from telegram import Update
from telegram.ext import ContextTypes


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отправь фото продуктов, блюда или чека 🍳"
    )