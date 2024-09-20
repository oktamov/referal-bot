from typing import Union

from aiogram import types, Router, F
from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message

from loader import db

router = Router()


class ChatGroupFilter(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == ChatType.GROUP or message.chat.type == ChatType.SUPERGROUP


@router.message(F.chat.type.in_({"group", "supergroup"}))
async def on_new_member(message: types.Message):
    for new_member in message.new_chat_members:
        inviter_id = message.from_user.id
        group_id = message.chat.id

        db.add_or_update_group_member(group_id, inviter_id)

        await message.answer(f"{message.from_user.full_name} guruhga {new_member.full_name} ni qo'shdi.")
        await message.answer(
            f"{message.from_user.full_name} hozirgacha {db.get_user_add_count(group_id, inviter_id)[0]} foydalanuvchini qo'shgan.")
