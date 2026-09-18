import asyncio
import logging
import os
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8588322130:AAH9EVvD9gVRDo4Z54aq28cKl5OSZHMvGiQ"
# Укажите ваш personal access token ghp_... от GitHub:
GITHUB_TOKEN = "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" 

# Используем асинхронный клиент с явным переопределением httpx для обхода ошибок соединения
client = AsyncOpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN,
    http_client=httpx.AsyncClient(trust_env=False)
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
        response = await client.chat.completions.create(
            model="Claude-3.5-Sonnet",
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
    asyncio.create_task(dp.start_polling(bot))
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
