from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import client
from logger import log_info, log_error
from services.recipe_service import (
    generate_recipe,
    generate_dish_image_prompt,
)

import base64


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text

        language = update.effective_user.language_code or "ru"

        log_info(f"TEXT RECEIVED: {user_text}")

        ingredients = [
            i.strip()
            for i in user_text.split(",")
            if i.strip()
        ]

        recipe = generate_recipe(
            ingredients,
            language=language
        )

        context.user_data["ingredients"] = ingredients
        context.user_data["last_recipe"] = recipe

        used_ingredients = recipe["used_ingredients"]

        steps = "\n".join(
            [f"{i + 1}. {step}" for i, step in enumerate(recipe["steps"])]
        )

        available_ingredients = "\n".join(
            [f"• {i}" for i in ingredients]
        )

        recipe_ingredients = "\n".join(
            [f"• {i}" for i in used_ingredients]
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🍳 Другой рецепт",
                    callback_data="another_recipe"
                ),
                InlineKeyboardButton(
                    "⚡ Быстрый рецепт",
                    callback_data="fast_recipe"
                ),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

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

        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup
        )

        image_prompt = generate_dish_image_prompt(recipe)

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="auto",
        )

        image_base64 = image_response.data[0].b64_json

        image_bytes = base64.b64decode(image_base64)

        await update.message.reply_photo(photo=image_bytes)

        log_info("Text recipe success")

    except Exception as e:
        log_error(f"TEXT HANDLER ERROR: {str(e)}")

        await update.message.reply_text(
            "Ошибка обработки текста"
        )