from database import *
from aiogram import Router
from aiogram import types
from main import bot, dp

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import asyncio
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext

from setting import *
from handlers import index, globalMenu
from aiogram.types import Message


translations = {
    'ru':{
        'start':(
            "👋 Привет! Я REEW - BETA — всегда готов помочь тебе найти друзей, вторую половинку или тиммейта!\n\n"
            "REEW отличается тем, что показывает ваши профили во время соединения — это наша главная изюминка. "
            "Перед тем как создавать профиль, вам должно быть 14 лет. Если готов(a), нажимай «Создать профиль».\n\n"
        ),
        'choose_language': "Оберите язык",
        'officale_message': "Официально переведено Reew",

        'change_lan': "Изменить язык",
        'create_acck': "Сделать профиль",
        'game': "Основной канал",

        #make profile on rus 
        'name': 'Напишите как вас зовут:',
        'name_evening': 'Добрый вечер, напишите как вас зовут:',

        'age_lg': 'Сколько вам лет?',
        'global': 'Сведу ваши сердца в одно целое',
        'choose_gender': 'Виберите свою стать:',
        'boy': 'Парень',
        'girl': 'Девушка',

        'small_age': 'Извините, мы увидели что вам меньше 14 лет, ваша регистрация отклонена',
        'сorrect_age': 'Пожалуйста, напишите правильный свой возраст(цифрами без пробелов)',
        'request_correct': 'Просим вас чтобы написали правильный свой возраст, ваш возраст не совпадает с вашим {age_text} ',
        #topic_chat
        'choose_topic': 'Выберите Тематику Диалога:',
        'selected_topic_but1': 'Обычный',
        'selected_topic': 'свободный разговор с собеседником в котором запрещено бросать намеки, просить, спрашивать, отправлять фото/видео то, что касается интима или сексуального толка. Бан выдается Шерифом',

        'selected_topic_but2': 'Флирт',
        'selected_topic2': 'можно обсуждать о любой теме, которая приходит на ум, включая контент 18+. Доступно всего от 18 лет. Бот проверяет возраст собеседника.',
       
        'flirt_18+_speak': 'Извините, но для доступа к Флирт диалогу нужно быть старше 18 лет',
        'flirt_18_small': 'Вы еще маленькие поэтому напишут «Обычный» диалог.',

        'choose_topic_1_2': 'Пожалуйста, выберите один из вариантов (Обычный или Флирт).',


        'bio': 'Опишите что-то о себе. Например: Что вас интересует в жизни?:',

        #Forb.bio
        'skip': 'Пропустить',
        'search_whom': 'Кого вам искать?',

        #Form.search_gender
        'her': 'Девушку',
        'his': 'Парня',
        'anything': 'Любого',

        'age_range': 'Выберите возрастной диапазон партнера:',

        #Form.partner_age_range
        'ADD_ragne': 'Можете добавить еще один возрастной диапазон или пропустите нажав Продолжить',
        
        #Form.location

        'city_was_born': 'Спасибо! Из какого вы города?',


        #Form.username

        'share': 'Поделиться UN',
        'Uncorrect_user': 'Вы не правильно указали свой username',


        #Form.photo_user

        'share_photo': 'Отправьте свое фото',

        'Profile_make': 'Профиль создан. Верно ли указана информация?',
        'Yes': 'Да',
        'No': 'Нет',


        #My Profile 
        'You': 'Вы',
        'search': 'Ищете:',
        'topic': 'Диалог:',
        'bonus': 'Бонусы:',
        'subcribe': 'Подписка:',


        'globalMenu': 'вы на главном меню:',
        'noneReew': 'Вы сейчас в текущем разговоре, завершите разговор если хотите искать другого',
        'interdiction': 'Пожалуйста, выберите один из вариантов:',

        'or': 'или',

    },      
    'ua':{
        'start':(
                    "👋 Привіт! Я REEW - BETA — завжди готовий допомогти тобі знайти друзів, супутника чи супутницю!\n\nREEW відрізняється тим, що показує ваші профілі під час з'єднання — це наша головна родзинка.  Перед тим як створювати профіль, повинно бути 14 років. Якщо готов(a) — натискай «Створити профіль».\n\n"        
        ),
        'choose_language': "Оберіть мову:",
        'officale_message': "Офіційно переведено Reew",
        'change_lan': "Змінить мову",
        'create_acck': "Створити профіль",
        'game': "Головний канал",
        'name': 'Напишіть, як вас звати:',
        'name_evening': 'Доброго вечора, напишіть як вас звати:',
        'age_lg': 'Скільки вам років?',
        'global': 'Зведу ваші серця в одне ціле',

            'choose_gender': 'Виберіть свою стать:',
            'boy': 'Хлопець',
            'girl': 'Дівчина',

            'small_age': 'Вибачте, ми побачили що вам менше 14 років, ваша реєстрація відхилена',
            'сorrect_age': 'Будь ласка, напишіть правильний свій вік (цифрами без пробілів)',
            'request_correct': 'Просимо вас, щоб написали правильний свій вік, ваш вік не збігається з вашим {age_text} ',
        #topic_chat
        'choose_topic': 'Оберіть Тематику Діалога:',
        'selected_topic_but1': 'Звичайний',
        'selected_topic': 'вільна розмова з співрозмовником у якій заборонено кидати натяки, просити, питати, відправляти фото/відео те що стосується інтима або сексуального спрямування. Бан видається Шеріфом',

        'selected_topic_but2': 'Флірт',
        'selected_topic2': 'можна обговорювати про будь-яку тему, що спадає на думку, включно з контентом 18+. Доступно лише від 18 років. Бот перевіряє вік співрозмовника.',

        'flirt_18+_speak': 'Вибачте, але для доступу до Флірт діалогу потрібно бути старше 18 років',
        'flirt_18_small': 'Ви ще маленькі тому напишуть "Звичайний" діалог.',

        'choose_topic_1_2': 'Будь ласка, оберіть одну з варіантів (Звичайний або Флірт).',

        #skip
        'bio': 'Опишіть щось про себе. Наприклад: Що вас цікавить в житті?:',

        #Forb.bio
        'skip': 'Пропустити',
        'search_whom': 'Кого вам шукати?',


        #Form.search_gender
        'her': 'Дівчину',
        'his': 'Хлопця',
        'anything': 'Будь-кого',

        'age_range': 'Виберіть віковий діапазон партнера:',

        #Form.partner_age_range
        'ADD_ragne': 'Можете додати ще один віковий діапазон або пропустіть натиснувши Продовжити',

        #Form.location
        'city_was_born': 'Дякую! З якого ви міста?',

        #Form.username

        'share': 'Поділитися UN',
        'Uncorrect_user': 'Ви не правильно вказали свій username',

        #Form.photo_user

        'share_photo': 'Відправте своє фото',
        'Profile_make': 'Профіль створено. Чи вірно вказана інформація?',

        'Yes': 'Так',
        'No': 'Ні',

        #My Profile 
        'You': 'Ви',
        'search': 'Шукаєте:',
        'topic': 'Діалог:',
        'bonus': 'Бонуси:',
        'subcribe': 'Підписка:',

        'globalMenu': 'ви на головному меню:',
        'noneReew': 'Ви зараз в поточній розмові, завершіть розмову якщо хочете шукати іншого',

        'interdiction': 'Будь ласка, оберіть одну з варіантів:',
        
        'or': 'aбо',

    },
    'pl':{
        'start':(
            "Cześć! Jestem REEW – zawsze gotowy, aby pomóc Ci znaleźć przyjaciół, "
            "drugą połówkę lub kolegę!\n\n"
            "REEW wyróżnia się tym, że pokazuje Wasze profile podczas połączenia – "
            "to nasza główna atrakcja. Przed stworzeniem profilu musisz mieć 14 lat. "
            "Jeśli jesteś gotowy(a) – kliknij „Stwórz profil”.\n\n"
            "Główny kanał z wiadomościami: @reewua"
        ),
        'choose_language': "Wybierz język:\n\n",
        'change_lan': "Zmień język ",
        'create_acck': "Utwórz konto",
    }

}

async def lan_current(state: FSMContext):
    data = await state.get_data()
    current_language = data.get('language', 'ua')
    
    return current_language

@dp.callback_query(lambda call: call.data == "langueage_choose")
async def callback_query(call: types.CallbackQuery, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = call.message.chat.id): 
        await asyncio.sleep(2)

    current_language = await lan_current(state)    

    if current_language is None:
        current_language = 'ua'

    message_reew = f"<b>{translations[current_language]['choose_language']}</b>\n\n{translations[current_language]['officale_message']}"

    kb_list = [
                    [InlineKeyboardButton(text="Українська 🇺🇦", callback_data="ua_lang"), InlineKeyboardButton(text="Русский 🇷🇺", callback_data="russian_langueage")],

                ] 
    kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

    await call.message.answer(text=message_reew, reply_markup=kb, parse_mode="HTML")

@dp.callback_query(lambda call: call.data == "ua_lang")
async def russian_langueage(call: types.CallbackQuery, state: FSMContext, current_language: str):
    await state.update_data(language='ua')
    chat_id = call.message.chat.id    

    if chat_id in user_dict and 'location' in user_dict[chat_id]:
        await globalMenu.display_menu_global(call.message, state, current_language)
    else:
        rus_bio = translations['ua']['global']
        await bot.set_my_short_description(short_description=rus_bio)

        kb_list = [
                    [InlineKeyboardButton(text=translations['ua']['change_lan'], callback_data="langueage_choose"), InlineKeyboardButton(text=translations['ua']['game'], url="https://t.me/reewua")],
                    [InlineKeyboardButton(text=translations['ua']['create_acck'], callback_data="create_profile")]
                ] 
        kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

            
        russ_start = translations['ua']['start']

        await call.message.answer(russ_start, reply_markup=kb)


@dp.callback_query(lambda call: call.data == "russian_langueage")
async def russian_langueage(call: types.CallbackQuery, state: FSMContext, current_language: str):
    await state.update_data(language='ru')
    chat_id = call.message.chat.id    

    if chat_id in user_dict and 'location' in user_dict[chat_id]:
        await globalMenu.display_menu_global(call.message, state, current_language)
    else:
        rus_bio = translations['ru']['global']
        await bot.set_my_short_description(short_description=rus_bio)

        kb_list = [
                    [InlineKeyboardButton(text=translations['ru']['change_lan'], callback_data="langueage_choose"), InlineKeyboardButton(text=translations['ru']['game'], url="https://t.me/reewru")],
                    [InlineKeyboardButton(text=translations['ru']['create_acck'], callback_data="create_profile")]
                ] 
        kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

            
        russ_start = translations['ru']['start']

        await call.message.answer(russ_start, reply_markup=kb)


@dp.callback_query(lambda call: call.data == "pl_langueage")
async def russian_langueage(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(language='pl')
    

    kb_list = [
                [InlineKeyboardButton(text=translations['pl']['change_lan'], callback_data="langueage_choose"), InlineKeyboardButton(text=translations['pl']['game'], callback_data="game_reew")],
                [InlineKeyboardButton(text=translations['pl']['create_acck'], callback_data="create_profile")]
            ] 
    kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

        
    russ_start = translations['pl']['start']

    await call.message.answer(russ_start, reply_markup=kb)


@dp.callback_query(lambda call: call.data == "error_messages")
async def error_message(message: types.Message, state: FSMContext):
    message_error = (f"📩 Не працює технічно, помилка виправляється")

    await message.answer(message_error)
    