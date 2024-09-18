from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from utils.db.sqlite import Database
from data.config import BOT_TOKEN

db = Database()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
