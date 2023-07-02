from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.filters import Command, CommandStart
from lexicon import LEXICON
from models.style_transfer import style_transfer
from config import Config, load_config
from io import BytesIO

router: Router = Router()


#начало работы бота
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])


#вызов справки
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


# вызов справки
@router.message(Command(commands=['info']))
async def process_info_command(message: Message):
    await message.answer(text=LEXICON['/info'])


# перенос стиля
@router.message(Command(commands=['transfer_style']))
async def process_transfer_style(message: Message):
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token)
    file = await bot.download(message.photo[-1])
    b = BytesIO()
    b.write(file.read())
    with open('imgs/content.png', 'wb') as f:
        f.write(b.getvalue())

    style_transfer('imgs/content.png', 'imgs/output.png', 'models/weights/last_checkpoint.pth')
    output = FSInputFile('imgs\output.jpg')

    await message.answer_photo(output)


# отправка примеров изображений переноса стиля
@router.message(Command(commands=['examples']))
async def sed_photo_examples(message: Message):
    photo_cat = InputMediaPhoto(type='photo', media=FSInputFile('imgs\cat.jpg'))
    photo_coty = InputMediaPhoto(type='photo', media=FSInputFile('imgs\city.jpg'))
    photo_zebras = InputMediaPhoto(type='photo', media=FSInputFile('imgs\zebras.jpg'))

    imgs = [photo_cat, photo_coty, photo_zebras]

    await message.answer_media_group(media=imgs)
