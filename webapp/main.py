from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command
import asyncio

TOKEN = "7810642321:AAGxqRFwFBqRS0hBR9yseX5UpguRKu4sh8k"
WEB_APP_URL = "https://d976fd7d11c3.ngrok-free.app"  # <-- Сюда вставь ссылку Ngrok

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    web_app_button = KeyboardButton(
        text="🛒 Открыть магазин", web_app=WebAppInfo(url=WEB_APP_URL)
    )
    keyboard = ReplyKeyboardMarkup(keyboard=[[web_app_button]], resize_keyboard=True)
    return keyboard

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Нажми на кнопку, чтобы открыть магазин:", reply_markup=get_main_keyboard())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
