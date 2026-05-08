import json
import re

from config import client


def extract_json(text: str):

    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("JSON not found")

    return json.loads(match.group())


def generate_recipe(ingredients: list[str]):

    ingredients_text = ", ".join(ingredients)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Ты кулинарный ассистент.

У пользователя есть ингредиенты:

{ingredients_text}

Предложи ОДИН простой рецепт.

Верни ТОЛЬКО JSON:

{{
  "title": "string",
  "time": "string",
  "steps": [
    "string"
  ]
}}

Без дополнительного текста.
"""
    )

    text = response.output_text

    return extract_json(text)