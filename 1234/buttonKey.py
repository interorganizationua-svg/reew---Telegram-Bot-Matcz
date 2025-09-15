from aiogram import types
from setting import user_dict  # Импорт базы данных

class ButtonText:
    Назад = 'Назад'
    Правила = 'Правила'
    Техпідтримка = 'Техпідтримка'

async def rules_bots(bot, message):
    chat_id = message.chat.id 

    if chat_id in user_dict:
        url_rules = (f"<b>Правила чата:</b>\n\nАктуальні правила за посиланням: https://pypi.org/project/pyTelegramBotAPI/#getting-started\n\nПри реєстрацію ви погоджуєтеся з правилами бота")
        keyboard_profil = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton(text="⬅️ назад")
        keyboard_profil.add(back_button)

        await message.answer(chat_id, url_rules, reply_markup=keyboard_profil, parse_mode='HTML')
    else:
        remove_key = types.ReplyKeyboardRemove()
        await message.answer(chat_id, "Ви ще не створили профіль, натисніть на /start", reply_markup=remove_key)
