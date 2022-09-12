from aiogram.fsm.state import State, StatesGroup


class FSMClientStart(StatesGroup):
    name = State()
    number_phone = State()
    menu = State()
    application = State()
    complaint1 = State()
    complaint2 = State()
    complaint3 = State()
    suggestion = State()
    settings = State()
    settings_name = State()
    setting_phone = State()
    contact = State()
    contact_question = State()
    contact_phone = State()
    admin_client = State()
