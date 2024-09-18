from aiogram import Router, types, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext

from data.config import url_yaml, CHANNELS, get_channels
from keyboards.inline.buttons import subscribe_keyboard_invited, subscribe_keyboard
from keyboards.reply.base import pul_ishlash
from loader import db, bot

router = Router()


@router.message(F.chat.type.in_({"group", "supergroup"}) & F.new_chat_members)
async def welcome_new_members(message: types.Message):
    new_members = message.new_chat_members
    for member in new_members:
        await message.answer(f"Xush kelibsiz, {member.full_name}! Guruhimizga xush kelibsiz!")


@router.message(F.chat.type.in_({"group", "supergroup"}))
async def respond_in_group(message: types.Message):
    if "salom" in message.text.lower():
        await message.answer("Salom! Qanday yordam bera olaman?")
    elif "rahmat" in message.text.lower():
        await message.answer("Arzimaydi!")


async def is_user_subscribed(channels, user_id):
    status = False
    for channel in channels:
        channel_id = channel['id']
        try:
            chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if chat_member.status in ['member', 'administrator', 'creator']:
                status = True
        except Exception as e:
            print(f"Error checking subscription for channel {channel_id}: {e}")
            continue

    return status


@router.message(CommandStart())
async def start(message: types.Message, command: CommandObject, state: FSMContext):
    try:
        await state.clear()
    except Exception as e:
        print(f"xatolik: {e}")
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    user = db.select_user(telegram_id=telegram_id)
    # args = message.text.split()[1:] if len(message.text.split()) > 1 else None
    # print(url_yaml("channels"))
    if await is_user_subscribed(channels=get_channels(), user_id=message.from_user.id):
        if not user:
            try:
                if command.args:
                    invited_by_user = db.get_user_invited_count(int(command.args))
                    if invited_by_user:
                        db.update_invite_current_history_count_plus_1(int(command.args))
                        db.add_user_invite_member(int(command.args), message.from_user.id)
                    else:
                        db.add_user_invite_count(int(command.args), 1, 1)
                        db.add_user_invite_member(int(command.args), message.from_user.id)
                db.add_user(full_name=full_name, username=username, telegram_id=telegram_id)
            except Exception as error:
                logger.info(error)
        await message.answer(
            f"Assalomu alaykum {full_name}. \n\nBot orqali pul ishlash uchun referal havolangiz orqali do'stlaringizni "
            f"botga taklf qilib har bir taklif qilgan do'stingizga {url_yaml['invited_credit']} so'mdan pul ishlang 🤑 "
            f"",
            reply_markup=pul_ishlash())
    else:
        if CHANNELS:
            if command.args:
                await message.answer(f" Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling! 👇👇👇",
                                     reply_markup=subscribe_keyboard_invited(int(command.args)))
            else:
                await message.answer(f" Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling! 👇👇👇",
                                     reply_markup=subscribe_keyboard())
        else:
            pass


@router.callback_query(lambda c: c.data.startswith("subscribe_true_"))
async def oldim(call: types.CallbackQuery):
    await call.message.delete()
    invited_user = call.data.split("_")[2]

    if await is_user_subscribed(get_channels(), call.from_user.id):
        await call.message.answer("Botdan foydalanishingiz mumkin😊", reply_markup=pul_ishlash())
        invited_by_user = db.get_user_invited_count(invited_user)
        if invited_by_user:
            db.update_invite_current_history_count_plus_1(invited_user)
            await bot.send_message(int(invited_user), text=f"Siz {call.from_user.get_mention(as_html=True)} "
                                                           f"ni botga taklif qildingiz va 100 so'm taqdim etildi")
        else:
            db.add_user_invite_count(invited_user, 1, 1)
            # await bot.send_message(int(invited_user), text=f"lif qildingiz va 100 so'm taqdim etildi")
    else:
        await call.message.answer("Iltimios! Foydalanish uchun quyidagi kanallarga a'zo bo'ling! 👇👇👇",
                                  reply_markup=subscribe_keyboard_invited(call.from_user.id))


@router.callback_query(lambda c: c.data == "subscribe_true")
async def oldim(call: types.CallbackQuery):
    await call.message.delete()
    if await is_user_subscribed(get_channels(), call.from_user.id):
        await call.message.answer("Botdan foydalanishingiz mumkin😊", reply_markup=pul_ishlash())
    else:
        await call.message.answer("Iltimios! Foydalanish uchun quyidagi kanallarga a'zo bo'ling! 👇👇👇",
                                  reply_markup=subscribe_keyboard())


@router.message()
async def on_new_member(message: types.Message):
    for new_member in message.new_chat_members:
        inviter_id = message.from_user.id
        group_id = message.chat.id

        db.add_or_update_group_member(group_id, inviter_id)

        await message.answer(f"{message.from_user.full_name} guruhga {new_member.full_name} ni qo'shdi.")
        await message.answer(
            f"{message.from_user.full_name} hozirgacha {db.get_user_add_count(group_id, inviter_id)[0]} foydalanuvchini qo'shgan.")
