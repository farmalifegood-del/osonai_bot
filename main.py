import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
from groq import Groq

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8588322130:AAEMlT8OdWO1UeyKdPgAVzV2-wKyW6ndQME"
GROQ_API_KEY = "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" # gsk_ kalitingiz tursin

client = Groq(api_key=GROQ_API_KEY)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salom! Men Telegram ichidagi Oson AI botiman. Xohlagan savolingizni yuboring!")

@dp.message()
async def ai_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        await message.answer(response.choices[0].message.content)
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
