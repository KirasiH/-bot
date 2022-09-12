from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F, Bot

from aiogram.filters import Text

from FSM import FSMClientStart

from keyboards.client.inlinekeyboard import leave_a_request_menu, leave_a_request_complaint, leave_a_request_finally_complain_suggestion
from keyboards.client.keyboard import client_menu

from filters.client.filters import ChatIsNotTextFilter
from filters.client.filters import ChatApplicationComplainFilter

from databot import databot

from text import text_request, say_request_complain1, say_request_complain2, say_request_complain3, say_request_complain3_text, say_leave_a_request


router = Router()
router.message.filter(F.chat.type.in_({"private"}))
router.callback_query.filter(F.message.chat.type == "private")


async def leave_a_request(message: types.Message, state: FSMContext):

    await message.answer(say_leave_a_request(), reply_markup=leave_a_request_menu())
    await state.set_state(FSMClientStart.application)


async def leave_a_request_back(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.menu)
    await event.message.delete()


async def leave_a_request_complaint1(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.complaint1)
    await event.message.edit_text(say_request_complain1(), reply_markup=leave_a_request_complaint(), parse_mode='html')


async def leave_a_request_complaint1_back(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.application)
    await event.message.edit_text(say_leave_a_request(), reply_markup=leave_a_request_menu())


async def leave_a_request_complaint1_text(messsage: types.Message, state: FSMContext):

    await state.set_state(FSMClientStart.complaint2)
    await state.update_data(complaint1_text=messsage.text)
    await messsage.answer(say_request_complain2(), reply_markup=leave_a_request_complaint(), parse_mode='html')


async def leave_a_request_complaint2(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.complaint2)
    await event.message.answer(say_request_complain2(), reply_markup=leave_a_request_complaint(), parse_mode='html')


async def leave_a_request_complaint2_back(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.complaint1)
    await event.message.edit_text(say_request_complain1(), reply_markup=leave_a_request_complaint())


async def leave_a_request_complaint2_media(message: types.Message, state: FSMContext):

    if message.content_type == "photo":
        await state.update_data(complaint2_photo=message.photo[-1].file_id)

    else:
        await state.update_data(complaint2_video=message.video.file_id)

    await state.set_state(FSMClientStart.complaint3)
    await message.answer(say_request_complain3(), reply_markup=leave_a_request_finally_complain_suggestion(), parse_mode='html')


async def leave_a_request_complaint3(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.complaint3)
    await event.message.answer(say_request_complain3(), reply_markup=leave_a_request_finally_complain_suggestion(), parse_mode='html')


async def leave_a_request_complaint3_back(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.complaint2)
    await event.message.answer(say_request_complain2(), reply_markup=leave_a_request_complaint(), parse_mode='html')


async def leave_a_request_complaint3_text(message: types.Message, state: FSMContext, bot: Bot):

    data = await state.update_data(text=message.text)
    await state.clear()
    await state.set_state(FSMClientStart.menu)

    text = say_request_complain3_text(message.from_user.username, databot.user_name(message.from_user.id), databot.user_phone(message.from_user.id), data)

    if databot.group_request_id != 1:
        if "complaint2_photo" in data:
            await bot.send_photo(
                databot.group_request_id,
                photo=data['complaint2_photo'],
                caption=text
            )

        elif "complaint2_video" in data:
            await bot.send_voice(
                databot.group_request_id,
                voice=data['complaint2_video'],
                caption=text
            )

        else:
            await bot.send_message(
                databot.group_request_id,
                text=text
            )

    await message.answer("✅Жалоба отправленна администрации. Спасибо за Ваше обращение", reply_markup=client_menu())


async def leave_a_suggestion(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.suggestion)
    await event.message.edit_text("Распишите Ваше предложение в подробностях: ", reply_markup=leave_a_request_finally_complain_suggestion())


async def leave_a_suggestion_back(event: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClientStart.application)
    await event.message.delete()


async def leave_a_suggestion_and_photo(message: types.Message, state: FSMContext, bot: Bot):

    await state.set_state(FSMClientStart.menu)
    await message.answer("Идея принята и передана администрации. Спасибо за Ваше обращение.", reply_markup=client_menu())

    if databot.group_suggestion_id != 1:
        await bot.send_message(
            databot.group_suggestion_id,
            text=f"Поступило новое предложение\n\n"
                 f"@{message.from_user.username}\n"
                 f"Имя и Фамилия: {databot.user_name(message.from_user.id)}\n"
                 f"Телефон: {databot.user_phone(message.from_user.id)}\n"
                 f"Содержание: {message.text}"
        )


def register_clientapplication():
    router.message.register(leave_a_request, Text(text=text_request()), state=FSMClientStart.menu)
    router.callback_query.register(leave_a_request_back, Text(text="3"), state=FSMClientStart.application)

    router.callback_query.register(leave_a_request_complaint1, Text(text="1"), state=FSMClientStart.application)
    router.callback_query.register(leave_a_request_complaint1_back, Text(text="2"), state=FSMClientStart.complaint1)
    router.message.register(leave_a_request_complaint1_text, ChatIsNotTextFilter(), state=FSMClientStart.complaint1)

    router.callback_query.register(leave_a_request_complaint2, Text(text="1"), state=FSMClientStart.complaint1)
    router.callback_query.register(leave_a_request_complaint2_back, Text(text="2"), state=FSMClientStart.complaint2)
    router.message.register(leave_a_request_complaint2_media, ChatApplicationComplainFilter(), state=FSMClientStart.complaint2)

    router.callback_query.register(leave_a_request_complaint3, Text(text="1"), state=FSMClientStart.complaint2)
    router.callback_query.register(leave_a_request_complaint3_back, Text(text="2"), state=FSMClientStart.complaint3)
    router.message.register(leave_a_request_complaint3_text, ChatIsNotTextFilter(), state=FSMClientStart.complaint3)

    router.callback_query.register(leave_a_suggestion, Text(text="2"), state=FSMClientStart.application)
    router.callback_query.register(leave_a_suggestion_back, Text(text="2"), state=FSMClientStart.suggestion)
    router.message.register(leave_a_suggestion_and_photo, ChatIsNotTextFilter(), state=FSMClientStart.suggestion)

    return router
