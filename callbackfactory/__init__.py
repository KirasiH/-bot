from aiogram.filters.callback_data import CallbackData

class CallbackQuestionFactory(CallbackData, prefix="question"):

    client_name: str
    client_id: int

class CallbackAnswerFactory(CallbackData, prefix="answer"):

    client_id: int