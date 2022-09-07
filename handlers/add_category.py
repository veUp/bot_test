import database
from bot_create import bot,dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
import logging

logger = logging.getLogger('app.handlers.add_category')
logger.info('In add_category')

lst = ['отмена','/отмена','cancel','/cancel']
class Add_category(StatesGroup):
    name_types = State()
    name = State()
    image = State()
    summa = State()

async def add(message: types.Message):
    marks = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = types.KeyboardButton('Овощи')
    button2 = types.KeyboardButton('Фрукты')
    button3 = types.KeyboardButton('Мясо')
    button4 = types.KeyboardButton('Напитки')
    marks.add(button4, button3, button1, button2)
    await message.answer('Выберите категорию',reply_markup=marks)
    await Add_category.name_types.set()

@dp.message_handler(lambda msg: msg.text.lower() in lst,state='*')
async def cancel(message:types.Message,state:FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отмена действия')

@dp.message_handler(state=Add_category.name_types)
async def load_type_name(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        mark = types.ReplyKeyboardRemove()
        data['type_name'] = message.text
        await Add_category.next()
        await message.reply('Введите название продукта',reply_markup=mark)

@dp.message_handler(state=Add_category.name)
async def load_name(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text.lower()
        await Add_category.next()
        await message.reply('Отправьте фотографию')

@dp.message_handler(content_types=['photo'],state=Add_category.image)
async def load_photo(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['image'] = message.photo[0].file_id
        await Add_category.next()
        await message.reply('Напишите сумму за единицу')

@dp.message_handler(state=Add_category.summa)
async def load_summa(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['summa'] = float(message.text)
        data = (tuple(data.values()))
        a = database.Magazine(data)
        check = a.add_subject_in_magazine()
        if check !='Продукт уже такой создан':
            await message.answer('Записись удачна')
        else:
            await message.answer('Имя продукта уже создано')
        await state.finish()


def registration_add(dp):
    dp.register_message_handler(add,lambda msg: msg.text == 'Добавить категорию')
