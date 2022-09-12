from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from callbackfactory import CallbackAnswerFactory


def admin_panel():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Рассылка", callback_data="1"),
        InlineKeyboardButton(text="Информация\nо пользователе", callback_data="2")
    )
    builder.row(InlineKeyboardButton(text="Блокировать пользователя", callback_data="3"))

    return builder.as_markup()

def admin_answer(client_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Ответить", callback_data=CallbackAnswerFactory(client_id=client_id))

    return builder.as_markup()
