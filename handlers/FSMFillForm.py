from aiogram.filters.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    upload_photo = State()
