import random 
import os
import string
import re

from setting import *
from database import database as db

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import asyncio
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import CommandStart, Command

from handlers import index, langueage_reew, globalMenu

from datetime import datetime, time

from aiogram import BaseMiddleware


Start_dp  = Router()

time_user = datetime.now().time()

print(time_user)

class Form(StatesGroup):
    user_id = State()
    name = State()
    age = State()  #- вік пошука партнера 
    gender = State()  #- гендер  
    topic_chat = State()  #- темат діалога 
    bio = State()
    search_gender = State() #- пошук гендера партнера 
    partner_age_range = State() #- вік пошука партнера 
    location = State()  #- локація 
    username = State()  #- username 
    photo_user = State()  #- фото 
    confirm_profiler = State()

@Start_dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext, current_language: str):
    await db.db_bot.cmd_start_db(message.from_user.id)

    chat_id = message.chat.id

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):


        if chat_id in user_dict and 'location' in user_dict[chat_id]:
            await globalMenu.display_menu_global(message, state, current_language)
        else:
            kb_list = [
                [InlineKeyboardButton(text=langueage_reew.translations[current_language]['change_lan'], callback_data="error_messages"), InlineKeyboardButton(text=langueage_reew.translations[current_language]['game'], url="https://t.me/reewua")],
                [InlineKeyboardButton(text=langueage_reew.translations[current_language]['create_acck'], callback_data="create_profile")]
            ] 
            kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

        
            await message.answer(text=langueage_reew.translations[current_language]['start'], reply_markup=kb)
            await state.set_state(Form.user_id)


@Start_dp.callback_query(lambda c: c.data == "create_profile", Form.user_id)
async def callback_query(call: CallbackQuery, state: FSMContext, current_language: str):
    async with ChatActionSender.typing(bot=bot, chat_id = call.message.chat.id): 
        await asyncio.sleep(2)
    chat_id = call.message.chat.id

    time_now = datetime.now().time()
    thous_check = time(18, 0)
    end_time = time(5, 0)
    
    current_state = await state.get_state()

    if chat_id not in user_dict:
        if thous_check >= time_now <= end_time:
            getting_id = string.ascii_letters + string.digits
            user_id = ''.join([random.choice(getting_id) for __ in range(8)])

            user_dict[chat_id] = {'user_id': user_id}
            keyboard = types.ReplyKeyboardRemove()
            await call.message.answer(text=langueage_reew.translations[current_language]['name_evening'], reply_markup=keyboard)  
            await state.update_data(user_id=user_id)
            await state.set_state(Form.name)
        else:
            getting_id = string.ascii_letters + string.digits
            user_id = ''.join([random.choice(getting_id) for __ in range(8)])

            user_dict[chat_id] = {'user_id': user_id}

            print(f"User_id: {user_id}, {chat_id}")
            keyboard = types.ReplyKeyboardRemove()
            await call.message.answer(text=langueage_reew.translations[current_language]['name'] , reply_markup=keyboard)  
            await state.update_data(user_id=user_id)
            await state.set_state(Form.name)
    else:

        if current_state == Form.user_id:
            await call.message.answer("Не виконуйте інших команд, як вас звати")  
            await state.set_state(Form.name)
        if current_state == Form.age:
            await call.message.answer("Не виконуйте інших команд, скільки років вам")  
            await state.set_state(Form.gender)

@Start_dp.message(F.text, Form.name)
async def process_name_step(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    name = message.text


    if not name.isalpha():
        await message.answer("Будь ласка, напишіть імя коректно без цифр")
        return
    
    print(f'{name}')
    await state.update_data(name=name)
    await db.db_bot.data_name(chat_id=chat_id, name=name)

    if chat_id in user_dict:
        user_dict[chat_id]['name'] = name


    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):    
        await message.answer(text=langueage_reew.translations[current_language]['age_lg'])
        await state.set_state(Form.age)

@Start_dp.message(F.text, Form.age)
async def process_age_step(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    age_text = message.text.strip()

    if chat_id in user_dict:
        if not age_text.isdigit():
            await message.answer(text=langueage_reew.translations[current_language]['сorrect_age'])
            return
        else:
            user_dict[chat_id]['age'] = age_text
        
        if int(age_text) <= 13:
            await message.answer(text=langueage_reew.translations[current_language]['small_age'])
            del user_dict[chat_id]
            return

        
        if int(age_text) >= 101:
            await message.answer(text=langueage_reew.translations[current_language]['request_correct'])
            return

        user_dict[chat_id]['age'] = age_text
        await state.update_data(age=age_text)


        set_key = ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True,
                    keyboard= [
                                            [   
                                                KeyboardButton(text=langueage_reew.translations[current_language]['boy']), 
                                                KeyboardButton(text=langueage_reew.translations[current_language]['girl'])
                                            ]
                                            ])
        

        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(1)
            await message.answer(text=langueage_reew.translations[current_language]['choose_gender'], reply_markup=set_key)
            await state.set_state(Form.gender)

@Start_dp.message(F.text, Form.gender)
async def process_gender(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    gender_text = message.text

    if chat_id in user_dict:

        if gender_text == langueage_reew.translations[current_language]['boy']:
            user_dict[chat_id]['gender'] = gender_text  # Store gender in user_dict
            await state.set_state(Form.topic_chat)
        elif gender_text == langueage_reew.translations[current_language]['girl']:
            user_dict[chat_id]['gender'] = gender_text  # Store gender in user_dict
            await state.set_state(Form.topic_chat)
        else:
            await message.answer(f"Будь ласка, оберіть одну з варіантів ('{langueage_reew.translations[current_language]['boy']}' або '{langueage_reew.translations[current_language]['girl']}').")
            return
    print(f'User id: {chat_id} ')
    print(f'Gen der: {user_dict[chat_id].get("gender")}  ')  # Corrected line using .get() method


    text_topic = (f"<b>{langueage_reew.translations[current_language]['choose_topic']}</b>\n\n"
                        f"<b>{langueage_reew.translations[current_language]['selected_topic_but1']}</b> - {langueage_reew.translations[current_language]['selected_topic']}\n\n"
                        f"<b>{langueage_reew.translations[current_language]['selected_topic_but2']}</b> - {langueage_reew.translations[current_language]['selected_topic2']}"
                        )
            

    set_key = ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True,
                                        keyboard= [
                                            [   
                                                KeyboardButton(text=langueage_reew.translations[current_language]['selected_topic_but1']), 
                                                KeyboardButton(text=langueage_reew.translations[current_language]['selected_topic_but2'])
                                            ]
                                            ])
            
        
    await message.answer(text_topic, reply_markup=set_key, parse_mode="HTML")

@Start_dp.message(F.text, Form.topic_chat)
async def process_selected_topic(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id        
    selected_topic = message.text
    
    user_dict[chat_id]['topic_chat'] = selected_topic

    if selected_topic == langueage_reew.translations[current_language]['selected_topic_but1']:
        user_dict[chat_id]['topic_chat'] = langueage_reew.translations[current_language]['selected_topic_but1']
        keyboard = [
            [KeyboardButton(text=langueage_reew.translations[current_language]['skip'])],
        ]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)
        await message.answer(langueage_reew.translations[current_language]['bio'], reply_markup=keyboard)
        await state.set_state(Form.bio)
    elif selected_topic == langueage_reew.translations[current_language]['selected_topic_but2']:
        user_dict[chat_id]['topic_chat'] = langueage_reew.translations[current_language]['selected_topic_but2']

        if int(user_dict[chat_id]['age']) >= 18:
            keyboard = [
                [KeyboardButton(text=langueage_reew.translations[current_language]['skip'])],
            ]
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)
            await message.answer(langueage_reew.translations[current_language]['bio'], reply_markup=keyboard)
            await state.set_state(Form.bio)
        else:
            await message.answer(langueage_reew.translations[current_language]['flirt_18+_speak'])
            del user_dict[chat_id]['topic_chat']   
            await message.answer(langueage_reew.translations[current_language]['flirt_18_small'])
            await state.set_state(Form.topic_chat)
    else:
        await message.answer(langueage_reew.translations[current_language]['flirt_18_small'])
    return

@Start_dp.message(F.text, Form.bio)
async def button_bio_text(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    bio = message.text
    
    if chat_id not in user_dict:
        await message.answer("Не створивши профіль, ви не можете написати Біо.")
        return

    if bio == langueage_reew.translations[current_language]['skip']:
        user_dict[chat_id]['bio'] = ''
    else:
        user_dict[chat_id]['bio'] = bio
    

    keyboard_key = ReplyKeyboardMarkup(row_width= 2,resize_keyboard=True, 
                                   keyboard = [

                                    [KeyboardButton(text=langueage_reew.translations[current_language]['her']), KeyboardButton(text=langueage_reew.translations[current_language]['his'])],
                                    [KeyboardButton(text=langueage_reew.translations[current_language]['anything'])]
                                    ])
    
    await message.answer(langueage_reew.translations[current_language]['search_whom'], reply_markup=keyboard_key)
    await state.set_state(Form.search_gender)

@Start_dp.message(F.text, Form.search_gender)
async def process_bio_step(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    search_gender = message.text

    if chat_id not in user_dict:
        await message.answer("Не створивши профіль, ви не можете обрати хто вас цікавить.")
        return
    
    if search_gender == langueage_reew.translations[current_language]['her']:
        user_dict[chat_id]['search_gender'] = langueage_reew.translations[current_language]['her']  # Store gender in user_dict
        await state.set_state(Form.partner_age_range)
    elif search_gender == langueage_reew.translations[current_language]['his']:
        user_dict[chat_id]['search_gender'] = langueage_reew.translations[current_language]['his']  # Store gender in user_dict
        await state.set_state(Form.partner_age_range)
    else:
        await message.answer(f"{langueage_reew.translations[current_language]['interdiction']} ('{langueage_reew.translations[current_language]['her']}' {langueage_reew.translations[current_language]['or']} '{langueage_reew.translations[current_language]['her']}').")
        return

    user_dict[chat_id]['search_gender'] = search_gender
    await state.update_data(search_gender=search_gender)

    keyboard_key = ReplyKeyboardMarkup(row_width= 2,resize_keyboard=True, 
                                   keyboard = [

                                    [KeyboardButton(text='14-16'), KeyboardButton(text='16-18')],
                                    [KeyboardButton(text='18-20'), KeyboardButton(text='20-25')],

                                    ])


    await message.answer(langueage_reew.translations[current_language]['age_range'], reply_markup=keyboard_key)
    await state.set_state(Form.partner_age_range)


@Start_dp.message(lambda message: message.text in ['14-16', '16-18', '18-20', '20-25'], Form.partner_age_range)
async def process_age_search(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    partner_age_range = message.text.strip()

    if chat_id not in user_dict:
        await message.answer("Не створивши профіль, ви не можете обрати віковий діапазон.")
        return

    if chat_id in user_dict:
        if 'partner_age_range' not in user_dict[chat_id]:
            user_dict[chat_id]['partner_age_range'] = []

        partner_age_ranges = user_dict[chat_id]['partner_age_range']

        if partner_age_range not in partner_age_ranges:
            partner_age_ranges.append(partner_age_range)


        if len(partner_age_ranges) < 2:
            button_key = lambda text:f"✅ {text}" if text in partner_age_range else text

            text_partners = langueage_reew.translations[current_language]['ADD_ragne']

            keyboard_key = ReplyKeyboardMarkup(row_width= 2,resize_keyboard=True, 
                                                    keyboard = [

                                                        [KeyboardButton(text=button_key('14-16')), KeyboardButton(text=button_key('16-18'))],
                                                        [KeyboardButton(text=button_key('18-20')), KeyboardButton(text=button_key('20-25'))],
                                                        [KeyboardButton(text='Продовжити')]

                                                        ])
                        
            await message.answer(text_partners, reply_markup=keyboard_key)
        else:
            key_delete = ReplyKeyboardRemove()
            await message.answer("Дякую! З якого ви міста?", reply_markup=key_delete)
            await state.set_state(Form.location)
    else:
        await message.answer("Не виконуйте інших команд", reply_markup=key_delete)

@Start_dp.message(lambda message: message.text == "Продовжити")
async def next_step(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    partner_age_range = user_dict[chat_id]['partner_age_range']
    
    if partner_age_range:
        key_delete = ReplyKeyboardRemove()
        await message.answer(langueage_reew.translations[current_language]['city_was_born'], reply_markup=key_delete)
        await state.set_state(Form.location)

@Start_dp.message(F.text, Form.location)
async def process_location_step(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    location = message.text.strip()

    keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,

    keyboard= [[KeyboardButton(text=langueage_reew.translations[current_language]['share'])]])
                        
    user_dict[chat_id]['location'] = location  # Store location in user_dict
    await message.answer('Напишіть свій username або надішліть через кнопку Поділитися UN', reply_markup=keyboard_key)
    await state.set_state(Form.username)


@Start_dp.message(F.text, Form.username)
async def process_username(message: Message, state: FSMContext, current_language: str):
    await state.update_data(username=message.text)

    chat_id = message.chat.id
    username = message.text.strip()
    user = message.from_user.username

    key_button = [
        [InlineKeyboardButton(text="Туторіал", url="https://www.youtube.com/watch?v=hh2J0kR2rFw")]
        ]
    ks = InlineKeyboardMarkup(inline_keyboard=key_button)

    if not user:
        await message.answer('<b>У вас немає у профілі username</b>'
                             '\n\nЯк же додати username:\n'
                             '1. Зайдіть в налаштування\n'
                             '2. Змінити Профіль\n'
                             '3. Оберіть Імя користувача і впишіть будь який username\n\n'
                             'Якщо не хочете додавати свій username, пропустіть', parse_mode='HTML', reply_markup=ks)
        return
    
    if username == langueage_reew.translations[current_language]['share']:
        username = username.replace(langueage_reew.translations[current_language]['share'], user)
        user_dict[chat_id]['username'] = ''
        print(f'{username}, {user}')
    else:
        if username == '':
            print(f'{username}, {user}')
            user_dict[chat_id]['username'] = user
            await message.answer('ERRRO')
            return
        
    if username not in user or username == '':
        await message.answer(langueage_reew.translations[current_language]['Uncorrect_user'])
    else:
        kbs = types.ReplyKeyboardRemove()
        user_dict[chat_id]['username'] = username  # Store location in user_dict
        await message.answer(langueage_reew.translations[current_language]['share_photo'], reply_markup=kbs)
        await state.set_state(Form.photo_user)


@Start_dp.message(F.photo, Form.photo_user)
async def process_photo_user(message: types.Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id

    if chat_id in user_dict:
        user_id = user_dict[chat_id]['user_id'] 
        photo_path  = f'photos/{chat_id}.jpg'
        os.makedirs('photos', exist_ok=True)


        File  = await bot.get_file(message.photo[-1].file_id)

        await bot.download_file(File.file_path, destination=photo_path)

        profile_info = user_dict[chat_id]
        caption_text = (
                    f"{profile_info['name']}, {profile_info['age']}, {profile_info['location']}\n"
                    f"{profile_info['bio']}\n"
                )
    
        with open(photo_path, 'rb') as photo:
            await message.answer_photo(
                types.FSInputFile(path=photo_path), caption=caption_text
                )

        chech_face = await get_images(photo_path, message)
        
        if chech_face[0]:

            user_dict[chat_id]['photo_user'] = photo_path
            await state.update_data(photo_user=photo_path)

            keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,
                                                keyboard= [ 
                                                                        
                                                    [KeyboardButton(text=langueage_reew.translations[current_language]['Yes']), KeyboardButton(text=langueage_reew.translations[current_language]['No'])]
                                                    
                                                            ])

                        
                
            await state.set_state(Form.confirm_profiler)
            await message.answer(langueage_reew.translations[current_language]['Profile_make'], reply_markup=keyboard_key)
        else:
            kb_list = [
                        [InlineKeyboardButton(text="Приклад", callback_data="error_messages")]

                    ] 
            kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

            await message.answer("<b>Фото виявилось без вашого обличчя</b>\n\nБуло не виявлено обличчя, будь ласка надішліть з обличчям фото, обличчя повинно розположоене в центрі уваги, інакше ви будете заблоковані", reply_markup=kb, parse_mode="HTML")
    else:
        await message.answer("Вашу анкету не знайдено")

import face_recognition



async def get_images(photo_path, message: Message):
    
    #load_image_file
    get_file_image = face_recognition.load_image_file(photo_path)

    #face_locations with photo_path and return a photo
    unknown_image = face_recognition.face_locations(get_file_image, model='cnn')
    enconding = face_recognition.face_encodings(get_file_image, unknown_image)[0] 

    return unknown_image, enconding

@Start_dp.message(F.text, Form.confirm_profiler)
async def confirm_profile(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    text_confirm = message.text
    data = await state.get_data()

    if text_confirm == langueage_reew.translations[current_language]['Yes']:
        user_dict[chat_id] == text_confirm

    if 'name' not in user_dict.get(chat_id, {}) or 'username' not in user_dict.get(chat_id, {}):
        await message.answer(f"Вибачте, вам потрібно заповнити профіль перед тим як писати {text_confirm}.")
    else:
        user_dict[chat_id]['confirm_profiler'] = text_confirm
    
        if text_confirm == text_confirm == langueage_reew.translations[current_language]['Yes']:
            user_profile = {
                'user_id': data['user_id'],
                'name': data['name'],
                'age': data['age'],
                'gender': data.get('gender', 'Unknown'),
                'topic_chat': data.get('topic_chat', 'Not specified'),
                'bio': data.get('bio', 'Not provided'),
                'search_gender': data.get('search_gender', 'Not specified'),
                'partner_age_range': data.get('partner_age_range', 'Not specified'),
                'location': data.get('location'),
                'username': data.get('username'),
                'photo_user': data.get('photo_user'),

            }            
            user_profiles.append(user_profile)
            await message.answer("Дякую! Ваш профіль підтверджено.")
            
            try:
                await index.update_data_reew(chat_id)
                online_users.add(chat_id)
                await globalMenu.display_menu_global(message, state, current_language)
            except Exception as e:
                await message.answer(f"Error {str(e)}")
            await state.clear()

        else:
            if text_confirm == text_confirm == langueage_reew.translations[current_language]['No']:
                del user_dict[chat_id]

                await start(message, state)
                await state.clear()