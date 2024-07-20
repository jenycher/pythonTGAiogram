import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import TOKEN, OPENWEATHER_API_KEY
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import sqlite3
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def init_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    city TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    logging.info("Received /start command")
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    logging.info(f"Received name: {message.text}")
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    logging.info(f"Received age: {message.text}")
    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Form.city)

@dp.message(Form.city)
async def city(message: Message, state: FSMContext):
    logging.info(f"Received city: {message.text}")
    await state.update_data(city=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO users (name, age, city) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()

    logging.info(f"Inserted user data into database: {user_data}")

    timeout = aiohttp.ClientTimeout(total=10)  # Устанавливаем общий таймаут на 10 секунд
    async with aiohttp.ClientSession(timeout=timeout) as session:
        logging.info(f"Requesting weather for city: {user_data['city']}")
        try:
            async with session.get(f"http://api.openweathermap.org/data/2.5/weather?q={user_data['city']}&appid={OPENWEATHER_API_KEY}&units=metric") as response:
                logging.info(f"Received weather response: {response.status}")
                if response.status == 200:
                    weather_data = await response.json()
                    logging.info(f"Weather data: {weather_data}")
                    main = weather_data['main']
                    weather = weather_data['weather'][0]

                    temperature = main['temp']
                    humidity = main['humidity']
                    description = weather['description']

                    weather_report = (f"Город - {user_data['city']}\n"
                                      f"Температура - {temperature}\n"
                                      f"Влажность воздуха - {humidity}\n"
                                      f"Описание погоды - {description}")
                    await message.answer(weather_report)
                else:
                    logging.error("Failed to get weather data")
                    await message.answer("Не удалось получить данные о погоде")
        except asyncio.TimeoutError:
            logging.error("Request timed out")
            await message.answer("Запрос к серверу занял слишком много времени. Попробуйте снова позже.")
        await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
