# 🍽 AI Recipe Telegram Bot
Multimodal AI Telegram bot that turns food photos, receipts, and text ingredients into recipes using OpenAI Vision and GPT models.

---

## ✨ Features
- 📸 Food image recognition (ingredients, dishes, fridge, receipts)
- 🧠 Vision-based ingredient extraction
- 🍳 Recipe generation from available ingredients
- 🌍 Multilingual support (RU / EN / ES)
- 🔘 Interactive buttons (another recipe / fast recipe)
- 🖼 AI-generated dish images
- 💬 Text input support (comma-separated ingredients)
- 🧾 Structured recipe output (title, time, steps)

---

## 🧩 Architecture
```text id="tree_1"
Telegram Update
↓
Handlers
├── text_handler
├── image_handler
├── callback_handler
↓
Services
├── OpenAI Vision (image → ingredients)
├── Recipe service (ingredients → recipe + image prompt)
↓
OpenAI API
↓
Formatted Telegram response
```

---

## 🚀 How it works
1. **User input**
   - Photo (food / fridge / ingredients / receipt)
   - Text (comma-separated ingredients)

2. **Input processing**
   - Vision model extracts ingredients from images
   - Text is parsed into a clean ingredient list

3. **Recipe generation**
   - GPT creates a structured recipe (title, time, steps)
   - Language is determined from Telegram user settings

4. **Response formatting**
   - Ingredients and recipe are formatted into a readable message
   - Interactive buttons are attached (another recipe / fast recipe)

5. **Image generation**
   - AI generates a dish image based on the recipe
   - Image is sent back to the user in Telegram
  
---

## ⚙️ Tech Stack

- Python 3.10+
- python-telegram-bot
- OpenAI GPT-4.1-mini
- OpenAI Vision API
- OpenAI Image Generation (gpt-image-1)
- dotenv
- logging

---

## 🚀 How to run

1. Clone repository
```bash
git clone <repo-url>
cd <project-name>
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Create `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```
4. Run bot
```bash
python bot.py
```

---

## 📸 Example usage

### Input:
- Photo of fridge / food / ingredients
- Text: `tomato, cheese, bread`

### Output:
- 🍽 Recipe title
- ⏱ Cooking time
- 🧾 Used ingredients
- 👨‍🍳 Step-by-step instructions
- 🖼 AI-generated dish image
- 🔘 Buttons: another recipe / fast recipe

---

## 📈Possible improvements
- Voice input (STT)
- Database storage (PostgreSQL)
- User profiles & history
- Dietary preferences
- Recipe ranking / feedback system

---

## 🧠 Status

MVP completed.

Multimodal AI assistant for cooking workflows:
- Vision + text understanding
- Recipe generation
- Image generation
- Multilingual support
- Interactive Telegram UX
