from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/start', description='Начало работы бота')
    ]

    await bot.set_my_commands(main_menu_commands)