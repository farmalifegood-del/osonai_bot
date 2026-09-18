import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from google import genai

# Sizning token va API kalitlaringiz
BOT_TOKEN = "8588322130:AAF_NBzbiLjOJr79YGhLMLSDckZeyqvwPyw"
GEMINI_API_KEY = "AQ.Ab8RN6J-zvcveHsk4G5hm50aSsiT1sD0UuKu67k2OR3u62ZvIA"

# Bot va Gemini sozlamalari
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# /start buyrug'i uchun
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Salom! Men Telegram ichidagi Oson AI botiman. Xohlagan savolingizni yuboring!")

# Matnli xabarlarga javob berish
@dp.message(F.text)
async def gemini_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        # Yangilangan Gemini modeli: gemini-3.6-flash
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())