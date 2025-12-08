from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    start = State()
    photo = State()
    text_1 = State()
    text_2 = State()