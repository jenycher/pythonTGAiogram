import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
import aiohttp
import logging
import json
from config import TOKEN, DADATA_API_KEY

# Установка логирования
logging.basicConfig(level=logging.INFO)




# URL для запросов к Dadata
DADATA_PARTY_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
DADATA_BANK_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/bank"

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем клавиатуру с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Определить компанию по ИНН")],
        [KeyboardButton(text="Найти банк по БИК")]
    ],
    resize_keyboard=True
)


# Функция для запроса информации по ИНН
async def get_company_name_by_inn(inn: str):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {
        "query": inn,
        "branch_type": "MAIN"  # Получить только головную организацию
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(DADATA_PARTY_URL, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                response_data = await response.json()
                suggestions = response_data.get("suggestions", [])
                if suggestions:
                    # Возвращаем название первой найденной организации
                    return suggestions[0]["value"]
                else:
                    return "Организация с указанным ИНН не найдена."
            else:
                return "Ошибка при запросе данных. Проверьте правильность ИНН."


# Функция для запроса информации по БИК
async def get_bank_name_by_bik(bik: str):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {
        "query": bik
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(DADATA_BANK_URL, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                response_data = await response.json()
                suggestions = response_data.get("suggestions", [])
                if suggestions:
                    # Возвращаем название первого найденного банка
                    return suggestions[0]["value"]
                else:
                    return "Банк с указанным БИК не найден."
            else:
                return "Ошибка при запросе данных. Проверьте правильность БИК."


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Выберите, что вы хотите сделать:", reply_markup=keyboard)


# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    text = message.text.strip()
    if text == "Определить компанию по ИНН":
        await message.answer("Пожалуйста, введите ИНН.")
    elif text == "Найти банк по БИК":
        await message.answer("Пожалуйста, введите БИК.")
    elif text.isdigit():
        if len(text) in {10, 12}:  # Проверка на ИНН
            await message.answer("Ищу информацию о компании, пожалуйста подождите...")
            company_name = await get_company_name_by_inn(text)
            await message.answer(company_name)
        elif len(text) == 9:  # Проверка на БИК
            await message.answer("Ищу информацию о банке, пожалуйста подождите...")
            bank_name = await get_bank_name_by_bik(text)
            await message.answer(bank_name)
        else:
            await message.answer("Пожалуйста, введите корректный ИНН (10 или 12 цифр) или БИК (9 цифр).")
    else:
        await message.answer("Пожалуйста, выберите действие с помощью кнопок или введите корректные данные.")


# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
