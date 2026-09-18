import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Render'dagi Environment Variables bo'limidan kalitlarni o'qish
BOT_TOKEN = "8588322130:AAF_NBzbiLj0Jr79YGhLMLSDckZeyqvwPyw"
GEMINI_API_KEY = "AQ.Ab8RN6LoJWo-h9RJcHc-W7loshL5KAxbG2zf-zi8EsHz5x-7GQ"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN ko'rsatilmadi!")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY ko'rsatilmadi!")

# Bot va Gemini mijozini yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men Telegram ichidagi Oson AI botiman. Xohlagan savolingizni yuboring!"
    )


@dp.message()
async def ai_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer(f"Xatolik yuz berdi: {e}")


async def main():
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())