from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv

from handlers import register_admin
from handlers import register_clientstart
from handlers import register_clientapplication
from handlers import register_contacts
from handlers import register_settings
from handlers import register_group
from handlers import register_contact

import os
import asyncio


load_dotenv(find_dotenv())


bot = Bot(os.getenv("TOKEN"))
dispatcher = Dispatcher()


async def main():
    dispatcher.include_router(register_admin())
    dispatcher.include_router(register_clientstart())
    dispatcher.include_router(register_clientapplication())
    dispatcher.include_router(register_contacts())
    dispatcher.include_router(register_settings())
    dispatcher.include_router(register_group())
    dispatcher.include_router(register_contact())

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
