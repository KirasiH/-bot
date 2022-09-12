from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def leave_a_request_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📛Оставить заявку", callback_data="1"),
        InlineKeyboardButton(text="🔅Поделиться\n предложением", callback_data="2")
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="3"))

    return builder.as_markup()


def leave_a_request_complaint():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Пропустить", callback_data="1"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="2"))

    return builder.as_markup()

def leave_a_request_finally_complain_suggestion():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад", callback_data="2"))

    return builder.as_markup()

def settings_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⚒Поменять имя", callback_data="1"),
        InlineKeyboardButton(text="⚒Сменить номер", callback_data="2")
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="3"))

    return builder.as_markup()

def contact_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📞Перезвоните мне", callback_data="1")
    )
    builder.row(
        InlineKeyboardButton(text="📞Задать вопрос", callback_data="2")
    )
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data="3")
    )

    return builder.as_markup()
