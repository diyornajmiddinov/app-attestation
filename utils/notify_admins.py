import logging

from aiogram import Bot


async def on_startup_notify(bot: Bot):
    try:
        await bot.send_message(5351489385, "Bot ishga tushdi")
    except Exception as err:
        logging.exception(err)
