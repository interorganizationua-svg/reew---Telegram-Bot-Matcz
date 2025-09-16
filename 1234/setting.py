from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


#токен бота
TOKEN = 'None'
bot = Bot(token=TOKEN)

#memory storage
storage=MemoryStorage()

#маршутотизатор
dp = Dispatcher(storage=MemoryStorage())

user_profiles = []
gender_selection = {}  # Global dictionary to store gender selection
online_users = set()
last_activity = {}


user_dict = {} #всі дані користувача 

add_chatReew = set()

chat_reew = {} #chat_with_partner


