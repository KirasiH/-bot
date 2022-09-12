from aiogram.filters import BaseFilter
from aiogram import types


class ChatApplicationComplainFilter(BaseFilter):

    async def __call__(self, message: types.Message):

        if not message.content_type in ["photo", "video"]:
            await message.answer("⛔В данном пункте нужно обязательно отправить фотографию или видео в виде медиа-сообщения\nПопробуйте ещё раз:")
            return False

        return True


class ChatIsNotTextFilter(BaseFilter):

    async def __call__(self, message: types.Message):

        if message.content_type == "text":
            return True

        await message.answer("Отправте текстовое сообщение!")
        return False
