import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN
import keyboards_dz as kb

# Инициализация бота
bot = Bot(token=TOKEN)

# Создание диспетчера
dp = Dispatcher()

# Регистрация обработчиков команд и кнопок
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Выберите опцию:", reply_markup=kb.main_menu())

@dp.message(F.text == "Привет")
async def greet(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')

@dp.message(F.text == "Пока")
async def farewell(message: Message):
    await message.answer(f'До свидания, {message.from_user.first_name}!')

@dp.message(Command(commands=["links"]))
async def send_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=kb.links_menu())

@dp.message(Command(commands=["dynamic"]))
async def show_dynamic(message: Message):
    await message.answer("Выберите опцию:", reply_markup=kb.dynamic_menu())

@dp.callback_query(F.data.in_(['show_more', 'option_1', 'option_2']))
async def handle_dynamic(callback: CallbackQuery):
    if callback.data == 'show_more':
        await callback.message.edit_text("Выберите опцию:", reply_markup=kb.dynamic_options())
    elif callback.data == 'option_1':
        await callback.message.answer("Вы выбрали Опцию 1")
    elif callback.data == 'option_2':
        await callback.message.answer("Вы выбрали Опцию 2")
    await callback.answer()  # Закрывает всплывающее уведомление

async def main():
    await dp.start_polling(bot)  # Передаем bot в start_polling

if __name__ == '__main__':
    asyncio.run(main())
