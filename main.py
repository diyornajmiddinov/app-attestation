import asyncio
import logging

from data.loader import dp, bot, router
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


async def main() -> None:
    import handlers
    dp.include_router(router=router)
    await on_startup_notify(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    asyncio.run(main())
