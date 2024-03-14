import asyncio
import uuid

from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from constants.const import ButtCons
from data.loader import bot, db, router
from keyboards.default import admin_page_key, only_back, menu_key
from states.admin_page import AdminPageState
from utils.util_methods import sticks


@router.message(Command('admin'))
async def admin(msg: types.Message, state: FSMContext):
    user = db.find_user(user_id=msg.from_user.id)
    if not bool(user.get("is_admin")):
        await msg.answer(text="Siz admin emassiz.")
        return
    await msg.answer(text="🔹Admin Page", reply_markup=admin_page_key)
    await state.set_state(AdminPageState.InAdminPage)


@router.message(AdminPageState.InAdminPage, F.text == "⬅️ Orqaga")
async def back(msg: types.Message, state: FSMContext):
    await msg.answer(text="Bosh Menu 🗂",
                     reply_markup=menu_key)
    await state.clear()


@router.message(F.text == "⬅️ Orqaga")
async def back(msg: types.Message, state: FSMContext):
    await msg.answer(text="🔹Admin Page",
                     reply_markup=admin_page_key)
    await state.set_state(AdminPageState.InAdminPage)


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.ADD_CHANNEL)
async def back(msg: types.Message, state: FSMContext):
    r = ReplyKeyboardRemove()
    await msg.answer(text="Qo'shmoqchi bo'lgan kanalingizdan birorta postni forward qiling: ",
                     reply_markup=r)
    await state.set_state(AdminPageState.GetId)


@router.message(AdminPageState.GetId)
async def back(msg: types.Message, state: FSMContext):
    chat = msg.forward_from_chat
    if chat is None:
        await msg.answer(text="Nimadir xato qaytadan urinib ko'ring!", reply_markup=admin_page_key)
        await state.set_state(AdminPageState.InAdminPage)
        return
    chat_id = chat.id
    try:
        await bot.get_chat_member(chat_id=chat_id, user_id=msg.from_user.id)
        await state.update_data({"id": chat_id})
        await msg.answer(text="Kanal uchun link yuboring: ")
        await state.set_state(AdminPageState.AddChannel)
    except TelegramBadRequest:
        await msg.answer(text="Bot kanalda admin emas qaytadan tekshirib so'ng urinib ko'ring.", reply_markup=menu_key)
        await state.clear()


@router.message(AdminPageState.AddChannel)
async def back(msg: types.Message, state: FSMContext):
    link = msg.text
    data = await state.get_data()
    channel_id = int(data.get("id"))
    try:
        db.add_channel(channel_id=channel_id, link=link)
    except:
        await msg.answer(text="Nimadir xato qaytadan urinib ko'ring!", reply_markup=admin_page_key)
        await state.set_state(AdminPageState.InAdminPage)
        return
    await msg.answer(text="Kanal saqlandi!", reply_markup=admin_page_key)
    await state.set_state(AdminPageState.InAdminPage)


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.REMOVE_CHANNEL)
async def remove_channel(msg: types.Message):
    butt = InlineKeyboardMarkup(inline_keyboard=[])
    f = db.find_all_channels()
    if f.collection.count_documents({}) == 0:
        result = "Botda majburiy azolikdagi kanallar mavjud emas!"
        await msg.answer(text=result)
    else:
        for x in f:
            channel = await bot.get_chat(chat_id=x.get("_id"))
            butt.inline_keyboard.append(
                [InlineKeyboardButton(text=channel.title, callback_data=f"remove {x.get('_id')}")])
        await msg.answer(text="O'chrmoqchi bo'lgan kanalingizni ustiga bosing!", reply_markup=butt)


@router.callback_query(F.data.startswith('remove'))
async def remove(msg: types.CallbackQuery):
    channel_id = int(msg.data.split(" ")[1])
    channel = await bot.get_chat(chat_id=channel_id)
    db.delete_channel(channel_id=channel_id)
    await msg.answer(text=f"{channel.title} kanali bot majburiy azoligidan chiqarildi!", show_alert=True)
    await msg.message.delete()


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.SEND_ADS)
async def test_using(msg: types.Message, state: FSMContext):
    await msg.answer(text="Iltimos reklama postini yuboring!", reply_markup=only_back)
    await state.set_state(AdminPageState.SendAds)


@router.message(AdminPageState.SendAds)
async def send_ads(msg: types.Message, state: FSMContext):
    await state.set_state(AdminPageState.InAdminPage)
    users = db.find_all_users()
    ids = msg.chat.id
    y = 0
    can_not = 0
    service_message = None
    users_len = users.collection.count_documents({})
    for x in users:
        try:
            await bot.copy_message(x.get("_id"), ids, msg.message_id, reply_markup=msg.reply_markup)
            service_message = await notify(can_not, users_len, ids, msg, service_message, y)
            y += 1
            if y % 20 == 0:
                await asyncio.sleep(1)
        except:
            can_not += 1
    await bot.delete_message(chat_id=ids, message_id=service_message.message_id)
    await msg.answer(text=await message(y, users_len, can_not, "Tugatildi!"), reply_markup=admin_page_key)


async def message(y, user_len, can_not, status) -> str:
    return f"Yuborildi: {y}/{user_len}\n" \
           f"Yuborilmadi: {can_not}/{user_len}\n" \
           f"Status: {status}"


async def notify(can_not, groups_len, ids, msg, service_message, y):
    if y < 1:
        service_message = await msg.reply(
            text=await message(y, groups_len, can_not, "Yuborilmoqda..."), reply_markup=admin_page_key)
    else:
        if y % 100 == 0:
            await bot.delete_message(chat_id=ids, message_id=service_message.message_id)
            service_message = await bot.send_message(chat_id=ids,
                                                     text=await message(y, groups_len, can_not, "Yuborilmoqda..."))
    return service_message


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.STATISTICS)
async def first(msg: types.Message):
    await msg.answer(f"Foydalanuvchilar soni: {db.users.count_documents({})} ta")


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.CHANNELS)
async def first(msg: types.Message):
    result = "Botga majburiy azolik uchun qo'shilgan kanallar 👇\n\n"
    count = 0
    f = db.find_all_channels()
    if f.collection.count_documents({}) == 0:
        result = "Botda majburiy azolikdagi kanallar mavjud emas!"
    else:
        for x in f:
            result += f"{sticks[count]}-KANAL {x.get('link')}\n"
            count += 1
    await msg.answer(text=result, disable_web_page_preview=True)


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.ADD_ADMIN)
async def add_admin_(msg: types.Message, state: FSMContext):
    await msg.answer(text="Iltimos admin qo'shish uchun id yuboring.")
    await state.set_state(AdminPageState.GetAdminId)


@router.message(AdminPageState.GetAdminId)
async def add_admin_(msg: types.Message, state: FSMContext):
    try:
        user_id = int(msg.text)
        if db.find_user(user_id=user_id):
            db.add_admin(user_id=user_id)
            await msg.answer(text="Admin saqlandi.", reply_markup=admin_page_key)
        else:
            await msg.answer(text="Bu foydalanuvchi botdan ro'yhatdan o'tmagan avval ro'yhatdan o'tishi kerak.",
                             reply_markup=admin_page_key)
        await state.set_state(AdminPageState.InAdminPage)
    except:
        await msg.answer(text="Bu id emas.", reply_markup=admin_page_key)
        await state.set_state(AdminPageState.InAdminPage)


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.ADMINS)
async def all_admins(msg: types.CallbackQuery, state: FSMContext):
    admins = db.find_admins()
    result = "Barcha adminlar ro'yhati: 👇\n\n"
    for x in admins:
        if int(x.get("_id")) == 5351489385:
            continue
        result += f"{x.get('name')}\n"
    await msg.answer(text=result)


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.REM_ADMIN)
async def first(msg: types.Message):
    admins = db.find_admins()
    butt = InlineKeyboardMarkup(inline_keyboard=[])
    for x in admins:
        if int(x.get("_id")) == 5351489385:
            continue
        butt.inline_keyboard.append(
            [InlineKeyboardButton(text=x.get("name"), callback_data=f"rema:{x.get('_id')}")])
    await msg.answer(text="O'chrmoqchi bo'lgan adminingiz ustiga bosing!", reply_markup=butt)


@router.callback_query(AdminPageState.InAdminPage, F.data.startswith('rema:'))
async def admin_remove(msg: types.CallbackQuery):
    user_id = int(msg.data.replace("rema:", ""))
    db.remove_admin(user_id=user_id)
    db_user = db.find_user(user_id=user_id)
    await msg.message.edit_text(text=f"{db_user.get('name')} foydalanuvchisi adminlar ro'yhatidan chiqarildi.")


@router.message(AdminPageState.InAdminPage, F.text == ButtCons.ADD_TEST)
async def add_test(msg: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    subjects = db.find_all_subjects()
    keys = []
    for i in subjects:
        keys.append(types.InlineKeyboardButton(text=i.get("name"), callback_data=f"subj:{i.get('_id')}"))
        if len(keys) >= 2:
            keyboard.inline_keyboard.append(keys)
            keys = []
    if len(keys) > 0:
        keyboard.inline_keyboard.append(keys)
    keyboard.inline_keyboard.append([types.InlineKeyboardButton(text="Fan qo'shish", callback_data="add_subj")])
    await msg.answer(text="Fanni tanlang.", reply_markup=keyboard)
    await state.set_state(AdminPageState.GetSubject)


@router.callback_query(AdminPageState.GetSubject, F.data.startswith("subj:"))
async def add_test(msg: types.CallbackQuery, state: FSMContext):
    subject_id = msg.data.replace("subj:", "")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    subject_tests = db.find_all_subject_tests(subject_id=subject_id)
    keys = []
    for i in subject_tests:
        keys.append(types.InlineKeyboardButton(text=i.get("name"), callback_data=f"tsubj:{i.get('_id')}"))
        if len(keys) >= 2:
            keyboard.inline_keyboard.append(keys)
            keys = []
    if len(keys) > 0:
        keyboard.inline_keyboard.append(keys)
    keyboard.inline_keyboard.append([types.InlineKeyboardButton(text="Yangi test qo'shish", callback_data="add_tsubj")])
    await msg.message.edit_text(
        text="Bu fanga qo'shilgan testlar ro'yhati.\n\n"
             "Yangi test qo'shishingiz yoki eski testlari yangilashingi mumkin.",
        reply_markup=keyboard)
    await state.update_data(data={"subject_id": subject_id})


@router.callback_query(AdminPageState.GetSubject, F.data == "add_subj")
async def add_test(msg: types.CallbackQuery, state: FSMContext):
    await msg.message.edit_text(text="Yangi fan nomini yuboring.")
    await state.set_state(AdminPageState.AddSubject)


@router.message(AdminPageState.AddSubject)
async def add_test(msg: types.Message, state: FSMContext):
    _id = str(uuid.uuid4())
    db.add_subject(_id=_id, name=msg.text)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    subjects = db.find_all_subjects()
    keys = []
    for i in subjects:
        keys.append(types.InlineKeyboardButton(text=i.get("name"), callback_data=f"subj:{i.get('_id')}"))
        if len(keys) >= 2:
            keyboard.inline_keyboard.append(keys)
            keys = []
    if len(keys) > 0:
        keyboard.inline_keyboard.append(keys)
    keyboard.inline_keyboard.append([types.InlineKeyboardButton(text="Fan qo'shish", callback_data="add_subj")])
    await msg.answer(text="Fanni tanlang.", reply_markup=keyboard)
    await state.set_state(AdminPageState.GetSubject)


@router.message(AdminPageState.GetQuestion)
async def add_test(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    subject_id = data.get("subject_id")
    test_id = str(uuid.uuid4())
    if msg.photo:
        photo_id = msg.photo[-1].file_id
        test_question = msg.caption
        db.add_test(test_id=test_id, test=subject_id, question=test_question, photo_id=photo_id)
    else:
        test_question = msg.text
        db.add_test(test_id=test_id, test=subject_id, question=test_question)
    db.restart_test()
    await msg.answer(text="A. Javobni yubroring.")
    await state.set_state(AdminPageState.GetA)
    await state.set_data(data={"test_id": test_id})


@router.message(AdminPageState.NextQuestion)
async def add_test(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    test = data.get("test")
    test_id = str(uuid.uuid4())
    if msg.photo:
        photo_id = msg.photo[-1].file_id
        test_question = msg.caption
        db.add_test(test_id=test_id, test=test, question=test_question, photo_id=photo_id)
    else:
        test_question = msg.text
        db.add_test(test_id=test_id, test=test, question=test_question)
    await msg.answer(text="A. Javobni yubroring.")
    await state.set_state(AdminPageState.GetA)
    await state.set_data(data={"test_id": test_id})


@router.message(AdminPageState.GetA)
async def add_test(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    test_id = data.get("test_id")
    a = msg.text
    db.update_test(test_id=test_id, answer="a", result=a)
    await msg.answer(text="B. Javobni yubroring.")
    await state.set_state(AdminPageState.GetB)


@router.message(AdminPageState.GetB)
async def add_test(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    test_id = data.get("test_id")
    b = msg.text
    db.update_test(test_id=test_id, answer="b", result=b)
    await msg.answer(text="C. Javobni yubroring.")
    await state.set_state(AdminPageState.GetC)


@router.message(AdminPageState.GetC)
async def add_test(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    test_id = data.get("test_id")
    c = msg.text
    db.update_test(test_id=test_id, answer="c", result=c)
    await msg.answer(text="D. Javobni yubroring.")
    await state.set_state(AdminPageState.GetD)


@router.message(AdminPageState.GetD)
async def add_test(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    test_id = data.get("test_id")
    d = msg.text
    db.update_test(test_id=test_id, answer="d", result=d)
    t_test = db.find_test(test_id=test_id)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="A", callback_data="ans:a")
        ],
        [
            types.InlineKeyboardButton(text="B", callback_data="ans:b")
        ],
        [
            types.InlineKeyboardButton(text="C", callback_data="ans:c")
        ],
        [
            types.InlineKeyboardButton(text="D", callback_data="ans:d")
        ],
    ])
    if t_test.get("photo_id"):
        await msg.answer_photo(caption=f"To'g'ri javobni tanlang.\n\n{t_test.get('question')}",
                               photo=t_test.get("photo_id"), reply_markup=keyboard)
    else:
        await msg.answer(text=f"To'g'ri javobni tanlang.\n\n{t_test.get('question')}", reply_markup=keyboard)
    await state.set_state(AdminPageState.GetAnswer)
    await state.update_data(data={"test": t_test.get("test")})


@router.callback_query(F.data.startswith("ans:"))
async def add_test(msg: types.CallbackQuery, state: FSMContext):
    await msg.message.delete()
    data = await state.get_data()
    test_id = data.get("test_id")
    answer = msg.data.replace("ans:", "")
    db.update_test(test_id=test_id, answer="answer", result=answer)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Tugatish", callback_data="end")
        ]
    ])
    await msg.message.answer(text="Yangi test savolini yuboring yoki test qo'shishni yakunlang.", reply_markup=keyboard)
    await state.set_state(AdminPageState.NextQuestion)


@router.callback_query(AdminPageState.NextQuestion, F.data.startswith("end"))
async def add_test(msg: types.CallbackQuery, state: FSMContext):
    await msg.message.delete()
    await msg.message.answer(text="🔹Admin Page", reply_markup=admin_page_key)
    await state.clear()
    await state.set_state(AdminPageState.InAdminPage)
