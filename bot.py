from bot_create import dp
from handlers import bot_client,bot_buy
from aiogram.utils import executor
from handlers import add_category
from aiogram import types
import logging

FORMAT = '%(asctime)s :: %(name)s:%(lineno)s :: %(levelname)s :: %(message)s'
logging.basicConfig(filename='logs/log_test.log',
                    format=FORMAT,
                    level=logging.DEBUG,
                    )
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(FORMAT))
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)

add_category.registration_add(dp)
bot_client.registration_client(dp)
bot_buy.registration_buy(dp)


@dp.message_handler()
async def warning(message:types.Message):
    await message.answer('Нет такой команды:(\nНажмите на /help')
    await message.delete()

if "__main__" == __name__:
    logging.info('Start bot')
    executor.start_polling(dp,skip_updates=True)
    logging.info('Stop bot')
