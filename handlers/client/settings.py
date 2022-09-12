from aiogram import types, Router, F
from aiogram.filters import Text, ContentTypesFilter
from aiogram.fsm.context import FSMContext

from keyboards.client.inlinekeyboard import settings_menu
from keyboards.client.keyboard import client_menu, client_start

from handlers.client.datafilters import correct_name

from databot import databot
from filters.client.filters import ChatIsNotTextFilter

from FSM import FSMClientStart

from text import text_settings, say_settings, say_discorrect_name, say_settings_name, say_settings_update


router = Router()
router.message.filter(F.chat.type.in_({"private"}))
router.callback_query.filter(F.message.chat.type == "private")


async def settings(message: types.Message, state: FSMContext):

    await state.set_state(FSMClientStart.settings)
    await message.answer(say_settings(), reply_markup=settings_menu())


async def settings_back(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.menu)
    await event.message.delete()


async def settings_name(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.settings_name)
    await event.message.edit_text(say_settings_name())


async def settings_update_name(message: types.Message, state: FSMContext):

    if await correct_name(message.text):
        await state.set_state(FSMClientStart.menu)
        await message.answer(say_settings_update(), reply_markup=client_menu())

        databot.user_new_name_phone(message.from_user.id, name=message.text)

    else:
        await message.answer(say_discorrect_name())


async def settings_phone(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.setting_phone)
    await event.message.delete()
    await event.message.answer("Ваш номер телефона", reply_markup=client_start())


async def settings_update_phone(message: types.Message, state: FSMContext):

    await state.set_state(FSMClientStart.menu)
    await message.answer(say_settings_update(), reply_markup=client_menu())

    databot.user_new_name_phone(message.from_user.id, phone=message.contact.phone_number)


def register_settings():
    router.message.register(settings, ChatIsNotTextFilter(), Text(text=text_settings()), state=FSMClientStart.menu)
    router.callback_query.register(settings_back, Text(text="3"), state=FSMClientStart.settings)

    router.callback_query.register(settings_name, Text(text="1"), state=FSMClientStart.settings)
    router.message.register(settings_update_name, ChatIsNotTextFilter(), state=FSMClientStart.settings_name)

    router.callback_query.register(settings_phone, Text(text="2"), state=FSMClientStart.settings)
    router.message.register(settings_update_phone, ContentTypesFilter(content_types=types.ContentType.CONTACT), state=FSMClientStart.setting_phone)

    return router
