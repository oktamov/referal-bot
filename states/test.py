from aiogram.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
    set_url = State()
    set_min = State()
    set_pul = State()
    set_kanal = State()
    set_vote = State()


class ReferalForm(StatesGroup):
    CARD = State()
    END = State()


class FilmAddStates(StatesGroup):
    kod = State()
    chekk = State()
    film_id = State()
    url = State()
    chat_id = State()
    delete_kanal = State()
    content = State()
    ask_ad_content = State()
    file_name = State()
