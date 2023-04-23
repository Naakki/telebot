from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

import math
import logging
import sqlite3


def get_main_kb():
    kb = [
        [KeyboardButton(text='Combo'),
         KeyboardButton(text='Настройки')]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    return keyboard


def get_brand_kb():
    kb = [
    [KeyboardButton(text='Tecno'), 
     KeyboardButton(text='Oppo'),
     KeyboardButton(text='Itel')
     ],

     [KeyboardButton(text='Infinix'),
     KeyboardButton(text='Realme'),
     KeyboardButton(text='Xiaomi')],

     [KeyboardButton(text='Black Fox')],

     [KeyboardButton(text='Назад')]
    ]
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    return keyboard


def get_model_ikb(data, page=0):
    i_keyboard = InlineKeyboardMarkup()    
    phones = []

    with sqlite3.connect('data\combo.db') as db:
        cur = db.cursor()
        models = cur.execute("SELECT * FROM phones WHERE brand=?", (data,))

    for model in models:
        i_keyboard.add(InlineKeyboardButton(text=f'{model[1]}', callback_data=f'{model[1]}'))

    max_page = math.ceil(len(phones) / 5)

    if page < 0:
        page = 0
    elif page > max_page:
        page = max_page

    # for i, phone in enumerate(phones):
    #     if (5 * page <= i) and (5 * (page + 1) > i):
    #         i_keyboard.add(InlineKeyboardButton(f'{phone}', callback_data='calculate'))

    # if len(phones) > 5:        
    #     i_keyboard.add(InlineKeyboardButton('<', callback_data='prev'), 
    #                    InlineKeyboardButton('>', callback_data='next'))

    return i_keyboard
