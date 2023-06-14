from aiogram import Router
from aiogram.types import Message
from lexicon import LEXICON

router: Router = Router()


@router.message()
async def send_message(message: Message):
    await message.answer(text=LEXICON['other_answer'])
