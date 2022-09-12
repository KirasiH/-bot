from aiogram import types, Router, Bot, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from FSM import FSMAdmin, FSMClientStart

from keyboards.client.keyboard import client_menu
from keyboards.admin.keyboard import admin_panel

from callbackfactory import CallbackAnswerFactory
from middleware.ban import BanMiddleware
from databot import databot


router = Router()
router.message.filter(F.chat.type.in_("private"))
router.message.outer_middleware(BanMiddleware())


async def admin_start(message: types.Message, state: FSMContext):

    if message.from_user.id in databot.list_admin():
        await state.clear()
        await state.set_state(FSMAdmin.admin)

        await message.answer("Добро пожаловать в режим администратора!", reply_markup=admin_panel())

    else:
        await message.answer("Извините, вы не являетесь администратором!")


async def admin_block(message: types.Message, state: FSMContext):

    await state.set_state(FSMAdmin.block)
    await message.answer("Введите id пользователя, которого нужно заблокировать!")


async def block_user(message: types.Message, state: FSMContext):

    try:
        databot.user_new_status_block(int(message.text), 1)
        await message.answer("Забанен)")

    except ValueError:
        await message.answer("Что-то пошло не так!")

    finally:
        await state.set_state(FSMAdmin.admin)


async def admin_disblock_user(message: types.Message, state: FSMContext):

    await state.set_state(FSMAdmin.disblock)
    await message.answer("Введите id пользователя, которого нужно разблокировать")


async def disblock_user(message: types.Message, state: FSMContext):

    try:
        databot.user_new_status_block(int(message.text), 0)
        await message.answer("Разабанен)")

    except ValueError:
        await message.answer("Что-то пошло не так!")

    finally:
        await state.set_state(FSMAdmin.admin)


async def admin_mailing(message: types.Message, state: FSMContext):

    await state.set_state(FSMAdmin.mailing)
    await message.answer("Напишите текст для рассылки")


async def mailing(message: types.Message, state: FSMContext, bot: Bot):

    for user in databot.user_list:

        if user != message.from_user.id:
            await bot.send_message(
                user,
                text=message.text
            )

    await message.answer("Рассылка была успешной!", reply_markup=admin_panel())

    await state.set_state(FSMAdmin.admin)


async def admin_info_user(message: types.Message, state: FSMContext):

    await state.set_state(FSMAdmin.info)
    await message.answer("Напишите id пользователя", reply_markup=admin_panel())


async def info_user(message: types.Message, state: FSMContext):

    try:
        data = databot.user_info(int(message.text))
        if not data:
            await message.answer("Данный пользователь не существует!")
            return

    except ValueError:
        await message.answer("Что-то пошло не так!")

    else:
        await message.answer(f"Имя и Фамилия: {data[1]} \nНомер телефона {data[2]}\n", reply_markup=admin_panel())

    finally:
        await state.set_state(FSMAdmin.admin)


async def admin_cancel(message: types.Message, state: FSMContext):

    await state.set_state(FSMClientStart.menu)
    await message.answer("Выхожу из состояния администратора!", reply_markup=client_menu())


async def callback_admin_answer(event: types.CallbackQuery, callback_data: CallbackAnswerFactory, state: FSMContext):

    await state.set_state(FSMAdmin.answer)
    await state.update_data(id=callback_data.client_id)

    await event.message.edit_text("Напишите ответ!")

async def admin_answer(message: types.Message, state: FSMContext, bot: Bot):

    data = await state.update_data()
    await state.set_state(FSMClientStart.menu)
    await bot.send_message(
        data['id'],
        text=message.text
    )

    await state.clear()
    await message.answer("Ответ отправлен пользователю!")


def register_admin():
    router.message.register(admin_start, Command(commands="admin"))
    router.message.register(admin_cancel, Command(commands="cancel"), state=FSMAdmin.admin)

    router.message.register(admin_block, Text(text="Блокировать\n пользователя"), state=FSMAdmin.admin)
    router.message.register(block_user, state=FSMAdmin.block)

    router.message.register(admin_disblock_user, Text(text="Разблокировать\n пользователя"), state=FSMAdmin.admin)
    router.message.register(disblock_user, state=FSMAdmin.disblock)

    router.message.register(admin_mailing, Text(text="Рассылка"), state=FSMAdmin.admin)
    router.message.register(mailing, state=FSMAdmin.mailing)

    router.message.register(admin_info_user, Text(text="Информация\nо пользователе"), state=FSMAdmin.admin)
    router.message.register(info_user, state=FSMAdmin.info)

    router.callback_query.register(callback_admin_answer, CallbackAnswerFactory.filter())
    router.message.register(admin_answer, state=FSMAdmin.answer)

    return router
