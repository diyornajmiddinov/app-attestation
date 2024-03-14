from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from data.db import Database

API_TOKEN = '5238896668:AAEvRoCs8BJGa0SmtPISp4gmStyALGflITQ'
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
router = Router(name="main")
dp = Dispatcher(storage=storage)
db = Database()
