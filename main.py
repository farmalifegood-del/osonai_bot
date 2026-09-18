import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8588322130:AAH9EVvD9gVRDo4Z54aq28cKl5OSZHMvGiQ"
# GitHub'dan olgan ghp_... tokeningizni shu yerga joylang:
GITHUB_TOKEN = "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" 

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN,
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
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Barqaror ishlashi uchun gpt-4o-mini ishlatamiz
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer(f"Aniq xatolik: {str(e)[:300]}")

async def handle(request):
    return web.Response(text="OK")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print("Bot muvaffaqiyatli ishga tushdi!")
    
    # Polling funksiyasini to'g'ri ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
