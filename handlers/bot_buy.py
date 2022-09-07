from aiogram import types
from bot_create import bot, dp
import database
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
import logging

logger = logging.getLogger('app.handlers.bot_buy')
logger.info('In bot_buy')

class Buy(StatesGroup):
    amount = State()

async def menu_buy(message:types.Message):
    marks = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = types.KeyboardButton('Овощи')
    button2 = types.KeyboardButton('Фрукты')
    button3 = types.KeyboardButton('Мясо')
    button4 = types.KeyboardButton('Напитки')
    button6 = types.KeyboardButton('Добавить категорию')
    button5 = types.KeyboardButton('В главное меню')
    marks.add(button4, button3, button1, button2, button5, button6)
    await bot.send_message(message.chat.id, 'ВИТРИНА', reply_markup=marks)

lst = ['Овощи','Фрукты','Мясо','Напитки']
@dp.message_handler(lambda msg: msg.text in lst)
async def vegetables(message: types.Message):
    name = message.text
    start = database.Magazine(type_name=name)
    veg = start.get_info_from_magazine()
    while True:
        x = veg.fetchone()
        if x is None:
            await bot.send_message(message.from_user.id, f'КАТЕГОРИЯ " {name.upper()} "\nПУСТО')
            break
        else:
            button = types.InlineKeyboardButton('Купить', callback_data=f'button {x[1]}')
            marks = types.InlineKeyboardMarkup().add(button)
            await bot.send_message(message.from_user.id, f'\nТип: {x[0]}\nНазвание: {x[1]}')
            await bot.send_photo(message.from_user.id, photo=x[2])
            await bot.send_message(message.from_user.id, f'Цена: {x[3]}Р', reply_markup=marks)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('button '),state=None)
async def call(callback: types.CallbackQuery):
    global name_sub
    name_sub = callback.data.split(' ')[1:]
    await callback.message.answer('Напишите количество, целочисленное')
    await callback.answer()
    await Buy.amount.set()

@dp.message_handler(lambda message: not message.text.isdigit(), state=Buy.amount)
async def process_age_invalid(message: types.Message):
    return await message.reply("Неверное количество")

@dp.message_handler(lambda message: int(message.text)<=0, state=Buy.amount)
async def process_age_invalid(message: types.Message):
    return await message.reply("Не может меньше или равен 0!")

@dp.message_handler(state=Buy.amount)
async def amont_set(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        dt = message.text
        try:
            dt = int(dt)
            data['amont'] = message.text
            print(dt)
            by = database.Magazine(name=name_sub)
            amount = by.buy() # цена продукта
            all_money = int(*amount) * dt
            print(message.from_user.id)
            a = database.Data_user(ID=message.from_user.id)
            info = a.edit_summa_amount(total_money=all_money,summ=dt)
            if info == 'Не хватает денег.':
                await message.answer('Не хватает денег.')
                await menu_buy(message)
            else:
                await message.answer('Покупка совершена!')

            await state.finish()
        except Exception as err:
            print(err)


def registration_buy(dp):
    dp.register_message_handler(menu_buy, lambda msg: msg.text == 'Купить продукты')