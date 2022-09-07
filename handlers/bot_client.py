from aiogram import types, Dispatcher
from bot_create import bot, dp
import database

async def menu(message):
    if message.chat.id == 671924527:
        marsk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=10)
        button1 = types.KeyboardButton('Мой кошелек')
        button2 = types.KeyboardButton('Купить продукты')
        button3 = types.KeyboardButton('Админ панель')
        marsk.add(button1,button2,button3)
        await bot.send_message(message.chat.id, '⬇️⬇️⬇️', reply_markup=marsk)
    else:
        marsk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=10, one_time_keyboard=True)
        button1 = types.KeyboardButton('Мой кошелек')
        button2 = types.KeyboardButton('Купить продукты')
        marsk.add(button1, button2)
        await bot.send_message(message.chat.id, '⬇️⬇️⬇️', reply_markup=marsk)

async def start(message : types.Message):
   await bot.send_message(message.from_user.id,f'Привет, <b> {message.from_user.first_name} </b>! \n\nДобро пожаловать в продуктовый магазин <b>"Дядя Костя"!</b>',
                     parse_mode='html')
   await menu(message)

async def walter(message:types.Message):
    get = database.Data_user(message.from_user.id, message.from_user.first_name)
    st = get.get_info_user_table()
    await bot.send_message(message.chat.id,
                     f'🆔 ID: {st[1]}\nИмя: {st[0]}\nБаланс: {st[2]} Р\nСовершено покупок: {st[3]}')

async def admin(message:types.Message):
    marks = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Редактирование пользователя')
    button2 = types.KeyboardButton('...')
    button3 = types.KeyboardButton('В главное меню')
    marks.add(button1, button2, button3)
    await bot.send_message(message.chat.id, '⬇️⬇️⬇️', reply_markup=marks)


def registration_client(dp: Dispatcher):
    dp.register_message_handler(start,commands=['start','help'])
    dp.register_message_handler(walter, lambda msg: msg.text == 'Мой кошелек')
    dp.register_message_handler(menu, lambda msg: msg.text == 'В главное меню')
    dp.register_message_handler(admin, lambda msg: msg.text == 'Админ панель' and msg.chat.id ==671924527)
