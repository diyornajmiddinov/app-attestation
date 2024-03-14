from aiogram import types
from aiogram.types import InlineKeyboardButton

from data.loader import bot, db

sticks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
          "21", "22", "23", "24", "25"]

stats = ['administrator', 'creator', 'member']


async def joined(user_id: int) -> bool:
    f = db.find_all_channels()
    if f.collection.count_documents({}) > 0:
        for x in f:
            s = await bot.get_chat_member(chat_id=x.get("_id"), user_id=user_id)
            if s.status in stats:
                pass
            else:
                return False
    return True


async def butts(user_id: int):
    f = db.find_all_channels()
    if f.collection.count_documents({}) > 0:
        y = 0
        butt = types.InlineKeyboardMarkup(inline_keyboard=[])
        for x in f:
            s = await bot.get_chat_member(chat_id=int(x.get("_id")), user_id=user_id)
            if s.status in stats:
                pass
            else:
                butt.inline_keyboard.append(
                    [types.InlineKeyboardButton(text=f"{sticks[y]} - KANAL", url=x.get("link"))]
                )
                y += 1
        butt.inline_keyboard.append([InlineKeyboardButton(text=f"Obuna bo‘ldim ✅", callback_data="check")])
        return butt
    else:
        return types.InlineKeyboardMarkup(inline_keyboard=[])
