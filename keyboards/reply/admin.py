from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def reply_keyboard_for_admin():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊Statistika"), KeyboardButton(text="📤Reklama")],
            [KeyboardButton(text="📌Majburiy Obuna")],
            [KeyboardButton(text="✏️Minimal chiqarish narx ni tahrirlash")],
            [KeyboardButton(text="✏️Pul berish summa ni tahrirlash")],
            [KeyboardButton(text="✏️To\'lov kanalni ni tahrirlash")],
        ],
        resize_keyboard=True,
    )
    return keyboard


def majburiy_obuna():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Kanal qo'shish"), KeyboardButton(text="➖ Kanal o'chrish")],
            [KeyboardButton(text="👁‍🗨 Majburiy kanallarni ko'rish"),KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button