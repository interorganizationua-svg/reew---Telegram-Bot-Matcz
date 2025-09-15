from main import *
from setting import *
from handlers import langueage_reew, index
import os
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import types

MAIN_SCREEN = 'global_menu'  # Додамо стан для головного меню

@dp.message(lambda message: message.text == MAIN_SCREEN)
async def display_menu_global(message: Message, state: FSMContext, current_language: str):
    chat_id = message.chat.id
    
    if chat_id in chat_reew:
        await bot.send_message(chat_id,{langueage_reew.translations[current_language]['noneReew']})
        return 
    
    # Check if the user has created a profile
    if chat_id in user_dict:
        profile_info = user_dict[chat_id]
        
        await index.update_data_reew(chat_id)

        
        # Compose the profile text
        profile_text = (
            f"<b>{profile_info['name']}</b>, {langueage_reew.translations[current_language]['globalMenu']}\n"
        )

        set_key = ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True,
                    keyboard= [
                                            
                                            [KeyboardButton(text='🔎 Пошук'), KeyboardButton(text='Живчики')],
                                            [KeyboardButton(text='Налаштування')]

                                            
                                            ])
    
    
        src = f'photos/{chat_id}.jpg'
        if os.path.exists(src):
            with open(src, 'rb') as photo:  
                await message.answer_photo(    
                types.FSInputFile(path=src), caption=profile_text, reply_markup=set_key, parse_mode="HTML")
        else:
            await message.answer(profile_text, reply_markup=set_key, parse_mode="HTML")
        
        await state.update_data(profile_info)
    else:
        kbs = types.ReplyKeyboardRemove()
        await message.answer("Виявилось що у вас ще немає профілю, нажміть /start", reply_markup=kbs)

