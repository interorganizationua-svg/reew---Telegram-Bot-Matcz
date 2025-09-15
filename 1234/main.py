from setting import bot, dp
from database import database as db
from handlers import reew_chat, index, course, start

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import Router, F

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.methods import DeleteWebhook

from handlers import langueage_reew

async def setting_bot():
    new_bio = "Хочеш Забалакти? Го Забалакаємо"
    await bot.set_my_short_description(short_description=new_bio)

    hello_reew = "Привіт, не знаєш з ким Забалакати? Го Забалакаємо"
    await bot.set_my_description(description=hello_reew)

class LanguageMiddleware(BaseMiddleware):

    async def translation_all(self, data: dict):
        state: FSMContext = data['state']
        # Отримуємо поточну мову
        current_language = await langueage_reew.lan_current(state)

        # Зберігаємо в контекст
        data['current_language'] = current_language

    async def __call__(self, handler, event: Message, data: dict):
        state: FSMContext = data['state']

        current_language = await langueage_reew.lan_current(state)

        data['current_language'] = current_language

        return await handler(event, data)


async def on_startup():
    await db.db_bot.db_start()
    print("Успішно працює")


async def main():
    #routers with functions
    dp.include_router(index.questionnaire_router)
    dp.include_router(course.Course)
    dp.include_router(reew_chat.Chat_router)
    dp.include_router(start.Start_dp)

    #Second simple middlewares, first for message and second for callback request handler
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())



    await setting_bot()

    await asyncio.sleep(1)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)
    
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == '__main__':
    asyncio.run(main())