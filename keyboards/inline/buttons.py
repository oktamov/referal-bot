from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import url_yaml


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
