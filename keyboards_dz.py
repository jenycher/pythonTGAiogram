from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Основное меню с кнопками "Привет" и "Пока"
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
        ],
        resize_keyboard=True
    )

# Меню с инлайн-кнопками и URL-ссылками
def links_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Новости", url='https://news.ycombinator.com/')],
            [InlineKeyboardButton(text="Музыка", url='https://www.spotify.com/')],
            [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/')]
        ]
    )

# Динамическое меню с кнопкой "Показать больше"
def dynamic_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Показать больше", callback_data='show_more')]
        ]
    )

# Динамическое меню с кнопками "Опция 1" и "Опция 2"
def dynamic_options():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Опция 1", callback_data='option_1')],
            [InlineKeyboardButton(text="Опция 2", callback_data='option_2')]
        ]
    )
