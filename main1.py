import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import aiohttp
import socket

from config import TOKEN, OPENWEATHER_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создадим объекты классов Bot и Dispatcher:
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text=="Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Искусственный интеллект - свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека (не следует путать с искусственным сознанием); наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ.")

@dp.message(Command('photo'))
async def photo(message: Message):
    list = [
        'https://koshka.top/uploads/posts/2021-12/1638584743_76-koshka-top-p-melkii-kotenok-87.jpg',
        'https://kartinki.pics/uploads/posts/2022-02/1644872517_1-kartinkin-net-p-kotiki-kartinki-1.jpg',
        'https://www.zastavki.com/pictures/originals/2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
    ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='это супер крутая картинка')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(Command(commands=["help"]))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /photo \n Спроси его, Что такое ИИ? \n отправь ему фотку\n /weather")

@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer("Приветики, я бот!")

@dp.message(Command(commands=["weather"]))
async def weather(message: Message):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"

    logging.info("Запрос к OpenWeatherMap: %s", url)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                logging.info("Ответ получен: статус %s", response.status)

                try:
                    data = await response.json()
                    logging.info("Данные ответа: %s", data)
                except Exception as json_error:
                    logging.error("Ошибка при чтении JSON: %s", json_error)
                    await message.answer("Ошибка при обработке данных о погоде.")
                    return

                if response.status == 200:
                    weather_description = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    humidity = data['main']['humidity']

                    await message.answer(
                        f"Погода в Москве:\n"
                        f"Описание: {weather_description.capitalize()}\n"
                        f"Температура: {temperature}°C\n"
                        f"Ощущается как: {feels_like}°C\n"
                        f"Влажность: {humidity}%"
                    )
                else:
                    logging.error("Ошибка в ответе от API: %s", data)
                    await message.answer("Не удалось получить данные о погоде. Пожалуйста, попробуйте позже.")
    except aiohttp.ClientConnectorError as e:
        logging.error("Ошибка соединения: %s", e)
        await message.answer("Не удаётся подключиться к сервису погоды. Проверьте ваше интернет-соединение.")
    except socket.gaierror as e:
        logging.error("Ошибка DNS: %s", e)
        await message.answer("Ошибка DNS. Проверьте настройки сети.")
    except Exception as e:
        logging.error("Ошибка при запросе погоды: %s", e)
        await message.answer("Ошибка при получении данных о погоде. Пожалуйста, попробуйте позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
