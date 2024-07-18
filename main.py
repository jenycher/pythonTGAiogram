import asyncio
from aiogram import Bot, Dispatcher, F
#Bot и Dispatcher — это два компонента, которые есть в aiogram.
# Bot отвечает за взаимодействие с Telegram bot API, а
# Dispatcher управляет обработкой входящих сообщений и команд.
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp

import random

from config import TOKEN, OPENWEATHER_API_KEY

#Создадим объекты классов Bot и Dispatcher:
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text=="Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Искусственный интеллект - свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека (не следует путать с искусственным сознанием); наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ.")

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://koshka.top/uploads/posts/2021-12/1638584743_76-koshka-top-p-melkii-kotenok-87.jpg', 'https://kartinki.pics/uploads/posts/2022-02/1644872517_1-kartinkin-net-p-kotiki-kartinki-1.jpg', 'https://www.zastavki.com/pictures/originals/2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='это супер крутая картинка')
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
@dp.message(Command(commands=["help"]))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /photo \n Спроси его, Что такое ИИ? \n отправь ему фотку")

#Создадим декоратор для обработки команды /start:
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer("Приветики, я бот!")


@dp.message(Command(commands=["weather"]))
async def weather(message: Message):
    # URL для получения прогноза погоды
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={OPENWEATHER_API_KEY}&units=metric"
     #url=f"https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={OPENWEATHER_API_KEY}&units=metric"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            # Извлечение необходимых данных из ответа
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
                await message.answer("Не удалось получить данные о погоде. Пожалуйста, попробуйте позже.")


#Создадим асинхронную функцию main, которая будет запускать наш бот:
async def main():
    await dp.start_polling(bot)
    # программа будет отправлять запрос в Telegram, проверяя, есть ли входящие сообщения
    #и произошедшие события.Если события есть, программа их “отлавливает”.
    # В отсутствие событий функция продолжает отправлять запросы и ждет, когда событие
    #произойдет, чтобы с этим можно было начать работать.

if __name__ == "__main__":
    asyncio.run(main())

