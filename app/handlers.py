from aiogram import Dispatcher, types
from aiogram.utils.markdown import hide_link, hlink
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import logging

from app import make_data


kb = [
    [types.KeyboardButton(text='Tecno'), 
     types.KeyboardButton(text='Oppo'),
     types.KeyboardButton(text='Itel')
     ],

     [types.KeyboardButton(text='Infinix'),
     types.KeyboardButton(text='Realme'),
     types.KeyboardButton(text='Xiaomi')],

     [types.KeyboardButton(text='Black Fox')]
    ]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True
)


class GetDataFile(StatesGroup):
    waiting_for_send_file = State()


class Brands(StatesGroup):
    choose_brand = State()


async def get_file_start(message: types.Message, state: FSMContext):
    '''
    Функция запрашивает отправку файла с данными и ожидает.
    '''    
    await state.set_state(GetDataFile.waiting_for_send_file.state)
    await message.answer('Отправь файл с данными: ', reply_markup=types.ReplyKeyboardRemove())

async def get_file(message: types.Message, state: FSMContext):
    '''
    Функция проверяет полученный файл, если он валидный, то меняет состояние.
    Если файл не валиден, то запрашивает повторную отправку.
    '''
    try:
        if message.document.file_name.split('.')[-1] == 'xlsx':
            await message.document.download(destination_file='Combo.xlsx')
            logging.info('Data file was downloaded')
            await message.answer('Обновил, спасибо', 
                                 reply_markup=types.ReplyKeyboardMarkup(kb, resize_keyboard=True))
            await state.finish()
        else:
            await message.answer('Отправь файл с данными')
    except Exception as ex:
        logging.info(ex)
        await message.answer('Мне нужен файл')


async def cmd_start(message: types.Message, state: FSMContext):
    '''
    Функция отправляет приветственное сообщение и включает клавиатуру
    '''
    await state.finish()

    await message.answer(
        "Привет! Тут ты можешь уточнить прайс по акции <b>Combo</b> на действующую матрицу смартфонов. Приятного пользования\n\n<i>Выбери раздел:</i>", 
        reply_markup=keyboard)


async def cmd_cancel(message: types.Message, state: FSMContext):
    '''
    Функция отменяет все действия пользователя
    '''
    await state.finish()
    await message.answer('Действие отменено', reply_markup=keyboard)


async def brands(message: types.Message, state: FSMContext):
    await state.set_state(Brands.choose_brand.state)

    text = ''
    i = 0
    for phone in make_data.telephones:
        if message.text.lower() == phone[0].lower():
            text += f'/{i}  {phone[1]}\n'
            i += 1

    match message.text.lower():
        case 'itel':
            url = 'https://mobitrends.co.ke/wp-content/uploads/2018/04/iTel-Logo.jpg'
        case 'tecno':
            url = 'https://www.nairaland.com/attachments/14066211_screenshot20210819141622_jpeg2eb5a55728c4095bd2c96d414c18a2f7'
        case 'oppo':
            url = 'https://aitnews.com/wp-content/uploads/2020/04/0.jpeg'
        case 'infinix':
            url = 'https://www.pinoytechnoguide.com/wp-content/uploads/2020/09/infinix-logo.jpg'
        case 'realme':
            url = 'https://seeklogo.com/images/R/realme-logo-8D20880530-seeklogo.com.png'
        case 'xiaomi':
            url = 'https://static.startuptalky.com/2021/05/Xiaomi_logo_startuptalky.png'
        case 'black fox':
            url = 'https://i.ytimg.com/vi/TtTe7pIpruA/hqdefault.jpg'

    await message.answer(f'{text} {hide_link(url)}')

    await state.finish()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(cmd_cancel, commands=['cancel'], state='*')
    dp.register_message_handler(cmd_cancel, Text(equals='отмена', ignore_case=True), state='*')

    
def register_handlers_file(dp: Dispatcher):
    dp.register_message_handler(get_file_start, commands=['update_file'], state='*')
    dp.register_message_handler(get_file, content_types=types.ContentTypes.ANY, state=GetDataFile.waiting_for_send_file)


def register_handlers_brands(dp: Dispatcher):
    dp.register_message_handler(brands, state=None)