from aiogram import Router, Bot, F
from aiogram.types import Message, PhotoSize, FSInputFile, InputMediaPhoto
from aiogram.filters import Command, CommandStart
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from lexicon import LEXICON
from models.style_transfer import style_transfer
from handlers.FSMFillForm import FSMFillForm
from config import Config, load_config
from io import BytesIO
from models.VGG16 import TransformerNet
import torch


router: Router = Router()

# Define model and load model checkpoint
transformer = TransformerNet()
transformer.load_state_dict(torch.load('models/weights/last_checkpoint.pth', map_location=torch.device('cpu')))
transformer.eval()


# начало работы бота
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы отменили перенос стиля\n\n'
                              'Чтобы снова к переносу стиля - '
                              'отправьте команду /transfer_style')
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы не запускали перенос стиля\n\n'
                              'Чтобы перейти к переносу стиля  - '
                              'отправьте команду /transfer_style')


# вызов справки
@router.message(Command(commands=['help']), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


# вызов справки
@router.message(Command(commands=['info']), StateFilter(default_state))
async def process_info_command(message: Message):
    await message.answer(text=LEXICON['/info'])


# перенос стиля
@router.message(Command(commands=['transfer_style']), StateFilter(default_state))
async def process_transfer_style_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, загрузите фото')
    await state.set_state(FSMFillForm.upload_photo)


@router.message(StateFilter(FSMFillForm.upload_photo),
                F.photo[-1].as_('largest_photo'))
async def process_upload_photo(message: Message):
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token)
    file = await bot.download(message.photo[-1])
    b = BytesIO()
    b.write(file.read())
    with open('imgs/content.png', 'wb') as f:
        f.write(b.getvalue())
    await message.answer('Фото загружено!)')

    style_transfer('imgs/content.png', 'imgs/output.png', transformer)

    output = [InputMediaPhoto(type='photo', media=FSInputFile('imgs\output.png'))]

    await message.answer_media_group(media=output)
    await message.answer('Вот фото в переносе стиля!)')


# отправка примеров изображений переноса стиля
@router.message(Command(commands=['examples']), StateFilter(default_state))
async def sed_photo_examples(message: Message):
    photo_cat = InputMediaPhoto(type='photo', media=FSInputFile('imgs\cat.jpg'))
    photo_coty = InputMediaPhoto(type='photo', media=FSInputFile('imgs\city.jpg'))
    photo_zebras = InputMediaPhoto(type='photo', media=FSInputFile('imgs\zebras.jpg'))

    imgs = [photo_cat, photo_coty, photo_zebras]

    await message.answer_media_group(media=imgs)
