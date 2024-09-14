from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext

from data.config import url_yaml
from keyboards.inline.buttons import url_button
from keyboards.reply.base import pul_ishlash
from loader import db
from utils.extra_datas import make_title

router = Router()


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
    else:
        msg = f"[{make_title(full_name)}](tg://user?id={telegram_id}) bazaga oldin qo'shilgan."

    await message.answer(f"Assalomu alaykum {full_name} ", reply_markup=pul_ishlash())
    await message.answer(
        f"Bot orqali open budjetga ovoz berib\nHar bir ovozingiz uchun {url_yaml['vote_credit']} so'mdan ishlab oling👇",
        reply_markup=url_button())
