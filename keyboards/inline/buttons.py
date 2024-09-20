from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import url_yaml, get_channels
from loader import db


def yes_no_keyboard(key):
    if key == 'url':
        inline_keyboard = [[
            InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
            InlineKeyboardButton(text="❌ No", callback_data='no')
        ]]
    elif key == 'min':
        inline_keyboard = [[
            InlineKeyboardButton(text="✅ Yes", callback_data='yes_min'),
            InlineKeyboardButton(text="❌ No", callback_data='no_min')
        ]]
    elif key == 'kanal':
        inline_keyboard = [[
            InlineKeyboardButton(text="✅ Yes", callback_data='yes_kanal'),
            InlineKeyboardButton(text="❌ No", callback_data='no_kanal')
        ]]
    elif key == 'vote':
        inline_keyboard = [[
            InlineKeyboardButton(text="✅ Yes", callback_data='yes_vote'),
            InlineKeyboardButton(text="❌ No", callback_data='no_vote')
        ]]

    else:
        inline_keyboard = [[
            InlineKeyboardButton(text="✅ Yes", callback_data='yes_pul'),
            InlineKeyboardButton(text="❌ No", callback_data='no')
        ]]
    are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return are_you_sure_markup


def url_button():
    inline_keyboard = [[
        InlineKeyboardButton(text="Ovoz berish", url=f'{url_yaml["url"]}'),
    ]]
    are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return are_you_sure_markup


def subscribe_keyboard_invited(user_id):
    channels = db.get_all_channels()
    inline_keyboard = []

    for sanoq, channel in enumerate(channels, start=1):
        button = InlineKeyboardButton(text=f"{sanoq} - kanal", url=channel[2])
        inline_keyboard.append([button])

    inline_keyboard.append([
        InlineKeyboardButton(text="Obuna bo'ldim✅", callback_data=f"subscribe_true_{user_id}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def subscribe_keyboard():
    channels = db.get_all_channels()
    inline_keyboard = []

    for sanoq, channel in enumerate(channels, start=1):
        button = InlineKeyboardButton(text=f"{sanoq} - kanal", url=channel[2])
        inline_keyboard.append([button])

    inline_keyboard.append([
        InlineKeyboardButton(text="Obuna bo'ldim✅", callback_data="subscribe_true")
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
