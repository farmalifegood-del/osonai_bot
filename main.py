import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
from google import genai

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8588322130:AAHiAxJNOscxuS-bA3EnYfCgO2lK3SAAUaw"
GEMINI_API_KEY = "AQ.Ab8RN6LAqQVv0WW7OMmEd8LFZejgdB7aIYB4vx3rJ_JBL_jLSA"

# AQ... kaliti uchun Vertex AI rejimida ulanish
client = genai.Client(
    vertexai=True,
    project="483143579792",
    location="us-central1",
    api_key=GEMINI_API_KEY
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salom! Men Telegram ichidagi Oson AI botiman. Xohlagan savolingizni yuboring!")

@dp.message()
async def ai_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer(f"Aniq xatolik: {str(e)[:300]}")

async def handle(request):
    return web.Response(text="Bot ishlayapti!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
