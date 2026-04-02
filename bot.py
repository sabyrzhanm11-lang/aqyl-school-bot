from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

TOKEN = "8287822576:AAGygu1q6r3MJk__ZQAmDQAwZBoItw2zja0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРА ---
def main_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Записаться")],
            [
                KeyboardButton(text="ℹ️ О курсах"),
                KeyboardButton(text="📞 Контакты")
            ]
        ],
        resize_keyboard=True
    )
    return kb


# --- СТАРТ ---
@dp.message(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Я помогу записать ребёнка на обучение.\n\n"
        "Выберите нужный пункт ниже 👇",
        reply_markup=main_keyboard()
    )


# --- ПОЛУЧИТЬ ID (ВАЖНО!) ---
@dp.message()
async def get_id(message: types.Message):
    await message.answer(f"ID: {message.chat.id}")


# --- ЗАПУСК ---
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
