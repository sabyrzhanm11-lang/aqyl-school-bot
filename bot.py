import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = "8723925776:AAFNsvYewVV7vesdM2clHcSP9Nun7iBgRAs"

bot = Bot(token=TOKEN)
dp = Dispatcher()


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Записаться")],
        [KeyboardButton(text="ℹ️ О курсах"), KeyboardButton(text="📞 Контакты")]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Я помогу записать ребёнка на обучение.\n\n"
        "Через этого бота можно:\n"
        "📚 оставить заявку на занятия\n"
        "ℹ️ узнать о курсах\n"
        "📞 получить контакты\n\n"
        "Выберите нужный пункт ниже 👇",
        reply_markup=main_keyboard
    )


@dp.message(F.text == "ℹ️ О курсах")
async def courses_handler(message: Message):
    await message.answer(
        "ℹ️ О курсах:\n\n"
        "• Подготовка к школе\n"
        "• Математика\n"
        "• Русский язык\n"
        "• Английский язык\n\n"
        "Формат: онлайн / офлайн\n"
        "Чтобы записаться, нажмите кнопку «📚 Записаться»."
    )


@dp.message(F.text == "📞 Контакты")
async def contacts_handler(message: Message):
    await message.answer(
        "📞 Контакты:\n\n"
        "Телефон: +7 XXX XXX XX XX\n"
        "WhatsApp: +7 XXX XXX XX XX\n"
        "Адрес: ваш адрес\n\n"
        "По всем вопросам можете написать или позвонить."
    )


@dp.message(F.text == "📚 Записаться")
async def signup_handler(message: Message):
    await message.answer(
        "Для записи отправьте одним сообщением:\n\n"
        "1. Имя ребёнка\n"
        "2. Возраст\n"
        "3. Класс\n"
        "4. Предмет\n"
        "5. Удобные дни\n"
        "6. Номер телефона родителя"
    )


@dp.message()
async def fallback_handler(message: Message):
    await message.answer(
        "Пожалуйста, выберите кнопку ниже 👇",
        reply_markup=main_keyboard
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
