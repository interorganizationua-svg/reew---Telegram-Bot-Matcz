import aiosqlite as sq
from setting import *
import asyncio



class DatabaseBot:

    def __init__(self, db_file):
         self.db_file = db_file
         self.lock = asyncio.Lock()
         try:
              self.connection = sq.connect(db_file)
              self.cursor = self.connection.cursor()
         except Exception as e:
              print(f'Error with database: {e}')
         pass
    
    async def __aenter__(self):
        self.db = await sq.connect(self.db_file)
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()

    async def db_start(self):
        async with sq.connect(self.db_file) as db:
                await db.execute("CREATE TABLE IF NOT EXISTS profile_info("
                            "chat_id INTEGER,"
                            "user_id INTEGER PRIMARY KEY,"
                            "name TEXT,"
                            "age TEXT,"
                            "gender TEXT,"
                            "topic_chat TEXT,"
                            "bio TEXT,"
                            "search_gender TEXT,"
                            "partner_age_range TEXT,"
                            "location TEXT,"
                            "username TEXT,"
                            "photo_user TEXT)")
                await db.commit()


    async def cmd_start_db(self, chat_id):
        async with sq.connect(self.db_file) as con:
            cur = await con.execute("SELECT * FROM profile_info WHERE chat_id = ?", (chat_id,))
            user = await cur.fetchone()
            if not user:
                await con.execute("INSERT OR REPLACE INTO profile_info (chat_id) VALUES (?)", (chat_id,))
                await con.commit()
                
    async def data_name(self,chat_id: str, name: int) -> None:
        async with sq.connect(self.db_file) as con:
            cursor = await con.cursor()
            request = "INSERT OR REPLACE INTO profile_info(chat_id, name) VALUES (?, ?)"
            await cursor.execute(request, (chat_id, name))
            await con.commit()
            
db_bot = DatabaseBot("database/DatabaseR.db")
