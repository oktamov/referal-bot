import logging
import asyncio

import yaml
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.reply import reply_keyboard_for_admin
from loader import db, bot
from keyboards.inline.buttons import yes_no_keyboard
from states.test import AdminState
from filters.admin import IsBotAdminFilter
from data.config import ADMINS, url_yaml, config_dir

router = Router()


@router.message(Command('admin'), IsBotAdminFilter(ADMINS))
async def get_all_users(message: types.Message):
    await message.answer(f"Xush kelibsiz", reply_markup=reply_keyboard_for_admin())


@router.message(F.text == '📊Statistika', IsBotAdminFilter(ADMINS))
async def get_all_users(message: types.Message):
    users_count = db.count_users()
    await message.answer(f"Botda foydalanuvchilar soni: {users_count[0]}")


@router.message(F.text == '✏️Url ni tahrirlash', IsBotAdminFilter(ADMINS))
async def set_url(message: types.Message, state: FSMContext):
    url = url_yaml['url']
    await message.answer(f"Avvalgi URL: {url}\nURL ni o'zgartirishni hohlaysizmi?", reply_markup=yes_no_keyboard('url'))
    # await state.set_state(AdminState.set_url)


@router.message(F.text == '✏️Minimal chiqarish narx ni tahrirlash', IsBotAdminFilter(ADMINS))
async def set_min_handler(message: types.Message, state: FSMContext):
    url = url_yaml['min_balance']
    await message.answer(f"Avvalgi minimal narx: {url}\n\no'zgartirishni hohlaysizmi?",
                         reply_markup=yes_no_keyboard('min'))
    # await state.set_state(AdminState.set_url)


@router.message(F.text == '✏️Pul berish summa ni tahrirlash', IsBotAdminFilter(ADMINS))
async def set_pul_handler(message: types.Message, state: FSMContext):
    url = url_yaml['invited_credit']
    await message.answer(f"Avvalgi qo'shiladigan Pul miqdori: {url}\no'zgartirishni hohlaysizmi?",
                         reply_markup=yes_no_keyboard('pul'))
    # await state.set_state(AdminState.set_url)


@router.message(F.text == '✏️To\'lov kanalni ni tahrirlash', IsBotAdminFilter(ADMINS))
async def set_kanal_handler(message: types.Message, state: FSMContext):
    url = url_yaml['tolov_kanal']
    await message.answer(f"Avvalgi to'lov kanal: {url}\no'zgartirishni hohlaysizmi?",
                         reply_markup=yes_no_keyboard('kanal'))


@router.message(F.text == '✏️Bir ovozga pul berishni tahrirlash', IsBotAdminFilter(ADMINS))
async def set_kanal_handler(message: types.Message, state: FSMContext):
    url = url_yaml['vote_credit']
    await message.answer(f"Avvalgi narx: {url}\no'zgartirishni hohlaysizmi?",
                         reply_markup=yes_no_keyboard('vote'))


@router.callback_query(F.data == 'no', IsBotAdminFilter(ADMINS))
async def request_url_no(call: types.CallbackQuery, state: FSMContext):
    text = "bekor qilindi"
    await call.message.answer(text)
    await state.clear()


@router.callback_query(F.data == 'yes', IsBotAdminFilter(ADMINS))
async def request_url_yes(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text = "yangi URL kiriting."
    await call.message.answer(text)
    await state.set_state(AdminState.set_url)


@router.callback_query(F.data == 'no_min', IsBotAdminFilter(ADMINS))
async def request_min_no(call: types.CallbackQuery, state: FSMContext):
    text = "bekor qilindi"
    await call.message.answer(text)
    await state.clear()


@router.callback_query(F.data == 'yes_min', IsBotAdminFilter(ADMINS))
async def request_min_yes(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text = f"Yangi MINIMAL yechib olish summasini kiriting.\navvalgisi : {url_yaml['min_balance']}"
    await call.message.answer(text)
    await state.set_state(AdminState.set_min)


@router.callback_query(F.data == 'no_pul', IsBotAdminFilter(ADMINS))
async def request_pul_no(call: types.CallbackQuery, state: FSMContext):
    text = "bekor qilindi"
    await call.message.answer(text)
    await state.clear()


@router.callback_query(F.data == 'yes_pul', IsBotAdminFilter(ADMINS))
async def request_pul_yes(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text = f"Har bir qo'shgan odam uchun beriladigan PUL ni kiriting\navvalgisi : {url_yaml['invited_credit']}"
    await call.message.answer(text)
    await state.set_state(AdminState.set_pul)


@router.callback_query(F.data == 'yes_kanal', IsBotAdminFilter(ADMINS))
async def request_kanal_yes(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text = f"Yangi to'lov kanalni belgilang \navvalgisi : {url_yaml['tolov_kanal']}"
    await call.message.answer(text)
    await state.set_state(AdminState.set_kanal)


@router.callback_query(F.data == 'yes_vote', IsBotAdminFilter(ADMINS))
async def request_kanal_yes(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text = f"Yangi ovoz berish uchun summani kiriting \navvalgisi : {url_yaml['vote_credit']}"
    await call.message.answer(text)
    await state.set_state(AdminState.set_vote)


@router.message(AdminState.set_url, IsBotAdminFilter(ADMINS))
async def set_url(message: types.Message, state: FSMContext):
    url_yaml['url'] = message.text
    with open(f"{config_dir}/url.yml", 'w') as f:
        yaml.dump(url_yaml, f, sort_keys=False)
    await message.answer(f"Muvoffaqiyatli o'zgartirildi \n{url_yaml['url']}")
    await state.clear()


@router.message(AdminState.set_min, IsBotAdminFilter(ADMINS))
async def set_min(message: types.Message, state: FSMContext):
    url_yaml['min_balance'] = int(message.text)
    with open(f"{config_dir}/url.yml", 'w') as f:
        yaml.dump(url_yaml, f, sort_keys=False)
    await message.answer(f"Muvoffaqiyatli o'zgartirildi \n{url_yaml['min_balance']}")
    await state.clear()


@router.message(AdminState.set_pul, IsBotAdminFilter(ADMINS))
async def set_pul(message: types.Message, state: FSMContext):
    url_yaml['invited_credit'] = int(message.text)
    with open(f"{config_dir}/url.yml", 'w') as f:
        yaml.dump(url_yaml, f, sort_keys=False)
    await message.answer(f"Muvoffaqiyatli o'zgartirildi \n{url_yaml['invited_credit']}")
    await state.clear()


@router.message(AdminState.set_kanal, IsBotAdminFilter(ADMINS))
async def set_kanal(message: types.Message, state: FSMContext):
    url_yaml['tolov_kanal'] = message.text
    with open(f"{config_dir}/url.yml", 'w') as f:
        yaml.dump(url_yaml, f, sort_keys=False)
    await message.answer(f"Muvoffaqiyatli o'zgartirildi \n{url_yaml['tolov_kanal']}")
    await state.clear()


@router.message(AdminState.set_vote, IsBotAdminFilter(ADMINS))
async def set_vote(message: types.Message, state: FSMContext):
    url_yaml['vote_credit'] = message.text
    with open(f"{config_dir}/url.yml", 'w') as f:
        yaml.dump(url_yaml, f, sort_keys=False)
    await message.answer(f"Muvoffaqiyatli o'zgartirildi \n{url_yaml['vote_credit']}")
    await state.clear()


@router.message(F.text == '📤Reklama', IsBotAdminFilter(ADMINS))
async def ask_ad_content(message: types.Message, state: FSMContext):
    await message.answer("Reklama uchun post yuboring")
    await state.set_state(AdminState.ask_ad_content)


@router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMINS))
async def send_ad_to_users(message: types.Message, state: FSMContext):
    await state.clear()
    users = db.select_all_users()
    count = 0
    for user in users:
        user_id = user[-1]
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            logging.info(f"Ad did not send to user: {user_id}. Error: {error}")
    await message.answer(text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.")
