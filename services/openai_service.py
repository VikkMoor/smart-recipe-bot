import base64
import json
import re

from config import client


def extract_json(text: str):

    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("JSON not found")

    return json.loads(match.group())


def extract_ingredients_from_image(image_bytes: bytes):

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

На изображении могут быть:
- продукты
- ингредиенты
- готовая еда
- чек
- упаковки продуктов
- содержимое холодильника

Определи, какие продукты или ингредиенты присутствуют на изображении.

Верни ТОЛЬКО JSON:

{
  "ingredients": [
    "string"
  ]
}

Правила:
- Используй только продукты питания
- Не добавляй предметы, которые не являются едой
- Не придумывай ингредиенты
- Названия делай короткими и понятными
- Без текста вне JSON
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