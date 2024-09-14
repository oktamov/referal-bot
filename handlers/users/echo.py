from aiogram import Router, types

from keyboards.inline.buttons import url_button

router = Router()


@router.message()
async def start_user(message: types.Message):
    await message.answer(f"Ovoz bering👇", reply_markup=url_button())
