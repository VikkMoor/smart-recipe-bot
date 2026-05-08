from telegram import Update
from telegram.ext import ContextTypes

from config import client
from logger import log_info, log_error
from services.openai_service import extract_ingredients_from_image
from services.recipe_service import (
    generate_recipe,
    generate_dish_image_prompt,
)


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

            await update.message.reply_text(
                "Не удалось прочитать файл"
            )

            return

        file = await context.bot.get_file(file_id)

        image_bytes = await file.download_as_bytearray()

        log_info(f"File downloaded: {file_id}")

        # Извлечение ингредиентов
        ingredients = extract_ingredients_from_image(image_bytes)

        log_info(f"Ingredients: {ingredients}")

        # Генерация рецепта
        recipe = generate_recipe(ingredients)

        used_ingredients = recipe["used_ingredients"]

        # Форматирование шагов
        steps = "\n".join(
            [
                f"{i + 1}. {step}"
                for i, step in enumerate(recipe["steps"])
            ]
        )

        # Всё, что найдено на изображении
        available_ingredients = "\n".join(
            [f"• {ingredient}" for ingredient in ingredients]
        )

        # Только ингредиенты рецепта
        recipe_ingredients = "\n".join(
            [f"• {ingredient}" for ingredient in used_ingredients]
        )

        # Текст ответа
        message_text = f"""
🛍 У вас есть:
{available_ingredients}

🍽 {recipe["title"]}

⏱ Время: {recipe["time"]}

🧾 Для рецепта используются:
{recipe_ingredients}

👨‍🍳 Шаги:
{steps}
"""

        # Отправка текста
        await update.message.reply_text(message_text)

        # Генерация изображения блюда
        image_prompt = generate_dish_image_prompt(recipe)

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024",
        )

        image_base64 = image_response.data[0].b64_json

        import base64

        image_bytes = base64.b64decode(image_base64)

        # Отправка изображения
        await update.message.reply_photo(photo=image_bytes)

        log_info("Success processing image")

    except Exception as e:
        log_error(f"ERROR in handle_photo: {str(e)}")

        await update.message.reply_text(
            "Ошибка обработки изображения"
        )