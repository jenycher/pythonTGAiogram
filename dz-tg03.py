#1. Создайте новую базу данных school_data.db. В этой базе данных создайте таблицу
# students с колонками: id (INTEGER, PRIMARY KEY, AUTOINCREMENT) name (TEXT)
# age (INTEGER) grade (TEXT)
#2. Создайте Телеграм-бота, который запрашивает у пользователя имя, возраст и класс (grade),
# в котором он учится. Сделайте так чтоб бот сохранял введенные данные в таблицу students
# базы данных school_data.db.

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import logging
from config import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Определяем состояния для конечного автомата
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Инициализируем базу данных
init_db()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    logging.info("Received /start command")
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

# Обработчик для получения имени
@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    logging.info(f"Received name: {message.text}")
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

# Обработчик для получения возраста
@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    logging.info(f"Received age: {message.text}")
    await state.update_data(age=message.text)
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

# Обработчик для получения класса
@dp.message(Form.grade)
async def process_grade(message: Message, state: FSMContext):
    logging.info(f"Received grade: {message.text}")
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    # Сохранение данных в базу данных
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)
    ''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    logging.info(f"Inserted student data into database: {user_data}")

    await message.answer("Спасибо, ваши данные сохранены!")
    await state.clear()


# Обработчик команды /list
@dp.message(Command(commands=['list']))
async def list_students(message: Message):
    logging.info("Received /list command")

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    rows = cur.fetchall()
    conn.close()

    if rows:
        response = "Список студентов:\n\n"
        for row in rows:
            response += f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}, Класс: {row[3]}\n"
    else:
        response = "В базе данных пока нет студентов."

    await message.answer(response)

# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
