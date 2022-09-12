from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, KICKED, Text
from databot import databot

from keyboards.admin.inlinekeyboard import admin_answer

from callbackfactory import CallbackQuestionFactory
from middleware.ban import BanMiddleware


router = Router()
router.message.filter(F.chat.type.in_({"group", "supergroup"}))
router.message.outer_middleware(BanMiddleware())


async def group_start(message: types.Message):
    
    await message.answer("Вас приветствует бот, что это за группа?\n1 - request\n2 - suggestion\n3 - admin")


async def request_group(message: types.Message):

    if databot.group_request_id != 1:
        await message.answer("Такая группа уже существует!")

    else:
        databot.add_group(message.chat.id, 'request')
        databot.group_request_id = message.chat.id

        await message.answer("Я рад, что вы меня добавили в группу. Сюда я буду отсылать жалобы!")


async def suggestion_group(message: types.Message):
    print(databot.group_suggestion_id)
    if databot.group_suggestion_id != 1:
        await message.answer("Такая группа уже существует!")

    else:
        databot.add_group(message.chat.id, 'suggestion')
        databot.group_suggestion_id = message.chat.id

        await message.answer("Я рад, что вы меня добавили в группу. Сюда я буду отсылать предложения!")


async def admin_group(message: types.Message):

    if databot.group_admin_id != 1:
        await message.answer("Такая группа уже существует!")

    else:
        databot.add_group(message.chat.id, 'admin')
        databot.group_admin_id = message.chat.id

        await message.answer("Я рад, что вы меня добавили в группу администрации!")


async def delete_group(message: types.Message):
    databot.delete_group(message.chat.id)

    if databot.group_suggestion_id == message.chat.id:
        databot.group_suggestion_id = 1

    elif databot.group_request_id == message.chat.id:
        databot.group_request_id = 1

    elif databot.group_admin_id == message.chat.id:
        databot.group_admin_id = 1


async def callback_question(event: types.CallbackQuery, callback_data: CallbackQuestionFactory, bot: Bot):

    await event.message.edit_text(f"Администратор @{event.from_user.username} отвечает клиенту @{callback_data.client_name}")
    await bot.send_message(event.from_user.id, f"Вы отвечаете пользователю @{callback_data.client_name}!", reply_markup=admin_answer(callback_data.client_id))


def register_group():
    router.message.register(group_start, CommandStart())
    router.message.register(request_group, Text(text="1"))
    router.message.register(suggestion_group, Text(text="2"))
    router.message.register(admin_group, Text(text="3"))

    router.callback_query.register(callback_question, CallbackQuestionFactory.filter())

    router.my_chat_member.register(delete_group, ChatMemberUpdatedFilter(member_status_changed=KICKED))

    return router
