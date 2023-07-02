from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Начало работы бота'),
        BotCommand(command='/help', description='Список команд бота'),
        BotCommand(command='/info', description='Информация о технологии переноса стиля'),
        BotCommand(command='/transfer_style', description='Перенос стиля'),
        BotCommand(command='/examples', description='Примеры изображений'),
    ]

    await bot.set_my_commands(main_menu_commands)
