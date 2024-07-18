import asyncio
import logging
import random

import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import aiohttp
from gtts import gTTS

from config import TOKEN, OPENWEATHER_API_KEY, GISMETEO_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создадим объекты классов Bot и Dispatcher:
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения состояния пользователя
user_states = {}

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Искусственный интеллект - свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека (не следует путать с искусственным сознанием); наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ.")

@dp.message(Command(commands=['photo']))
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
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(Command(commands=["help"]))
async def help(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды: \n /start \n /help \n /photo \n /video \n"
        "Спроси его, Что такое ИИ? \n отправь ему фотку\n /weather"
    )

@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}')

@dp.message(Command(commands=['video']))
async def video(message: Message):
    try:
        # Отправка индикации о загрузке
        await bot.send_chat_action(message.chat.id, 'upload_video')

        # Загрузка и отправка видео
        video = FSInputFile('video.mp4')
        await bot.send_video(message.chat.id, video)
    except Exception as e:
        logging.error(f"Ошибка при отправке видео: {e}")
        await message.answer("Не удалось отправить видео. Проверьте наличие файла и попробуйте снова.")

@dp.message(Command(commands=['audio']))
async def audio(message: Message):
    audio = FSInputFile('sound.mp3')
    await bot.send_video(message.chat.id, audio)

@dp.message(Command(commands=['training']))
async def training(message: Message):
   training_list = [
       "Тренировка 1: \n 1. Скручивания: 3 подхода по 15 повторений \n 2. Велосипед: 3 подхода по 20 повторений (каждая сторона) \n 3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2: \n 1. Подъемы ног: 3 подхода по 15 повторений \n 2. Русский твист: 3 подхода по 20 повторений (каждая сторона) \n 3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3: \n 1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений \n 2. Горизонтальные ножницы: 3 подхода по 20 повторений \n 3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   audio = FSInputFile("training.ogg")
   await bot.send_voice(chat_id=message.chat.id, voice=audio)
   os.remove("training.ogg")

@dp.message(Command(commands=['voice']))
async def voice(message: Message):
    try:
        await bot.send_chat_action(message.chat.id, 'record_voice')

        voice = FSInputFile("sample.ogg")
        await bot.send_voice(message.chat.id, voice)
    except Exception as e:
        logging.error(f"Ошибка при отправке голосового сообщения: {e}")
        await message.answer("Не удалось отправить голосовое сообщение. Проверьте наличие файла и попробуйте снова.")

@dp.message(Command(commands=['doc']))
async def doc(message: Message):
    doc = FSInputFile("деке.pdf")
    await bot.send_document(message.chat.id, doc)
@dp.message()
async def echo(message: Message):
    if message.text.lower() == 'test':
        await message.answer('Тестируем')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
