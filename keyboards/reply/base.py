from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data.config import url_yaml


def bekor_qilish_keyboard():
    button = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True
    )
    return button



def pul_ishlash():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Referal havola📎"), KeyboardButton(text="Balans💵")],
            [KeyboardButton(text="To'lov kanali📜"), KeyboardButton(text="Pul chiqarish💰")],
        ],
        resize_keyboard=True,
    )
    return keyboard


