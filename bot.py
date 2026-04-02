import asyncio
import json
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8723925776:AAGRsBDPMBSpZtrnjl13OyXX-ibhWtb8_mo"
DATA_FILE = "applications.json"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    child_name = State()
    age = State()
    grade = State()
    subject = State()
    goal = State()
    days = State()
    duration = State()
    format = State()
    parent_phone = State()
    comment = State()


def load_applications():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_application(application):
    applications = load_applications()
    applications.append(application)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(applications, file, ensure_ascii=False, indent=4)


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Записаться")],
            [KeyboardButton(text="ℹ️ О курсах"), KeyboardButton(text="📞 Контакты")]
        ],
        resize_keyboard=True
    )


def subject_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Математика"), KeyboardButton(text="📘 Русский язык")],
            [KeyboardButton(text="🌍 Английский язык"), KeyboardButton(text="🧠 Подготовка к школе")],
            [KeyboardButton(text="✍️ Другое")]
        ],
        resize_keyboard=True
    )


def days_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Пн, Ср, Пт")],
            [KeyboardButton(text="📅 Вт, Чт, Сб")],
            [KeyboardButton(text="📅 Индивидуально")]
        ],
        resize_keyboard=True
    )


def duration_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏱ 1 час")],
            [KeyboardButton(text="⏱ 2 часа")]
        ],
        resize_keyboard=True
    )


def format_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💻 Онлайн"), KeyboardButton(text="🏫 Офлайн")],
            [KeyboardButton(text="🔄 Без разницы")]
        ],
        resize_keyboard=True
    )


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Я помогу записать ребёнка на обучение.\n\n"
        "Через этого бота можно:\n"
        "📚 оставить заявку на занятия\n"
        "ℹ️ узнать о курсах\n"
        "📞 получить контакты\n\n"
        "Выберите нужный пункт ниже 👇",
        reply_markup=main_keyboard()
    )


@dp.message(F.text == "ℹ️ О курсах")
async def about_courses(message: types.Message):
    await message.answer(
        "📚 Наши занятия подходят для детей до 6 класса.\n\n"
        "Направления:\n"
        "• математика\n"
        "• русский язык\n"
        "• английский язык\n"
        "• подготовка к школе\n\n"
        "Формат:\n"
        "• онлайн\n"
        "• офлайн\n\n"
        "Чтобы оставить заявку, нажмите:\n"
        "📚 Записаться",
        reply_markup=main_keyboard()
    )


@dp.message(F.text == "📞 Контакты")
async def contacts(message: types.Message):
    await message.answer(
        "📞 Контакты:\n\n"
        "Напишите сюда свои контакты.\n\n"
        "Пример:\n"
        "Instagram: @your_account\n"
        "WhatsApp: +7 700 000 00 00",
        reply_markup=main_keyboard()
    )


@dp.message(F.text == "📚 Записаться")
async def start_form(message: types.Message, state: FSMContext):
    await state.set_state(Form.child_name)
    await message.answer("1️⃣ Напишите имя ребёнка:")


@dp.message(Form.child_name)
async def get_child_name(message: types.Message, state: FSMContext):
    await state.update_data(child_name=message.text)
    await state.set_state(Form.age)
    await message.answer("2️⃣ Сколько лет ребёнку?")


@dp.message(Form.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Form.grade)
    await message.answer("3️⃣ В каком классе учится ребёнок?")


@dp.message(Form.grade)
async def get_grade(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await state.set_state(Form.subject)
    await message.answer(
        "4️⃣ Какой предмет нужен?",
        reply_markup=subject_keyboard()
    )


@dp.message(Form.subject)
async def get_subject(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(Form.goal)
    await message.answer(
        "5️⃣ Какая цель занятий?\n\n"
        "Например:\n"
        "• подтянуть оценки\n"
        "• подготовка к контрольной\n"
        "• подготовка к школе\n"
        "• понять тему"
    )


@dp.message(Form.goal)
async def get_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await state.set_state(Form.days)
    await message.answer(
        "6️⃣ В какие дни удобно заниматься?",
        reply_markup=days_keyboard()
    )


@dp.message(Form.days)
async def get_days(message: types.Message, state: FSMContext):
    await state.update_data(days=message.text)
    await state.set_state(Form.duration)
    await message.answer(
        "7️⃣ Сколько по времени должно длиться занятие?",
        reply_markup=duration_keyboard()
    )


@dp.message(Form.duration)
async def get_duration(message: types.Message, state: FSMContext):
    await state.update_data(duration=message.text)
    await state.set_state(Form.format)
    await message.answer(
        "8️⃣ Какой формат вам подходит?",
        reply_markup=format_keyboard()
    )


@dp.message(Form.format)
async def get_format(message: types.Message, state: FSMContext):
    await state.update_data(format=message.text)
    await state.set_state(Form.parent_phone)
    await message.answer(
        "9️⃣ Напишите номер телефона родителя для связи.\n\n"
        "Пример:\n"
        "+7 700 000 00 00"
    )


@dp.message(Form.parent_phone)
async def get_parent_phone(message: types.Message, state: FSMContext):
    await state.update_data(parent_phone=message.text)
    await state.set_state(Form.comment)
    await message.answer(
        "🔟 Есть ли дополнительный комментарий?\n\n"
        "Если комментария нет, напишите:\n"
        "Нет"
    )


@dp.message(Form.comment)
async def get_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)

    data = await state.get_data()

    application = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "telegram_id": message.from_user.id,
        "telegram_name": message.from_user.full_name,
        "child_name": data["child_name"],
        "age": data["age"],
        "grade": data["grade"],
        "subject": data["subject"],
        "goal": data["goal"],
        "days": data["days"],
        "duration": data["duration"],
        "format": data["format"],
        "parent_phone": data["parent_phone"],
        "comment": data["comment"]
    }

    save_application(application)

    await state.clear()
    await message.answer(
        "✅ Заявка сохранена!\n\n"
        f"👦 Имя ребёнка: {data['child_name']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"🏫 Класс: {data['grade']}\n"
        f"📚 Предмет: {data['subject']}\n"
        f"🎯 Цель: {data['goal']}\n"
        f"📅 Дни: {data['days']}\n"
        f"⏱ Длительность: {data['duration']}\n"
        f"💻 Формат: {data['format']}\n"
        f"📞 Телефон: {data['parent_phone']}\n"
        f"📝 Комментарий: {data['comment']}\n\n"
        "Мы скоро с вами свяжемся 🤝",
        reply_markup=main_keyboard()
    )


@dp.message()
async def fallback(message: types.Message):
    await message.answer(
        "Пожалуйста, выберите кнопку ниже 👇",
        reply_markup=main_keyboard()
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())