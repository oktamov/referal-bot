from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def reply_keyboard_for_admin():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊Statistika"), KeyboardButton(text="📤Reklama")],
            # [KeyboardButton(text="✏️Url ni tahrirlash")],
            [KeyboardButton(text="✏️Minimal chiqarish narx ni tahrirlash")],
            [KeyboardButton(text="✏️Pul berish summa ni tahrirlash")],
            [KeyboardButton(text="✏️To\'lov kanalni ni tahrirlash")],
            # [KeyboardButton(text="✏️Bir ovozga pul berishni tahrirlash")],
        ],
        resize_keyboard=True,
    )
    return keyboard
