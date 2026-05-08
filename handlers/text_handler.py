from telegram import Update
from telegram.ext import ContextTypes

from config import client
from logger import log_info, log_error
from services.recipe_service import (
    generate_recipe,
    generate_dish_image_prompt,
)


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    try:
        user_text = update.message.text

        log_info(f"TEXT RECEIVED: {user_text}")

        # Превращаем текст в список ингредиентов
        ingredients = [
            ingredient.strip()
            for ingredient in user_text.split(",")
            if ingredient.strip()
        ]

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

        # Всё, что есть
        available_ingredients = "\n".join(
            [f"• {ingredient}" for ingredient in ingredients]
        )

        # Используемые ингредиенты
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

        await update.message.reply_text(message_text)

        # Генерация картинки
        image_prompt = generate_dish_image_prompt(recipe)

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024",
        )

        image_base64 = image_response.data[0].b64_json

        import base64

        image_bytes = base64.b64decode(image_base64)

        await update.message.reply_photo(photo=image_bytes)

        log_info("Text recipe success")

    except Exception as e:
        log_error(f"TEXT HANDLER ERROR: {str(e)}")

        await update.message.reply_text(
            "Ошибка обработки текста"
        )