from aiogram import types

from constants.const import ButtCons

admin_page_key = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text=ButtCons.ADD_TEST)
        ],
        [
            types.KeyboardButton(text=ButtCons.SEND_ADS),
            types.KeyboardButton(text=ButtCons.STATISTICS)
        ],
        [
            types.KeyboardButton(text=ButtCons.CHANNELS),
            types.KeyboardButton(text=ButtCons.ADMINS)
        ],
        [
            types.KeyboardButton(text=ButtCons.ADD_ADMIN),
            types.KeyboardButton(text=ButtCons.REM_ADMIN)
        ],
        [
            types.KeyboardButton(text=ButtCons.REMOVE_CHANNEL),
            types.KeyboardButton(text=ButtCons.ADD_CHANNEL)
        ],
        [
            types.KeyboardButton(text=ButtCons.BACK)
        ]
    ],
    resize_keyboard=True
)

menu_key = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text=ButtCons.SOLVE_TEST)
        ],
        [
            types.KeyboardButton(text=ButtCons.MY_TEST_RESULTS),
            types.KeyboardButton(text=ButtCons.HELP)
        ]
    ],
    resize_keyboard=True
)

get_phone = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Raqam yuborish", request_contact=True)
        ]
    ],
    resize_keyboard=True
)

only_back = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="⬅️ Orqaga")
        ]
    ],
    resize_keyboard=True
)
