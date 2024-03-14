from aiogram.fsm.state import StatesGroup, State


class AdminPageState(StatesGroup):
    GetAdminId = State()
    InAdminPage = State()
    SendAds = State()
    AddChannel = State()
    GetId = State()
    GetSubject = State()
    GetQuestion = State()
    GetTestName = State()
    GetA = State()
    GetB = State()
    GetC = State()
    GetD = State()
    GetAnswer = State()
    NextQuestion = State()
    AddSubject = State()

