from aiogram.fsm.state import StatesGroup, State


class Vote(StatesGroup):
    GetName = State()
    ChooseRegion = State()

