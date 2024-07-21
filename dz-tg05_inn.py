# получении организации по ИНН
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import aiohttp
import logging
import json
from config import TOKEN, INN_API_KEY

# Установка логирования
logging.basicConfig(level=logging.INFO)


# URL для запроса к Dadata
DADATA_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Функция для запроса информации по ИНН
async def get_company_name_by_inn(inn: str):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {INN_API_KEY}"
    }
    data = {
        "query": inn,
        "branch_type": "MAIN"  # Получить только головную организацию
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(DADATA_URL, headers=headers, data=json.dumps(data)) as response:
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


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Введите ИНН, чтобы получить название организации.")


# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    inn = message.text.strip()
    if inn.isdigit() and len(inn) in {10, 12}:
        await message.answer("Ищу информацию, пожалуйста подождите...")
        company_name = await get_company_name_by_inn(inn)
        await message.answer(company_name)
    else:
        await message.answer("Пожалуйста, введите корректный ИНН (10 или 12 цифр).")


# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
