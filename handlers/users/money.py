from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.client.session.middlewares.request_logging import logger

from data.config import MONEY_ADMIN, url_yaml
from keyboards.inline.money import get_money, ha_yoq, qabul_qilish
from keyboards.reply.base import pul_ishlash, bekor_qilish_keyboard
from loader import db, bot
from states.test import ReferalForm

router = Router()


@router.message(F.text == "Pul chiqarish💰")
async def make_money(message: types.Message):
    invited_count = db.get_user_invited_count(message.from_user.id)
    count = db.get_user_invited_count(message.from_user.id)
    if not count:
        count = 0
    else:
        count = count[0]
    if invited_count:
        my_money = invited_count[0] * url_yaml['invited_credit']
        await message.answer(f"Sizning hisobingizda {my_money} so'm bor.\n"
                             f"👨‍👩‍👦 Referal orqali qo'shilganlar: {count} dona\n"
                             f"\nHisobingizda jami {url_yaml['min_balance']} so'm bo'lsa pulingizni chiqarib olishingiz mumkin",
                             reply_markup=get_money())
    else:
        await message.answer("Sizning hisobingizda pul yo'q. \n"
                             f"👨‍👩‍👦 Referal orqali qo'shilganlar: {count} dona\n"

                             "\nReferal havola orqali do'stlaringizni taklif qiling va pul ishlang")


@router.message(F.text == "To'lov kanali📜")
async def make_money(message: types.Message):
    kanal = url_yaml['tolov_kanal']
    if kanal:
        await message.answer(f"Bot to'lovlarini shu kanalda ko'rishingiz mumkin.\n\n{kanal}")
    else:
        await message.answer(f"Bot to'lovlari uchun kanal qo'shilmagan")


@router.message(F.text == "Referal havola📎")
async def referal_havola(message: types.Message):
    msg = f"""ℹ️ Referal manzil orqali do'stlaringizni botga taklif qiling va pul ishlab toping. 


Sizning referal manzilingiz 👇 """
    bot_properties = await bot.me()
    await message.answer(f"{msg}\n\n t.me/{bot_properties.username}?start={message.from_user.id}")


@router.message(F.text == "Balans💵")
async def balans(message: types.Message):
    invited_count = db.get_user_invited_count(message.from_user.id)
    count = db.get_user_invited_count(message.from_user.id)
    if not count:
        count = 0
    else:
        count = count[0]
    if invited_count:
        my_money = invited_count[0] * url_yaml['invited_credit']
        await message.answer(f"Sizning hisobingizda {my_money} so'm bor.\n"
                             f"👨‍👩‍👦 Referal orqali qo'shilganlar: {count} dona\n"
                             f"\nHisobingizda jami {url_yaml['min_balance']} so'm bo'lsa pulingizni chiqarib olishingiz mumkin",
                             reply_markup=get_money())
    else:
        await message.answer("Sizning hisobingizda pul yo'q. \n"
                             f"👨‍👩‍👦 Referal orqali qo'shilganlar: {count} dona\n"

                             "\nReferal havola orqali do'stlaringizni taklif qiling va pul ishlang")


@router.callback_query(F.data == "pul_chiqarib_olish")
async def pul_chiqarish(call: types.CallbackQuery, state: FSMContext):
    invited_count = db.get_user_invited_count(call.from_user.id)
    if invited_count[0] >= url_yaml['min_balance'] / url_yaml['invited_credit']:
        await call.message.answer("Telefon raqam yoki karta raqamingizni tashlang.")
        await state.set_state(ReferalForm.CARD)
    else:
        await call.message.answer("Hisobingizda yetarlicha pul yo'q,  "
                                  f"\nhisobingiz {url_yaml['min_balance']} so'mga yetganda pulingizni chiqarib olishingiz mumkin")


@router.message(ReferalForm.CARD)
async def get_card(message: types.Message, state: FSMContext):
    await message.answer(f"{message.text}\nShu hisobga pul o'tkazilishiga ishonchingiz komilmi?", reply_markup=ha_yoq())
    await state.update_data(card=message.text)


@router.callback_query(F.data == "Ha", ReferalForm.CARD)
async def ha(call: types.CallbackQuery, state: FSMContext):
    count = db.get_user_invited_count(call.from_user.id)
    card = await state.get_data()
    card = card.get('card')
    msg = (
        f"User: <a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a>\nTaklif qilganlari soni: {count[0]}"
        f"\nO'tkazilishi kerak bo'lgan summa: {count[0] * url_yaml['invited_credit']} so'm\nKarta/telefon raqam: {card}")

    await bot.send_message(MONEY_ADMIN, msg, reply_markup=qabul_qilish(call.from_user.id), parse_mode='HTML')
    await call.message.answer("""Ovoz berishni ustiga bosib ovoz bering va pul ishlang 💰

Toʻlov 24 soatdan 48 soat ichida tashlab beriladi bemalol ungacha pul ishlashingiz mumkin 💸👍""")
    await state.clear()


@router.callback_query(F.data == "Yoq", ReferalForm.CARD)
async def yoq(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Bekor qilindi", reply_markup=pul_ishlash())
    await state.clear()


@router.callback_query(F.data.startswith("otkazildi_"))
async def otkazildi(call: types.CallbackQuery):
    user_id = call.data.split("_")[1]
    try:
        db.update_invite_current_count_set_0(int(user_id))
        await bot.edit_message_reply_markup(chat_id=MONEY_ADMIN, message_id=call.message.message_id)
        await bot.send_message(user_id, "Hisobingizga pul o'tkazildi")
    except Exception as e:
        bot.send_message(MONEY_ADMIN, f"xatolik yuz berdi\n{e}")


@router.callback_query(F.data.startswith("bekor_qilindi_"))
async def otkazildi(call: types.CallbackQuery):
    user_id = call.data.split("_")[2]
    try:
        db.update_invite_current_count_set_0(int(user_id))
        await bot.edit_message_reply_markup(chat_id=MONEY_ADMIN, message_id=call.message.message_id)
        await bot.send_message(user_id, "Hisobingizga pul o'tkazilmadi. Iltimos qayta urinib ko'ring")
    except Exception as e:
        logger.info(e)
