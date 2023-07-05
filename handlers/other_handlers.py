from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from lexicon import LEXICON

router: Router = Router()


@router.message(StateFilter(default_state))
async def send_message(message: Message):
    await message.answer(text=LEXICON['other_answer'])
