from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext

from setting import user_dict, bot

Course = Router()

@Course.message(lambda meesage: meesage.text == "Конкурс")
async def tourner_reew(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    if chat_id in user_dict and 'confirm_profiler' in user_dict[chat_id]:
        rules_game = (f"<b>Конкурс REEW</b>\n\n"
                    f"<b>Як прийняти участь:</b>\n"
                    f"1. Зареєструватися в боті\n"
                    f"2. Підписатися на канал REEW\n"
                    f"3. Натиснути на кнопку Прийняти участь\n\n"
                    f"<b>Суть конкурса</b>:\n"
                    f"Чим більше білетів тим більший шанс перемогти, ми запровадили реферальне посилання по якому можете запрошувати друзів - кожен друг = 1 білет, і другий варіант - купівля вогнів що дуже спрощує накопчивати білетів\n\n"

                    f"<b>Прийняли участь</b>: 0\n\n"
                    f"У 2025 році пройде наймасштабний конкурс на вогні та декілька преміум підписок в тг, конкурс буде тривати 2 тижні"
                    ) 
        kb_list = [
                    [InlineKeyboardButton(text="Прийняти участь", callback_data="click_on_course"), InlineKeyboardButton(text="Додати друга", callback_data="add_friends")],
                    [InlineKeyboardButton(text="Топ місця", callback_data="error_messages")]

                ] 
        kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

        await message.answer(rules_game, reply_markup=kb, parse_mode='HTML')
    else:
        await message.edit_text('Вам потрібно створити профіль')  # Редагуємо текст повідомлення

@Course.callback_query(lambda call: call.data == "click_on_course")
async def course_click(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    if chat_id in user_dict:  # Перевіряємо, чи chat_id є в user_dict
        await call.message.edit_text('Ви прийняли участь')  # Редагуємо текст повідомлення
    else:
        await call.message.edit_text('Вам потрібно створити профіль')  # Редагуємо текст повідомлення
