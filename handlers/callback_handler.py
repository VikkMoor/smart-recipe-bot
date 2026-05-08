from telegram import Update
from telegram.ext import ContextTypes

from services.recipe_service import generate_recipe


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    ingredients = context.user_data.get("ingredients")

    if not ingredients:
        await query.edit_message_text("Нет сохранённых ингредиентов 😕")
        return

    if data == "another_recipe":
        recipe = generate_recipe(ingredients)

    elif data == "fast_recipe":
        recipe = generate_recipe(
            ingredients + ["быстро", "до 15 минут"]
        )

    else:
        await query.edit_message_text("Неизвестная команда")
        return

    steps = "\n".join(
        [f"{i + 1}. {step}" for i, step in enumerate(recipe["steps"])]
    )

    text = f"""
🍽 {recipe["title"]}

⏱ Время: {recipe["time"]}

👨‍🍳 Шаги:
{steps}
"""

    await query.message.reply_text(text)