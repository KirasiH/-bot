from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text

from keyboards.client.inlinekeyboard import contact_menu
from keyboards.client.keyboard import client_menu
from keyboards.group.inlinekeyboard import admin_message_client

from databot import databot

from FSM import FSMClientStart

from text import text_contact, text_complete_contact


router = Router()
router.message.filter(F.chat.type.in_({"private"}))


async def contact(message: types.Message, state: FSMContext):

    await state.set_state(FSMClientStart.contact)
    await message.answer("Выберите способ связи из списка: ", reply_markup=contact_menu())


async def contact_back(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.contact)
    await event.message.delete()


async def contact_question(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.contact_question)
    await event.message.edit_text("Задайте вопрос!")


async def question(message: types.Message, state: FSMContext, bot: Bot):

    await state.set_state(FSMClientStart.admin_client)

    await bot.send_message(
        databot.group_admin_id,
        text=f"Сообщение от: @{message.from_user.username}\n"
             f"{message.text}",
        reply_markup=admin_message_client(message.from_user.id, message.from_user.username)
    )

    await message.answer("Ждите ответ!")


async def contact_phone(event: types.CallbackQuery, state: FSMContext, bot: Bot):

    await state.set_state(FSMClientStart.menu)

    await bot.send_message(
        databot.group_admin_id,
        text=f"Позвоните по номеру: {databot.user_phone(user_id=event.from_user.id)}"
    )

    await event.message.edit_text("Ждите звонка")


async def complete_contact(message: types.Message, state: FSMContext):

    await state.set_state(FSMClientStart.menu)
    await message.answer("Вы завершили диолог", reply_markup=client_menu())


def register_contact():
    router.message.register(contact, Text(text=text_contact()))
    router.callback_query.register(contact_back, Text(text="3"), state=FSMClientStart.contact)
    router.callback_query.register(contact_phone, Text(text="1"), state=FSMClientStart.contact)
    router.callback_query.register(contact_question, Text(text="2"), state=FSMClientStart.contact)
    router.message.register(question, state=FSMClientStart.contact_question)

    router.message.register(complete_contact, Text(text=text_complete_contact()), state=FSMClientStart.admin_client)

    return router
