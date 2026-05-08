from telegram import Update
from telegram.ext import ContextTypes

from services.openai_service import extract_ingredients_from_image
from logger import log_info, log_error
from services.recipe_service import generate_recipe


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        log_info("FILE RECEIVED")

        message = update.message

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document:
            file_id = message.document.file_id
        else:
            log_error("Unknown file type")
            await update.message.reply_text("Не удалось прочитать файл")
            return

        file = await context.bot.get_file(file_id)
        image_bytes = await file.download_as_bytearray()

        log_info(f"File downloaded: {file_id}")

        ingredients = extract_ingredients_from_image(image_bytes)
        recipe = generate_recipe(ingredients)

        log_info(f"Ingredients: {ingredients}")

        steps = "\n".join(
            [f"{i + 1}. {step}" for i, step in enumerate(recipe["steps"])]
        )

        message_text = f"""
        🍽 {recipe["title"]}

        ⏱ Время: {recipe["time"]}

        👨‍🍳 Шаги:

        {steps}
        """

        await update.message.reply_text(message_text)

        log_info("Success processing image")

    except Exception as e:
        log_error(f"ERROR in handle_photo: {str(e)}")
        await update.message.reply_text("Ошибка обработки изображения")