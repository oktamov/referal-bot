from aiogram.fsm.context import FSMContext

from filters import IsBotAdmin
from loader import db
from aiogram import types, F, Router

from states.test import FilmAddStates
from keyboards.reply import reply_keyboard_for_admin

router = Router()


@router.message(F.text == "🔙 Orqaga", IsBotAdmin())
async def orqaga(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🔝 Asosiy Menyu", reply_markup=reply_keyboard_for_admin())


@router.message(F.text == "➕ Kanal qo'shish", IsBotAdmin())
async def add_channel(message: types.Message, state: FSMContext):
    await message.answer("Telegram kanal chat id'si kiriting !!!")
    await state.set_state(FilmAddStates.chat_id)


@router.message(F.text, FilmAddStates.chat_id)
async def film_quality_add(message: types.Message, state: FSMContext):
    await message.answer("Telegram kanal kanal Url'ni kiriting !!!")
    await state.set_state(FilmAddStates.url)
    chat_id = message.text
    await state.update_data({
        'chat_id': chat_id
    })


@router.message(F.text, FilmAddStates.url)
async def film_quality_add(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data({
        'url': url
    })
    data = await state.get_data()
    db.add_channel(data['chat_id'], data['url'])
    await message.answer(f"Yangi kanal qo‘shildi: {url}")
    await state.clear()


@router.message(F.text == "➖ Kanal o'chrish", IsBotAdmin())
async def delete_channel(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, o'chirish uchun kanal id'sini kiriting !!!")
    await state.set_state(FilmAddStates.delete_kanal)


@router.message(F.text, FilmAddStates.delete_kanal)
async def delete_kanal(message: types.Message, state: FSMContext):
    kanal_delete = message.text
    await state.update_data({
        'kanal_delete': kanal_delete
    })
    data = await state.get_data()
    db.delete_channel(data['kanal_delete'])
    await message.answer(f"Kanal o‘chirildi !!")
    await state.clear()


@router.message(F.text == "👁‍🗨 Majburiy kanallarni ko'rish", IsBotAdmin())
async def list_channels(message: types.Message):
    channels = db.get_all_channels()
    if channels:
        channels_text = "\n\n".join([f"{channel}" for channel in channels])
        await message.answer(f"Majburiy kanallar:\n\n{channels_text}")
    else:
        await message.answer("Majburiy kanallar qo'shilmagan.")
