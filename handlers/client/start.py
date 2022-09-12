from aiogram import types, Router, F
from aiogram.filters import CommandStart, ContentTypesFilter, ChatMemberUpdatedFilter, KICKED

from aiogram.fsm.context import FSMContext
from FSM import FSMClientStart

from handlers.client.datafilters import correct_name

from keyboards.client.keyboard import client_start, client_menu

from text import say_menu, say_start, say_correct_name, say_discorrect_name
from databot import databot


router = Router()
router.message.filter(F.chat.type.in_({"private"}))


async def command_start(message: types.Message, state: FSMContext):

    if databot.check_user(message.from_user.id):
        await state.set_state(FSMClientStart.menu)
        await message.answer(say_menu(), reply_markup=client_menu())

    else:
        await state.set_state(FSMClientStart.name)
        await message.answer(say_start())


async def name(message: types.Message, state: FSMContext):

    if await correct_name(message.text):
        await state.update_data(name=message.text)
        await state.set_state(FSMClientStart.number_phone)

        await message.answer(say_correct_name(), reply_markup=client_start())

    else:
        await message.answer(say_discorrect_name())


async def number_phone(message: types.Message, state: FSMContext):

    data = await state.update_data(number_phone=message.contact)

    await state.clear()
    await state.set_state(FSMClientStart.menu)

    databot.add_user(message.from_user.id, data['name'], data['number_phone'].phone_number, 0, 0)

    await message.answer(say_menu(), reply_markup=client_menu())


async def delete_user(event: types.ChatMemberUpdated):
    databot.delete_user(event.from_user.id)


def register_clientstart():
    router.message.register(command_start, CommandStart())
    router.message.register(name, state=FSMClientStart.name)
    router.message.register(number_phone, ContentTypesFilter(content_types=types.ContentType.CONTACT), state=FSMClientStart.number_phone)

    router.my_chat_member.register(delete_user, ChatMemberUpdatedFilter(member_status_changed=KICKED))

    return router
