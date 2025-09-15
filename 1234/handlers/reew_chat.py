from main import Router, types
from setting import *

Chat_router = Router()

@Chat_router.message(lambda message: message.chat.id in chat_reew and message.text)
async def chat_message(message: types.Message):
    chat_id = message.chat.id
    text = message.text

    if chat_id in chat_reew:
        partner_id = chat_reew[chat_id]
        await bot.send_message(partner_id, text=text)

@Chat_router.message(lambda message: message.chat.id in chat_reew and message.photo)
async def send_photo(message: types.Message):
    chat_id = message.chat.id

    if chat_id in chat_reew:
        photo = message.photo[0]

        partner_id = chat_reew[chat_id]
        await bot.send_photo(partner_id, photo=photo)
        
