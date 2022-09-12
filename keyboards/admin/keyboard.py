from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


def admin_panel():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Рассылка"),
        KeyboardButton(text="Информация\nо пользователе")
    )
    builder.row(KeyboardButton(text="Блокировать\n пользователя"), KeyboardButton(text="Разблокировать\n пользователя"))

    return builder.as_markup(resize_keyboard=True)
