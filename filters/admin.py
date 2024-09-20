from aiogram.filters import BaseFilter, Filter
from aiogram.types import Message

from data.config import ADMINS


class IsBotAdminFilter(BaseFilter):
    def __init__(self, user_ids: list):
        self.user_ids = user_ids

    async def __call__(self, message: Message) -> bool:
        admin_ids_int = [int(id) for id in self.user_ids]
        return int(message.from_user.id) in admin_ids_int


class IsBotAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in ADMINS
