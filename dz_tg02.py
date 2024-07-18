import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator

# Укажите ваш токен Telegram Bot API
from config import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов классов Bot и Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()

# Создание папки для изображений, если её ещё нет
if not os.path.exists('img'):
    os.makedirs('img')

# Хэндлер на команду /start
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Я ваш помощник.')

# Хэндлер на команду /help
@dp.message(Command(commands=["help"]))
async def help(message: Message):
    await message.answer(
        "Я могу помочь вам с несколькими задачами:\n"
        "1. Отправьте мне фото, и я сохраню его.\n"
        "2. Отправьте мне текст, и я переведу его на английский язык.\n"
        "3. Используйте команду /voice, чтобы я отправил вам голосовое сообщение.\n"
        "4. Команды /start и /help для информации обо мне."
    )

# Хэндлер для сохранения фотографий
@dp.message(F.photo)
async def save_photo(message: Message):
    try:
        # Уведомляем пользователя, что фото загружается
        await bot.send_chat_action(message.chat.id, 'upload_photo')

        # Получаем последнее фото (самого высокого качества)
        photo = message.photo[-1]

        # Определяем путь сохранения
        photo_path = f'img/{photo.file_id}.jpg'

        # Сохраняем фото
        await bot.download(photo, destination=photo_path)
        await message.answer("Фото успешно сохранено!")
    except Exception as e:
        logging.error(f"Ошибка при сохранении фото: {e}")
        await message.answer("Не удалось сохранить фото. Пожалуйста, попробуйте снова.")

# Хэндлер для отправки голосового сообщения
@dp.message(Command(commands=['voice']))
async def send_voice(message: Message):
    try:
        # Уведомляем пользователя, что отправляется голосовое сообщение
        await bot.send_chat_action(message.chat.id, 'record_voice')

        voice = FSInputFile("sample.ogg")
        await bot.send_voice(message.chat.id, voice)
    except Exception as e:
        logging.error(f"Ошибка при отправке голосового сообщения: {e}")
        await message.answer("Не удалось отправить голосовое сообщение. Проверьте наличие файла и попробуйте снова.")

# Хэндлер для перевода текста на английский
@dp.message(F.text)
async def translate_text(message: Message):
    text = message.text.strip()

    # Убедитесь, что сообщение не является командой
    if text.startswith('/'):
        return

    try:
        # Перевод текста на английский с использованием googletrans
        translated = translator.translate(text, dest='en')
        translated_text = translated.text
        await message.answer(f"Перевод: {translated_text}")
    except Exception as e:
        logging.error(f"Ошибка при переводе текста: {e}")
        await message.answer("Ошибка при переводе текста. Пожалуйста, попробуйте снова.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
