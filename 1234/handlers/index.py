import os
import re

from datetime import datetime, timedelta, time

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from buttonKey import ButtonText

import random
import string

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import Router, F
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import CommandStart, Command

from handlers import langueage_reew as lg, start, globalMenu as Menu, factNight
from setting import user_dict, chat_reew, add_chatReew, last_activity, bot, dp


#диспетчер 
questionnaire_router  = Router()

async def update_data_reew(chat_id):
    last_time = datetime.now()
    last_activity[chat_id] = last_time  # Store the last activity timestamp


@questionnaire_router.message(F.text == '🛒 Магазин')
async def shops_reew(message: Message, state: FSMContext):
    chat_id = message.chat.id

    if chat_id in chat_reew:
        await bot.send_message(chat_id,"Ви зараз в поточній розмові, завершіть розмову якщо хочете шукати іншого")
        return 

    if chat_id in user_dict:
        shop_message = (
            f"<b>Магазин Reew</b>\n\n"
            f"<b>💰 Прайси:</b>\n"
            f"—❤️ 10 Сердець : <b> 5 грн</b>\n"
            f"—📅 Місячна підписка: <b> 210 грн</b>\n\n"
                        
            f"<b>Що дає підписка:</b>\n"
            f"1. ✨ <b>Ексклюзивний статус</b> підписника в анкеті\n"
            f"2. 🚫 <b>Можливість блокування</b> користувачів, щоб вони більше не з'являлися\n"
            f"3. 💬 <b>Спілкування</b> без набридливої реклами\n"
            f"4. 🔗 <b>Відправлення посилань</b> у флірт-діалогах\n"
            f"5. ✏️ <b>Можливість змінювати анкету</b> у будь-який момент\n\n"

            f"Акція дійсна з дня оголошення конкурса і до завершення конкурса!\n\n"

            f"<i>Після замовлення надішліть номер замовлення Шеріфам.</i>\n"
        )
        kb_list = [
                    [InlineKeyboardButton(text="Замовити ❤️", callback_data="error_messages"), InlineKeyboardButton(text="Оформити підписку", callback_data="error_messages")],
                    [InlineKeyboardButton(text="Питання", callback_data="error_messages")]

                ] 
        kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

        await message.answer(shop_message, reply_markup=kb, parse_mode="HTMl")   
    else:
        await message.answer("Для початку щоб щось відкрити Магазин, потрібно створити профіль /start.")

MAIN_MENU = 'Налаштування'

user_state = {}

def update_user_state(user_id, state):
    user_state[user_id] = state

def get_user_state(user_id):
    return user_state.get(user_id, MAIN_MENU)

@questionnaire_router.message(lambda message: message.text == MAIN_MENU)
async def setting_users(message: Message, state: FSMContext):
    chat_id = message.chat.id
    update_user_state(message.from_user.id, MAIN_MENU)


    if chat_id in chat_reew:
        await bot.send_message(chat_id,"Ви зараз в поточній розмові, завершіть розмову якщо хочете шукати іншого")
        return 

    if chat_id in user_dict:
        chat_settings = f"⚙️Налаштування:"

        keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,
                                           keyboard= [ 
                                                                
                                            [KeyboardButton(text='Мій профіль'), KeyboardButton(text='Техпідтримка')],
                                            [KeyboardButton(text='Назад')],

                                                    ])
        await message.answer(chat_settings, reply_markup=keyboard_key)   
    else:
        await message.answer("Для початку щоб відкрити Налаштування, потрібно створити профіль /start.")


@dp.message(lambda message: message.text == 'Змінить мову')
async def request_transltation(message: types.Message, state: FSMContext, current_language: str):

    message_reew = lg.translations[current_language]['choose_language']

    kb_list = [
                    [InlineKeyboardButton(text="Українська 🇺🇦", callback_data="ua_lang"), InlineKeyboardButton(text="Русский 🇷🇺", callback_data="russian_langueage")],

                ] 
    kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

    await message.answer(text=message_reew, reply_markup=kb, parse_mode="HTML")

@questionnaire_router.message(lambda message: message.text == ButtonText.Назад)
async def back_setting(message: Message, state: FSMContext, current_language: str):  
    user_id = message.from_user.id
    current_state = get_user_state(user_id)

    if current_state == MAIN_MENU:
        update_user_state(user_id, Menu.MAIN_SCREEN)
        await Menu.display_menu_global(message, state, current_language)
    else:
        await Menu.display_menu_global(message, state, current_language)


@questionnaire_router.message(lambda message: message.text in ["Мій профіль"])
async def check_profiles_(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id

    if chat_id in chat_reew:
        await bot.send_message(chat_id,"Ви зараз в поточній розмові, завершіть розмову якщо хочете шукати іншого")
        return 

    if chat_id in user_dict:
        profile_info = user_dict[chat_id]

        partner_age_range = user_dict[chat_id]['partner_age_range']
        format_age = ', '.join(partner_age_range)

        check_profiles_user = ( f"<b>{lg.translations[current_language]['You']}</b> {profile_info['name']} ({profile_info['gender']}, {profile_info['age']} років, {profile_info['location']}) \n"
                                f"<b>{lg.translations[current_language]['search']}</b> {profile_info['search_gender']}, {format_age}\n"
                                f"<b>{lg.translations[current_language]['topic']}</b>  {profile_info['topic_chat']} \n" 
                                f"<b>{lg.translations[current_language]['bonus']}</b> 0 ❤️ \n" 
                                )
        
        username = profile_info['username']
        
        if profile_info['username']:
            check_profiles_user += f'<b>Username:</b> @{username}'

        keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,
                                           keyboard= [ 
                                                                
                                            [KeyboardButton(text='👤 Змінити анкету'), KeyboardButton(text='Видалити профіль')],
                                            [KeyboardButton(text='Назад')]

                                                    ])
        src = f'photos/{chat_id}.jpg'
        if os.path.exists(src):
            with open(src, 'rb') as photo:        
                await message.answer_photo(
                types.FSInputFile(path=src), caption=check_profiles_user, reply_markup=keyboard_key, parse_mode="HTML")
        else:
            await message.answer(check_profiles_user, reply_markup=keyboard_key, parse_mode="HTML")
    else:
        kbs = types.ReplyKeyboardRemove()
        await message.answer("Для початку щоб відкрити Профіль, потрібно створити профіль /start.", reply_markup=kbs)

@questionnaire_router.message(lambda message: message.text in ["Видалити профіль"])
async def delete_account(message: Message, state:FSMContext):
    chat_id = message.chat.id

    if chat_id not in user_dict and 'confirm_profiler' not in user_dict:
        await bot.send_message(chat_id,"Ви не можете видалити профіль якщо не зареєстровані")

    if chat_id in user_dict:

        keyboard_key = ReplyKeyboardMarkup(row_width= 2,resize_keyboard=True, 
                                    keyboard = [

                                        [KeyboardButton(text='Підтвердити'), KeyboardButton(text='Відхилити')]
                                        ])
        
        await message.answer("Підтвердіть що ви точно хочете видалити профіль з бота. Відхиліть якщо хочете залишитися", reply_markup=keyboard_key)
    

@questionnaire_router.message(lambda message: message.text in ["Підтвердити"] )
async def delete_account(message: Message, state:FSMContext):
    chat_id = message.chat.id
    if chat_id not in user_dict and 'confirm_profiler' not in user_dict:
        await bot.send_message(chat_id,"Ви не можете видалити профіль якщо не зареєстровані")

    if chat_id in user_dict and 'confirm_profiler' in user_dict:
        del user_dict[chat_id]
        await bot.send_message(chat_id,"Ви успішно видалили профіль з бота")

@questionnaire_router.message(lambda message: message.text in ["Відхилити"] )
async def delete_account(message: Message, state:FSMContext, current_language: str):
    chat_id = message.chat.id
    if chat_id not in user_dict and 'confirm_profiler' not in user_dict:
        await bot.send_message(chat_id,"Ви не можете видалити профіль якщо не зареєстровані")

    if chat_id in user_dict and 'username' in user_dict:
        await Menu.display_menu_global(message, state, current_language)


@questionnaire_router.message(lambda message: message.text == "Живчики")
async def lives_profiles(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id

    if chat_id in chat_reew:
        await bot.send_message(chat_id,"Ви зараз в поточній розмові, завершіть розмову якщо цікаво скільки онлайн")
        return 

    if chat_id in user_dict:

        
        await update_data_reew(chat_id)

        online_girls = 0 
        online_boys = 0

        topic_online_boys = 0
        topic_online_girls = 0
        topic_online_boys_18 = 0
        topic_online_girls_18 = 0

        currently_time = datetime.now()
        print(f"last_activity: {last_activity}")

        online_users = [user_id for user_id, last_time in last_activity.items()
                        if currently_time - last_time < timedelta(minutes=10)]

        print(f"Online users: {online_users}")
        
        for_you_count = 0

        # Count online profiles
        for user_id in online_users:
            if user_id in user_dict:
                #пошук за гендером

                profile = user_dict[user_id]
                if profile['gender'] == lg.translations[current_language]['girl']:
                    online_girls += 1
                elif profile['gender'] == lg.translations[current_language]['boy']:
                    online_boys += 1

                #пошук за топом
                if profile['topic_chat'] == lg.translations[current_language]['selected_topic_but1']:
                    if profile['gender'] == lg.translations[current_language]['boy']:
                        topic_online_boys += 1
                    elif profile['gender'] == lg.translations[current_language]['girl']:
                            topic_online_girls += 1

                elif profile['topic_chat'] == lg.translations[current_language]['selected_topic_but2']:
                    if profile['gender'] == lg.translations[current_language]['boy']:
                        topic_online_boys_18 += 1
                    elif profile['gender'] == lg.translations[current_language]['girl']:
                            topic_online_girls_18 += 1        
                
                #пошук за гендера партнера
                if profile['gender'] == lg.translations[current_language]['girl']:
                    if profile['search_gender'] == lg.translations[current_language]['his']:
                            for_you_count += 1
                    elif profile['gender'] == lg.translations[current_language]['boy']:
                        if profile['search_gender'] == lg.translations[current_language]['her']:
                                for_you_count += 1

        together_online = online_girls + online_boys


        if together_online == 0:
            await bot.send_message(chat_id, "Наразі нікого немає 😔")
        else:
            profiles_text = (
                f"<b>🔹 Активних в чаті</b>:\n"
                f"👧 Дівчат: {online_girls} | 👦 Хлопців: {online_boys}\n\n"
                f"<b>💙 У Звичайному діалозі</b>:\n"
                f"👧 Дівчат: {topic_online_girls} | 👦 Хлопців: {topic_online_boys}\n\n"
                f"<b>💕 У Флірт діалозі</b>:\n"
                f"👧 Дівчат: {topic_online_girls_18} | 👦 Хлопців: {topic_online_boys_18} \n\n"

                f"🫵 Онлайн для тебе: {for_you_count}\n"
                f"🔸🔸🔸🔸🔸🔸🔸🔸🔸\n"
                f"🌐 Всього онлайн: {together_online}\n"
            )
            
            kb_list = [
                [InlineKeyboardButton(text="Оновити", callback_data="error_messages")]
            ] 
            kb = InlineKeyboardMarkup(inline_keyboard=kb_list)
            
            await message.answer(profiles_text, reply_markup=kb, parse_mode='HTML')
    else:
        await message.answer("Щоб дізнатися скільки користувачів онлайн, вам потрібно створити профіль /start.")


@dp.message(lambda message: message.text == "🔎 Пошук")
async def search_profiles(message: Message, current_language: str, state: FSMContext):
    chat_id = message.chat.id


    if chat_id in chat_reew:
        await bot.send_message(chat_id, "Ви зараз в поточній розмові, завершіть розмову якщо хочете шукати іншого")
        return 
    
    if chat_id in user_dict and 'confirm_profiler' in user_dict[chat_id]:
        #add user in searching reew
        add_chatReew.add(chat_id)

        #перевірка активності
        await update_data_reew(chat_id)
        partner_age_range = user_dict[chat_id]['partner_age_range'] 
        format_age = ', '.join(partner_age_range)

        profile_info = user_dict[chat_id]
        send_request = f"🔎 Шукаю тобі {profile_info['search_gender']} ({format_age}), діалог {profile_info['topic_chat']} "
        keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,
                                           keyboard= [ 
                                                                
                                            [KeyboardButton(text='Скасувати пошук')]

                                                    ])        
        await message.answer(send_request, reply_markup=keyboard_key)

        #found parter in REEW
        search_partner = await find_partner(chat_id, profile_info, current_language)
        
        if search_partner:
            for match in search_partner:
                if match in chat_reew:
                    continue
        
                match_info = user_dict[match]
                match_message = (f"Вас зєднано з співрозмовником {match_info['name']}, {match_info['age']}, {match_info['location']}\n")

                if match_info['bio']:
                    match_message += match_info['bio']

                partner_message = ( f"Вас зєднано з співрозмовником\n"
                                f"{profile_info['name']}, {profile_info['age']}, {profile_info['location']}\n\n")
                
                if profile_info['bio']:
                    partner_message += profile_info['bio']

                keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,
                                                keyboard= [                  
                                                    [KeyboardButton(text='Припинити розмову'), KeyboardButton(text='Запросити UN')]
                                                ])
                await state.update_data(keyboard_key=keyboard_key)

                chat_reew[chat_id] = match
                chat_reew[match] = chat_id

                src = f"photos/{chat_id}.jpg"
                if os.path.exists(src):
                    with open(src, 'rb') as photo:        
                        await bot.send_photo(match, types.FSInputFile(path=src) ,caption=partner_message, reply_markup=keyboard_key)
                else:
                    await message.answer("На жаль, поки немає підходящих збігів. Спробуйте пізніше.")


                src = f"photos/{match}.jpg"
                if os.path.exists(src):
                    with open(src, 'rb') as photo:        
                        await bot.send_photo(chat_id, types.FSInputFile(path=src), caption=match_message, reply_markup=keyboard_key)

                else:
                    await message.answer("На жаль, поки немає підходящих збігів. Спробуйте пізніше.")

                add_chatReew.remove(chat_id)
                add_chatReew.remove(match)
                break
        else:
            if chat_id in add_chatReew:
                check_time = datetime.now().time()
                thous_check = time(18, 0)
                end_time = time(5, 0)

                text_wait = (
                    "🔍 Шукаємо для вас співрозмовника! Як тільки знайдемо – одразу вас з'єднаємо 😊\n\n"
                    "⏳ Втомились чекати? Ви завжди можете скасувати пошук і спробувати пізніше.\n\n"
                    "Я тут, щоб зробити ваше спілкування приємним! 💬"
                )
       
                if chat_id not in add_chatReew:
                
                    # Перевірка перед сном
                    await asyncio.sleep(10)  # Затримка тільки якщо не потрібно виходити
                    await message.answer(text_wait, parse_mode='HTML')
                    return
                
                if thous_check <= check_time <= end_time:
                    text = f'<b>Цікаві факти на ніч:</b> {random.choice(factNight.list1)}'
                    text_wait += "\n\n" + text
                    await message.answer(text_wait, parse_mode='HTML')
    else:
        keyboard_del = types.ReplyKeyboardRemove()
        await message.answer("Для початку створіть профіль /start.", reply_markup=keyboard_del)


@questionnaire_router.message(lambda message: message.text == 'Запросити UN')
async def username_send_reew(message: Message, state: FSMContext):
    chat_id = message.chat.id

    if chat_id in user_dict:
        if chat_id in chat_reew:

            partner_id = chat_reew[chat_id]
            chat_id = chat_reew[partner_id]    

            keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,
                                                    keyboard= [ 
                                                                            
                                                        [KeyboardButton(text='Надіслати'), KeyboardButton(text='Відмовити')]
                                                        
                                                                ])

            await bot.send_message(partner_id, f"Розмовник просить у вас username, чи готові надіслати?", reply_markup=keyboard_key)
        

@questionnaire_router.message(lambda message: message.text in ['Надіслати', 'Відмовити'])
async def username_send_reew_Yes_NO(message: Message, state: FSMContext):
    chat_id = message.chat.id
    text_message = message.text

    data = await state.get_data()
    keys = data.get('keyboard_key')


    if chat_id in user_dict:
        if chat_id in chat_reew:

            partner_id = chat_reew[chat_id]
            original_chat_id = chat_id
            chat_id = chat_reew[partner_id]  

            if text_message == 'Надіслати':
              
                    profile_info = user_dict[chat_id]
                    username_profile = profile_info['username']

                            
                    if profile_info:  
                                
                        username_link = f'https://t.me/{username_profile}   '
                        keyboard = [[InlineKeyboardButton(text='Перейти в лс', url=username_link)]]
                                
                        key = InlineKeyboardMarkup(inline_keyboard=keyboard)
                        await bot.send_message(partner_id, f"Вашого співрозмовника username: {username_profile}", reply_markup=key)
                        await bot.send_message(chat_id, f"Було успішно надіслано ваш username", reply_markup=keys)

            else:
                if text_message == 'Відмовити':
                    await bot.send_message(original_chat_id, f"Ви скасували запрос на username", reply_markup=keys)
                    await bot.send_message(partner_id, f"Вам відмовили давати username", reply_markup=keys)
        else:
            await bot.send_message(chat_id, f"Ви ні з ким не спілкуєтесь. Перейдіть в чат щоб отримати username розмовника")
    else:
        await bot.send_message(chat_id, f"Виявилось що у вас немає профілю. Створіть будь ласка профіль через команду /start")

@questionnaire_router.message(lambda message: message.text == "Припинити розмову")
async def chat_message_stop(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    
    
    if chat_id in user_dict and 'confirm_profiler' in user_dict[chat_id]:
        if chat_id in chat_reew:
            
            partner_id = chat_reew[chat_id]
            chat_id = chat_reew[partner_id]

            await update_data_reew(chat_id)

            Keyboard = [ 
                [InlineKeyboardButton(text='Поскаржитись', callback_data="new"), InlineKeyboardButton(text='Заблокувати', callback_data="new")], 

            ]
            set_key = InlineKeyboardMarkup(inline_keyboard=Keyboard)

            await bot.send_message(chat_id, "<b>🚪Ви від'єднались від співрозмовника</b>\n\nЯкщо співрозмовник вам не сподобався — заблокуйте його\nЯкщо порушив правила — поскаржтесь нам",reply_markup=set_key, parse_mode="HTML")
            
            await bot.send_message(partner_id,"<b>🚪Співрозмовник від'єднався.</b>\n\nЯкщо співрозмовник вам не сподобався — заблокуйте його\nЯкщо порушив правила — поскаржтесь нам\n", reply_markup=set_key, parse_mode="HTML")

            del chat_reew[partner_id]
            del chat_reew[chat_id]
            
            add_chatReew.discard(chat_id)
            add_chatReew.discard(partner_id)
            
            keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,
                                        keyboard=[ 
                                                [KeyboardButton(text='🔎 Пошук'), KeyboardButton(text='Живчики')],
                                                [KeyboardButton(text='Налаштування')]
                                            ])
            
            profile_info = user_dict[chat_id]
            profile_infos = user_dict[partner_id]

            await bot.send_message(partner_id, f"<b>{profile_infos['name']}</b>, ви на головному меню:", reply_markup=keyboard_key, parse_mode='HTML')

            await bot.send_message(chat_id, f"<b>{profile_info['name']}</b>, ви на головному меню:", reply_markup=keyboard_key, parse_mode='HTML')
        else:
            await message.answer("Ви не розмовляєте з співрозмовником")
    else:
        await start.start(message, state, current_language)

@questionnaire_router.message(lambda message: message.text == 'Техпідтримка')
async def handle_support(message: Message, state: FSMContext):
    chat_id = message.chat.id

    if chat_id in chat_reew:
        await bot.send_message(chat_id,"Ви зараз в поточній розмові, завершіть розмову якщо хочете написати адмінам")
        return 

    if chat_id in user_dict:
        user_id = user_dict[chat_id]['user_id']
    else:
        user_id = "Не виявлено"

    support_text = (
        f"<b>Техпідтримка REEW</b>\n\n"

        f"Зв'язок з Шеріфом: @djdjsjddj\n\n"

        f"🔑 ID: <code>{user_id}</code>\n\n"
        f"<i><b>⚠️ Увага:</b> Нікому не передавайте свій ID окрім Шеріфу.</i>\n\n"
    )

    key_keyboard = [
                    [InlineKeyboardButton(text="📄 Правила", url="https://pypi.org/project/pyTelegramBotAPI/#getting-started")],
                    ]
    kb = InlineKeyboardMarkup(inline_keyboard=key_keyboard)
    await message.answer(support_text, parse_mode = 'HTML', reply_markup=kb)


async def display_menu_global_by_id(message: types.Message, state: FSMContext):
    keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,
                                keyboard=[ 
                                        [KeyboardButton(text='🔎 Пошук'), KeyboardButton(text='Живчики')],
                                        [KeyboardButton(text='Налаштування')]
                                    ])
    
    return "ви на головному меню:", keyboard_key


async def find_partner(chat_id, profile_info, current_language: str):
    potential_matches = []
    current_time = datetime.now()

    if chat_id in user_dict and 'confirm_profiler' in user_dict[chat_id]:
        for user_id, user_data in user_dict.items():

            # Skip the user themselves and check last activity
            if user_id != chat_id and user_id in last_activity and user_id in add_chatReew:
                last_active_time = last_activity[user_id]

                # Check if the user was active in the last 10 minutes
                if (current_time - last_active_time) < timedelta(minutes=1):
                    print(f"Checking user {user_id}, {user_data}, Looking for: {user_data['search_gender']}")
                    print(f"user {chat_id}, {profile_info['gender']}, Looking for: {profile_info['search_gender']}")


                    user_profile_gender = profile_info['gender']  # Стать користувача
                    user_search_gender = profile_info['search_gender']  # Кого шукає користувач

                    topic_chat_user = profile_info['topic_chat']

                    print(f"{user_id} {user_profile_gender}, Looking for: {user_search_gender} {topic_chat_user}")
                    print(f"{chat_id} {user_profile_gender}, Looking for: {user_search_gender} {topic_chat_user}")

                    is_match = any([
                        user_profile_gender == lg.translations[current_language]['boy'] and user_search_gender == lg.translations[current_language]['her'],
                        user_profile_gender == lg.translations[current_language]['girl'] and user_search_gender == lg.translations[current_language]['his'],
                        user_profile_gender == lg.translations[current_language]['boy'] and user_search_gender == lg.translations[current_language]['anything'],
                        user_profile_gender == lg.translations[current_language]['girl'] and user_search_gender == lg.translations[current_language]['anything']
                    ])


                    if is_match:
                        if user_data['gender'] != profile_info['search_gender']:
                            potential_matches.append(user_id)
                            print(f"Match found: {user_data['name']} for {profile_info['name']}")
                            break

        if potential_matches:               
            print(f"Potential matches for {chat_id}: {potential_matches}")
            return potential_matches
        else:
            print(f"No potential matches found for {chat_id}.")
            return []
    else:
        print(f"Chat ID {chat_id} not found in user_dict.")
        return []



@questionnaire_router.message(lambda message: message.text == "Скасувати пошук")
async def search_profiles(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id

    if chat_id in chat_reew:
        await bot.send_message(chat_id,"Ви зараз в поточній розмові, завершіть розмову якщо хочете шукати іншого")
        return 

    if chat_id in user_dict:
        keyboard_key = ReplyKeyboardMarkup(resize_keyboard=True,

            keyboard= [ 
                                                                    
            [KeyboardButton(text='🔎 Пошук'), KeyboardButton(text='Живчики')],
            [KeyboardButton(text='Налаштування')],

            ])

        await Menu.display_menu_global(message, state, current_language)

        if chat_id in chat_reew:
            partner_id = chat_reew[chat_id]
            del chat_reew[chat_id]
            del chat_reew[partner_id]
                # Send the photo with the profile text and keyboard
            await message.answer("<b>Ви скасували пошук</b>", reply_markup=keyboard_key, parse_mode="HTML") 
    else:
        await message.answer("Для початку створіть профіль /start.")

URL_BLOCK = re.compile(r"(https://)")

@dp.message(lambda message: message.text and URL_BLOCK.search(message.text))
async def send_line(message: types.Message, state: FSMContext):
    await message.delete()
    key_board = [ 
        [InlineKeyboardButton(text="Читати правила", url="https://pypi.org/project/pyTelegramBotAPI/#getting-started")] 
        ]
    ks = InlineKeyboardMarkup(inline_keyboard=key_board) 
    await message.answer("🚫У REEW забороняється відправляти посилання, ознайомтесь з правилами", reply_markup=ks)   

NM_BLOCK = re.compile(r"(@)")
@dp.message(lambda message: message.text and NM_BLOCK.search(message.text))
async def block_send_nm(message: Message, state: FSMContext):
    chat_id = message.chat.id

    if chat_id in chat_reew:

        await message.delete()
        await bot.send_message(chat_id, "За новими правилами REEW заборонено відправляти username в чат")

