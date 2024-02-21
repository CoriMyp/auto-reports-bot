from aiogram import Bot
from aiogram.enums import ParseMode

import sqlite3 as sql
from typing import Optional

#  main: 6842489166:AAE8T14fSydhLQa31YFc856uluEKueO15LE
#  test: 6822076191:AAHXgAWqa-Ithds3udJh2dAPUNPJkzH417A
TOKEN = "6842489166:AAE8T14fSydhLQa31YFc856uluEKueO15LE"
bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN_V2)

ALLOWED = [1004461367, 447050022]


db = sql.connect("database.db")
cursor = db.cursor()


# to work with sqlite3 db
def execute(query: str, res=True) -> Optional[str]:
    if res:
        result = cursor.execute(query).fetchone()
    else:
        result = cursor.execute(query).fetchall()

    db.commit()
    return result[0] if res and result else result
