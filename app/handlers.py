from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import logging
import pathlib

from app import database
from app import keyboards


class GetDataFile(StatesGroup):
    waiting_for_send_file = State()


async def get_file_start(message: types.Message, state: FSMContext):
    '''
    Функция запрашивает отправку файла с данными и ожидает.
    '''    
    await state.set_state(GetDataFile.waiting_for_send_file.state)
    await message.answer('Отправь файл с данными: ', reply_markup=types.ReplyKeyboardRemove())
    logging.info('Asking data file...')

async def get_file(message: types.Message, state: FSMContext):
    '''
    Функция проверяет полученный файл, если он валидный, то сохраняет его.
    Если файл не валиден, то запрашивает повторную отправку.
    '''
    try:
        if message.document.file_name.split('.')[-1] == 'xlsx':
            await message.document.download(destination_file=pathlib.Path('data', 'Combo.xlsx'))
            logging.info('Data file was downloaded')
            database.make_db()
            await message.answer('Обновил, спасибо', 
                                 reply_markup=keyboards.get_brand_kb())
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
        """Привет! Тут ты можешь уточнить прайс по 
        акции <b>Combo</b> на действующую матрицу 
        смартфонов. Приятного пользования\n\n
        <i>Выбери раздел:</i>""", 
        reply_markup=keyboards.get_main_kb())


async def cmd_cancel(message: types.Message, state: FSMContext):
    '''
    Функция отменяет все действия пользователя
    '''
    await state.finish()
    await message.answer('Действие отменено\n<i>Выбери раздел:</i>', 
                         reply_markup=keyboards.get_main_kb())


async def combo_phones(message: types.Message, state: FSMContext):
    await message.answer('<i>Выбери бренд:</i>', reply_markup=keyboards.get_brand_kb())


async def brands(message: types.Message, page=0):
    match message.text.lower():
        case 'itel':
            url = pathlib.Path('img', 'itel.jpg')
        case 'tecno':
            url = pathlib.Path('img', 'tecno.jpg')
        case 'oppo':
            url = pathlib.Path('img', 'oppo.jpeg')
        case 'infinix':
            url = pathlib.Path('img', 'infinix.jpg')
        case 'realme':
            url = pathlib.Path('img', 'realme.png')
        case 'xiaomi':
            url = pathlib.Path('img', 'xiaomi.jpg')
        case 'black fox':
            url = pathlib.Path('img', 'black fox.jpg')
        case 'назад':
            await message.answer('<i>Выбери раздел:</i>', reply_markup=keyboards.get_main_kb())
    try:
        with open(url, 'rb') as photo:
            await message.answer_photo(photo=photo, 
                                    reply_markup=keyboards.get_model_ikb(data=message.text)
                                    )
    except UnboundLocalError:
        logging.info('Action was canceled')
        

async def show_combo(callback: types.CallbackQuery):
    data = callback.data

    check = f"<b>Состав чека:</b>\n\
            <i>{data}  {database.get_price(data)} руб.\n\
            Страховка  {database.get_insurance(data)} руб.\n\
            Sim-карта  2150 руб.</i>\n\n Сумма по акции <b> {database.get_combo(data)} руб.</b>"
    await callback.message.answer(text=check)
    await callback.answer()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, 
                                commands=['start'], 
                                state='*'
                                )
    dp.register_message_handler(cmd_cancel, 
                                commands=['cancel'], 
                                state='*'
                                )
    dp.register_message_handler(cmd_cancel, 
                                Text(equals='отмена', 
                                     ignore_case=True), 
                                state='*'
                                )

    
def register_handlers_file(dp: Dispatcher):
    dp.register_message_handler(get_file_start, 
                                commands=['update_file'], 
                                state='*'
                                )
    dp.register_message_handler(get_file, 
                                content_types=types.ContentTypes.ANY, 
                                state=GetDataFile.waiting_for_send_file
                                )


def register_handlers_brands(dp: Dispatcher):
    dp.register_message_handler(combo_phones, Text(equals='combo',
                                                   ignore_case=True), 
                                                   state='*')
    dp.register_message_handler(brands, state='*')


def register_callback_handler(dp: Dispatcher):
    dp.register_callback_query_handler(show_combo)