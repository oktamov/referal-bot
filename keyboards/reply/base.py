from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data.config import url_yaml


def bekor_qilish_keyboard():
    button = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True
    )
    return button


# def pul_ishlash():
#     button = ReplyKeyboardMarkup
#     referal = KeyboardButton(text="Referal havola📎")
#     balans = KeyboardButton(text="Balans💵")
#     orqaga = KeyboardButton(text="⬅️ Orqaga")
#     button.row(referal, balans)
#     button.add(orqaga)
#     return button


def pul_ishlash():
    kanal = url_yaml.get('tolov_kanal', None)
    if kanal:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🗳 Ovoz berish")],
                [KeyboardButton(text="Referal havola📎"), KeyboardButton(text="Balans💵")],
                [KeyboardButton(text="To'lov kanali📜")],
            ],
            resize_keyboard=True,
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🗳 Ovoz berish")],
                [KeyboardButton(text="Referal havola📎"), KeyboardButton(text="Balans💵")],
            ],
            resize_keyboard=True,
        )
    return keyboard


