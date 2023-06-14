from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, Text, CommandStart
from lexicon import LEXICON

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])


@router.message(Command(commands=['help']))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands=['transfer_style']))
async def process_transfer_style(message: Message):
    await message.answer(text=LEXICON['/transfer_style'])
