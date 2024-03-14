from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants.const import TextConst
from data.loader import router, db
from keyboards.default import menu_key
from states.main_states import Vote
from utils.util_methods import joined, butts


@router.callback_query(F.data == "check")
async def check(msg: types.CallbackQuery):
    user_id = msg.from_user.id
    if not await joined(user_id=user_id):
        await msg.answer(text=TextConst.SUBSCRIPTION, show_alert=True)
        return
    else:
        await msg.message.delete()
        await msg.message.answer("Botdan foydalanishingiz mumkin.", reply_markup=menu_key)


@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    user_id = message.from_user.id
    user = db.find_user(user_id=user_id)
    if not user:
        db.add_user(user_id=user_id, name=message.from_user.first_name)
    if not await joined(user_id=user_id):
        await message.answer(text=TextConst.SUBSCRIPTION, reply_markup=await butts(user_id=user_id))
    else:
        await message.answer(text="Assalomu alaykum botimizga hush kelibsiz.", reply_markup=menu_key)

