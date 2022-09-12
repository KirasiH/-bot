from aiogram import types, Router, F
from aiogram.filters import Text

from text import text_contacts


router = Router()
router.message.filter(F.chat.type.in_({"private"}))


async def contacts(message: types.Message):

    with open("contact.txt", "r", encoding="utf-8") as file:
        await message.answer(file.read())


def register_contacts():
    router.message.register(contacts, Text(text=text_contacts()))

    return router

