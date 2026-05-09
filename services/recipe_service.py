import json
import re

from config import client


def extract_json(text: str):

    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("JSON not found")

    return json.loads(match.group())


def generate_recipe(
    ingredients: list[str],
    language: str = "ru"
):

    ingredients_text = ", ".join(ingredients)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Ты кулинарный ассистент.

Отвечай на языке: {language}

У пользователя есть ингредиенты:

{ingredients_text}

Предложи ОДИН простой рецепт.

Используй только часть ингредиентов,
которые действительно нужны для рецепта.

Верни ТОЛЬКО JSON:

{{
  "title": "string",
  "time": "string",
  "used_ingredients": [
    "string"
  ],
  "steps": [
    "string"
  ]
}}

Без дополнительного текста.
"""
    )

    text = response.output_text

    return extract_json(text)


def generate_dish_image_prompt(recipe: dict):

    return f"""
A realistic food photo of {recipe['title']}.
Professional food photography, soft natural lighting, high detail, appetizing presentation.
"""