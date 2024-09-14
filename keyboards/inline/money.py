from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_money():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Pulni chiqarib olish💸", callback_data="pul_chiqarib_olish")]
        ]
    )
    return button


def ha_yoq():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ha✅", callback_data="Ha"),
         InlineKeyboardButton(text="Yo'q❌", callback_data="Yoq")]
    ])
    return markup


def qabul_qilish(user_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'tkazildi✅", callback_data=f"otkazildi_{user_id}"),
         InlineKeyboardButton(text="Bekor qilish❌", callback_data=f"bekor_qilindi_{user_id}")]
    ])
    return markup


def ha_yoq_chegirma():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ha✅", callback_data="ha_chegirma"),
         InlineKeyboardButton(text="Yo'q❌", callback_data="yoq_chegirma")]
    ])
    return markup
