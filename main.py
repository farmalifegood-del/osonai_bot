import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8588322130:AAHiAxJNOscxuS-bA3EnYfCgO2lK3SAAUaw"
GEMINI_API_KEY = "AQ.Ab8RN6LAqQVv0WW7OMmEd8LFZejgdB7aIYB4vx3rJ_JBL_jLSA"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salom! Men Telegram ichidagi Oson AI botiman. Xohlagan savolingizni yuboring!")

@dp.message()
async def ai_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        # Xatolikning aniq matnini Telegram'ga yuboradi
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
