from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbackfactory import CallbackQuestionFactory


def admin_message_client(client_id, client_name):
    builder = InlineKeyboardBuilder()
    builder.button(text="Откликнуться", callback_data=CallbackQuestionFactory(client_id=client_id, client_name=client_name))

    return builder.as_markup()
