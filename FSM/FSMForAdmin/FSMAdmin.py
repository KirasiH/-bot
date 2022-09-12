from aiogram.fsm.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    admin = State()
    info = State()
    mailing = State()
    block = State()
    disblock = State()
    answer = State()