from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from text import text_contact, text_settings, text_contacts, text_number_phone, text_request, text_complete_contact

def client_start():
    button_phone = [[KeyboardButton(text=text_number_phone(), request_contact=True)]]

    return ReplyKeyboardMarkup(keyboard=button_phone, resize_keyboard=True)

def client_menu():
    menu = ReplyKeyboardBuilder()
    menu.row(KeyboardButton(text=text_request()), KeyboardButton(text=text_contact()))
    menu.row(KeyboardButton(text=text_settings()))
    menu.row(KeyboardButton(text=text_contacts()))

    return menu.as_markup(resize_keyboard=True, one_time_keyboard=True)

def client_contact():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=text_complete_contact()))

    return builder.as_markup(resize_keyboard=True)
