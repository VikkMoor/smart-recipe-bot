import base64
import json
import re

from config import client


def extract_json(text: str):
    """
    Извлекает JSON из ответа модели
    """

    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("JSON not found")

    return json.loads(match.group())


def extract_ingredients_from_image(image_bytes: bytes):
    """
    Анализирует изображение продуктов или чека
    и возвращает список ингредиентов
    """

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    data_url = f"data:image/jpeg;base64,{base64_image}"

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """
Ты кулинарный ассистент.

Проанализируй изображение.

Если на изображении:
- продукты
- чек
- ингредиенты
- еда

Ты кулинарный ассистент.

Проанализируй изображение.

Если это:
- чек
- продукты
- блюдо
- ингредиенты

то выдели ТОЛЬКО основные продукты и ингредиенты.

Правила:
- убирай бренды
- убирай проценты жирности
- убирай лишние описания
- приводи слова к обычному виду

Примеры:
"Молоко Сибирская Милена 2.5%" -> "молоко"
"Сыр Гауда 48%" -> "сыр"
"Макаронные изделия Гра..." -> "макароны"

Верни ТОЛЬКО JSON:

{
  "ingredients": [
    "string"
  ]
}

Никакого дополнительного текста.

Верни ТОЛЬКО JSON:

{
  "ingredients": [
    "string"
  ]
}

Никакого дополнительного текста.
"""
                    },
                    {
                        "type": "input_image",
                        "image_url": data_url
                    }
                ]
            }
        ]
    )

    text = response.output_text

    try:
        data = extract_json(text)

        return data.get("ingredients", [])

    except Exception:
        return []