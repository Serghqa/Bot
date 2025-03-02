from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()
    play = State()
    win = State()
