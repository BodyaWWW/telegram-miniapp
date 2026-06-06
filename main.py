from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command
import asyncio

TOKEN = "7810642321:AAGxqRFwFBqRS0hBR9yseX5UpguRKu4sh8k"
WEB_APP_URL = "https://telegram-miniapp-2-pimo.onrender.com"  # <-- Сюда вставь ссылку Ngrok

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


ADMIN_ID = 617454203


@dp.message()
async def handle_all_messages(message: types.Message):
    # 1. ЯКЩО ПИШЕ АДМІН (Відповідь клієнту через Reply)
    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        try:
            # Витягуємо ID клієнта з тексту, який ми самі додали нижче
            text = message.reply_to_message.text
            if "Клієнт (ID: " in text:
                client_id = text.split("Клієнт (ID: ")[1].split(")")[0]
                await bot.send_message(client_id, f"👤 Відповідь менеджера:\n{message.text}")
                await message.answer("✅ Відправлено клієнту")
            else:
                await message.answer("❌ Це повідомлення не містить ID клієнта.")
        except Exception as e:
            await message.answer(f"❌ Помилка: {e}")

    # 2. ЯКЩО ПИШЕ КЛІЄНТ
    elif message.from_user.id != ADMIN_ID:
        # Пересилаємо повідомлення адміну
        await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        # Додаємо текст з ID, щоб ви могли зробити Reply
        await bot.send_message(
            ADMIN_ID,
            f"👤 Клієнт (ID: {message.from_user.id}) пише:\n{message.text}"
        )
if __name__ == "__main__":
    asyncio.run(main())
